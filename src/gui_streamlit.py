"""
gui_streamlit.py – Interfaz gráfica Streamlit para Casa Monarca MILP
======================================================================
Ejecutar desde la raíz del proyecto:
    streamlit run src/gui_streamlit.py
"""

import sys
import os
from datetime import datetime

# Permite importar módulos hermanos en src/
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import streamlit as st

from milp_model_core import (
    DEFAULT_B,
    DEFAULT_COST,
    DEFAULT_DEMAND,
    DEFAULT_DONATIONS,
    DEFAULT_INITIAL_INV,
    DEFAULT_LOT_SIZE,
    DEFAULT_SCHEDULE,
    DAY_NAMES,
    DISH_NAMES,
    INSUMO_NAMES,
    MEAL_NAMES,
    solve_milp,
)
from result_tables import (
    make_consumption_df,
    make_cost_summary_df,
    make_inventory_df,
    make_meal_plan_df,
    make_purchases_df,
)

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Casa Monarca – MILP",
    page_icon="🦋",
    layout="wide",
)

st.title("Casa Monarca – Optimización MILP")
st.caption("Minimiza el costo de adquisición de insumos durante una semana (7 días, 3 tiempos de comida, 100 porciones).")

# ──────────────────────────────────────────────────────────────────────────────
# PARÁMETROS GLOBALES
# ──────────────────────────────────────────────────────────────────────────────

with st.expander("Parámetros globales", expanded=True):
    col1, col2 = st.columns(2)
    B = col1.number_input(
        "Presupuesto global B ($MXN)",
        min_value=0.0,
        value=float(DEFAULT_B),
        step=1000.0,
        format="%.2f",
    )
    demand_val = col2.number_input(
        "Demanda (porciones / tiempo de comida)",
        min_value=1,
        value=DEFAULT_DEMAND,
        step=1,
    )

# ──────────────────────────────────────────────────────────────────────────────
# COSTOS UNITARIOS
# ──────────────────────────────────────────────────────────────────────────────

with st.expander("Costos unitarios ($ MXN por unidad)"):
    cost_df = pd.DataFrame(
        [
            {"ID": i, "Insumo": INSUMO_NAMES[i], "Costo ($MXN)": DEFAULT_COST[i]}
            for i in range(1, 31)
        ]
    )
    edited_cost = st.data_editor(
        cost_df,
        column_config={
            "ID": st.column_config.NumberColumn("ID", disabled=True, width="small"),
            "Insumo": st.column_config.TextColumn("Insumo", disabled=True),
            "Costo ($MXN)": st.column_config.NumberColumn(
                "Costo ($MXN)", min_value=0.0, format="%.2f"
            ),
        },
        hide_index=True,
        use_container_width=True,
        key="cost_editor",
    )

# ──────────────────────────────────────────────────────────────────────────────
# INVENTARIO INICIAL
# ──────────────────────────────────────────────────────────────────────────────

with st.expander("Inventario inicial (unidades)"):
    inv_df = pd.DataFrame(
        [
            {"ID": i, "Insumo": INSUMO_NAMES[i], "Inventario inicial": DEFAULT_INITIAL_INV[i]}
            for i in range(1, 31)
        ]
    )
    edited_inv = st.data_editor(
        inv_df,
        column_config={
            "ID": st.column_config.NumberColumn("ID", disabled=True, width="small"),
            "Insumo": st.column_config.TextColumn("Insumo", disabled=True),
            "Inventario inicial": st.column_config.NumberColumn(
                "Inventario inicial", min_value=0.0, format="%.2f"
            ),
        },
        hide_index=True,
        use_container_width=True,
        key="inv_editor",
    )

# ──────────────────────────────────────────────────────────────────────────────
# DONACIONES
# ──────────────────────────────────────────────────────────────────────────────

with st.expander("Donaciones"):
    don_rows = [
        {
            "Insumo (ID)": i,
            "Día (1–7)": t,
            "Cantidad": v,
        }
        for (i, t), v in DEFAULT_DONATIONS.items()
    ]
    don_df = pd.DataFrame(don_rows) if don_rows else pd.DataFrame(
        columns=["Insumo (ID)", "Día (1–7)", "Cantidad"]
    )
    edited_don = st.data_editor(
        don_df,
        column_config={
            "Insumo (ID)": st.column_config.NumberColumn("Insumo (ID)", min_value=1, max_value=30),
            "Día (1–7)": st.column_config.NumberColumn("Día (1–7)", min_value=1, max_value=7),
            "Cantidad": st.column_config.NumberColumn("Cantidad", min_value=0.0, format="%.2f"),
        },
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        key="don_editor",
    )

# ──────────────────────────────────────────────────────────────────────────────
# TAMAÑOS DE LOTE
# ──────────────────────────────────────────────────────────────────────────────

with st.expander("Tamaños de lote"):
    lot_df = pd.DataFrame(
        [
            {"ID": i, "Insumo": INSUMO_NAMES[i], "Tamaño de lote": DEFAULT_LOT_SIZE[i]}
            for i in range(1, 31)
        ]
    )
    edited_lot = st.data_editor(
        lot_df,
        column_config={
            "ID": st.column_config.NumberColumn("ID", disabled=True, width="small"),
            "Insumo": st.column_config.TextColumn("Insumo", disabled=True),
            "Tamaño de lote": st.column_config.NumberColumn(
                "Tamaño de lote", min_value=1, step=1
            ),
        },
        hide_index=True,
        use_container_width=True,
        key="lot_editor",
    )

# ──────────────────────────────────────────────────────────────────────────────
# CALENDARIO DE COMIDAS  (3 tiempos × 7 días)
# ──────────────────────────────────────────────────────────────────────────────

# Mapa inverso: para cada (día, tiempo_comida) → platillo por defecto
_default_dish_for = {}
for (m, t), c in DEFAULT_SCHEDULE.items():
    _default_dish_for[(t, c)] = m

dish_options = list(DISH_NAMES.values())  # 12 opciones
dish_id_from_name = {v: k for k, v in DISH_NAMES.items()}

with st.expander("Calendario de comidas (platillo por día y tiempo)", expanded=True):
    # Cabecera de días
    header_cols = st.columns([2] + [1] * 7)
    header_cols[0].markdown("**Tiempo / Día**")
    for t in range(1, 8):
        header_cols[t].markdown(f"**{DAY_NAMES[t]}**")

    for c in range(1, 4):
        row_cols = st.columns([2] + [1] * 7)
        row_cols[0].write(MEAL_NAMES[c])
        for t in range(1, 8):
            default_m = _default_dish_for.get((t, c), 1)
            default_name = DISH_NAMES[default_m]
            row_cols[t].selectbox(
                label="",
                options=dish_options,
                index=dish_options.index(default_name),
                key=f"sched_{t}_{c}",
                label_visibility="collapsed",
            )

# ──────────────────────────────────────────────────────────────────────────────
# RECOLECCIÓN DE PARÁMETROS Y VALIDACIÓN
# ──────────────────────────────────────────────────────────────────────────────

st.divider()

def _build_report_text(res: dict) -> str:
    """Genera el reporte de resultados como texto plano (para descarga)."""
    lines = []

    def w(line=""):
        lines.append(line)

    w("=" * 70)
    w("  MILP – Optimización de Flujos Alimentarios en Casa Monarca")
    w("=" * 70)
    w(f"  Estado del solver   : {res['status']}")
    w(f"  Condición de término: {res['termination']}")

    total_cost = res["total_cost"]
    B = res["B"]
    w(f"  Costo total óptimo  : $ {total_cost:,.2f} MXN")
    w("=" * 70)

    # Plan de comidas
    w("\n" + "─" * 70)
    w("  PLAN DE COMIDAS (porciones preparadas)")
    w("─" * 70)
    z_vals = res["z_vals"]
    for t in range(1, 8):
        w(f"\n  {DAY_NAMES[t]}")
        for c in range(1, 4):
            w(f"    {MEAL_NAMES[c]}:")
            any_dish = False
            for m in range(1, 13):
                val = z_vals.get((m, t, c))
                if val is not None and val > 0.5:
                    from milp_model_core import DISH_NAMES as _DISH
                    w(f"      {_DISH[m]}: {int(round(val))} porciones")
                    any_dish = True
            if not any_dish:
                w("      (ninguno)")

    # Compras diarias
    w("\n" + "─" * 70)
    w("  COMPRAS DIARIAS")
    w("─" * 70)
    x_vals = res["x_vals"]
    y_vals = res["y_vals"]
    cost = res["cost"]
    daily_costs = res["daily_costs"]
    for t in range(1, 8):
        day_cost = daily_costs.get(t, 0.0)
        w(f"\n  {DAY_NAMES[t]}  (gasto: $ {day_cost:,.2f} MXN)")
        purchases = [
            (i, x_vals[i, t], y_vals.get((i, t), 0), cost[i] * x_vals[i, t])
            for i in range(1, 31)
            if x_vals.get((i, t)) and x_vals[i, t] > 1e-6
        ]
        if purchases:
            w(f"    {'Insumo':<30s} {'Cantidad':>10s}  {'Lotes':>6s}  {'Costo ($MXN)':>13s}")
            w("    " + "-" * 64)
            for i, xval, yval, spend in purchases:
                w(f"    {INSUMO_NAMES[i]:<30s} {xval:>10.2f}  {int(round(yval)) if yval else 0:>6d}  {spend:>13,.2f}")
        else:
            w("    (sin compras este día)")

    # Inventario
    w("\n" + "─" * 70)
    w("  INVENTARIO AL FINAL DE CADA DÍA")
    w("─" * 70)
    mu_vals = res["mu_vals"]
    w(f"\n  {'Insumo':<30s}" + "".join(f"  {DAY_NAMES[t]:>10s}" for t in range(1, 8)))
    w("  " + "-" * (30 + 12 * 7))
    for i in range(1, 31):
        row_vals = [mu_vals.get((i, t)) or 0.0 for t in range(1, 8)]
        if any(v > 1e-6 for v in row_vals):
            row = f"  {INSUMO_NAMES[i]:<30s}" + "".join(f"  {v:>10.2f}" for v in row_vals)
            w(row)

    # Consumo interno
    w("\n" + "─" * 70)
    w("  CONSUMO INTERNO DIARIO")
    w("─" * 70)
    gamma_vals = res["gamma_vals"]
    w(f"\n  {'Insumo':<30s}" + "".join(f"  {DAY_NAMES[t]:>10s}" for t in range(1, 8)))
    w("  " + "-" * (30 + 12 * 7))
    for i in range(1, 31):
        row_vals = [gamma_vals.get((i, t)) or 0.0 for t in range(1, 8)]
        if any(v > 1e-6 for v in row_vals):
            row = f"  {INSUMO_NAMES[i]:<30s}" + "".join(f"  {v:>10.3f}" for v in row_vals)
            w(row)

    # Resumen de costos
    w("\n" + "─" * 70)
    w("  RESUMEN DE COSTOS")
    w("─" * 70)
    for t in range(1, 8):
        w(f"  {DAY_NAMES[t]:<12s}: $ {daily_costs.get(t, 0.0):>10,.2f} MXN")
    w("  " + "-" * 30)
    w(f"  {'TOTAL':<12s}: $ {total_cost:>10,.2f} MXN")
    w(f"  Presupuesto   : $ {B:>10,.2f} MXN")
    w(f"  Remanente     : $ {B - total_cost:>10,.2f} MXN")
    w("=" * 70)

    return "\n".join(lines)


def collect_params():
    """Lee los widgets y devuelve el dict params para solve_milp."""
    # Costos
    cost = {
        int(row["ID"]): float(row["Costo ($MXN)"])
        for _, row in edited_cost.iterrows()
    }
    # Inventario inicial
    initial_inv = {
        int(row["ID"]): float(row["Inventario inicial"])
        for _, row in edited_inv.iterrows()
    }
    # Lotes
    lot_size = {
        int(row["ID"]): int(row["Tamaño de lote"])
        for _, row in edited_lot.iterrows()
    }
    # Donaciones
    donations = {}
    for _, row in edited_don.iterrows():
        i = int(row["Insumo (ID)"])
        t = int(row["Día (1–7)"])
        v = float(row["Cantidad"])
        donations[(i, t)] = v
    # Calendario
    schedule = {}
    for c in range(1, 4):
        for t in range(1, 8):
            dish_name = st.session_state.get(f"sched_{t}_{c}", dish_options[0])
            m = dish_id_from_name[dish_name]
            schedule[(m, t)] = c

    return {
        "cost": cost,
        "lot_size": lot_size,
        "B": B,
        "demand": demand_val,
        "initial_inv": initial_inv,
        "donations": donations,
        "schedule": schedule,
    }


def validate_params(params):
    """Devuelve lista de mensajes de error (vacía = ok)."""
    errors = []
    # Costos no negativos
    for i, v in params["cost"].items():
        if v < 0:
            errors.append(f"Costo del insumo {INSUMO_NAMES[i]} es negativo.")
    # Inventarios no negativos
    for i, v in params["initial_inv"].items():
        if v < 0:
            errors.append(f"Inventario inicial del insumo {INSUMO_NAMES[i]} es negativo.")
    # Cada día debe tener exactamente un platillo por tiempo de comida
    schedule = params["schedule"]
    for t in range(1, 8):
        for c in range(1, 4):
            assigned = [(m, tc) for (m, tc), tc2 in schedule.items() if tc == t and tc2 == c]
            # schedule[(m,t)] = c, so check how many m map to (t, c)
    # Verificar que cada (t, c) tiene exactamente un platillo
    slot_count = {}
    for (m, t), c in schedule.items():
        key = (t, c)
        slot_count[key] = slot_count.get(key, 0) + 1
    for (t, c), cnt in slot_count.items():
        if cnt > 1:
            errors.append(
                f"{DAY_NAMES[t]} – {MEAL_NAMES[c]}: asignados {cnt} platillos (máximo 1)."
            )
    return errors


# ── Botón principal ───────────────────────────────────────────────────────────

if st.button("Resolver modelo MILP", type="primary", use_container_width=True):
    params = collect_params()
    errors = validate_params(params)

    if errors:
        for msg in errors:
            st.error(msg)
    else:
        try:
            with st.spinner("Resolviendo con GLPK…"):
                res = solve_milp(params)
            st.session_state["results"] = res
        except RuntimeError as e:
            st.error(str(e))

# ──────────────────────────────────────────────────────────────────────────────
# RESULTADOS
# ──────────────────────────────────────────────────────────────────────────────

if "results" in st.session_state:
    res = st.session_state["results"]

    st.divider()
    st.subheader("Resultados")

    # ── Métricas de resumen ───────────────────────────────────────────────────
    term = res["termination"]
    status_display = "Óptimo" if term == "optimal" else term

    m1, m2, m3 = st.columns(3)
    m1.metric("Estado", status_display)

    if res["total_cost"] is not None:
        m2.metric("Costo total", f"$ {res['total_cost']:,.2f} MXN")
        remanente = res["B"] - res["total_cost"]
        m3.metric("Remanente", f"$ {remanente:,.2f} MXN")
    else:
        st.warning("No se encontró solución óptima. Verifica los parámetros o el calendario.")

    # ── Tabs de resultados ────────────────────────────────────────────────────
    if res["total_cost"] is not None:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Plan de comidas", "Compras diarias", "Inventario", "Consumo interno", "Resumen de costos"]
        )

        with tab1:
            df_meal = make_meal_plan_df(res)
            st.dataframe(df_meal, use_container_width=True, hide_index=True)

        with tab2:
            df_purch = make_purchases_df(res)
            st.dataframe(df_purch, use_container_width=True, hide_index=True)
            df_costs = make_cost_summary_df(res)
            if not df_costs.empty:
                st.bar_chart(
                    df_costs.set_index("Día")["Gasto ($MXN)"],
                    use_container_width=True,
                )

        with tab3:
            df_inv = make_inventory_df(res)
            st.dataframe(df_inv, use_container_width=True, hide_index=True)

        with tab4:
            df_cons = make_consumption_df(res)
            st.dataframe(df_cons, use_container_width=True, hide_index=True)

        with tab5:
            df_summary = make_cost_summary_df(res)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)

        st.divider()
        txt_content = _build_report_text(res)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Descargar resultados (.txt)",
            data=txt_content,
            file_name=f"resultados_{timestamp}.txt",
            mime="text/plain",
            use_container_width=True,
        )
