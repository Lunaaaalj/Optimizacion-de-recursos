"""
result_tables.py – Conversión de resultados del MILP a DataFrames de pandas
============================================================================
"""

import pandas as pd
from milp_model_core import DAY_NAMES, DISH_NAMES, INSUMO_NAMES, MEAL_NAMES


def make_meal_plan_df(results: dict) -> pd.DataFrame:
    """Plan de comidas: Dia | Tiempo | Platillo | Porciones (long format)."""
    z_vals = results["z_vals"]
    rows = []
    for (m, t, c), val in z_vals.items():
        if val is not None and val > 0.5:
            rows.append(
                {
                    "Día": DAY_NAMES[t],
                    "Tiempo": MEAL_NAMES[c],
                    "Platillo": DISH_NAMES[m],
                    "Porciones": int(round(val)),
                }
            )
    if not rows:
        return pd.DataFrame(columns=["Día", "Tiempo", "Platillo", "Porciones"])
    df = pd.DataFrame(rows)
    # Orden lógico: día → tiempo → platillo
    day_order = list(DAY_NAMES.values())
    meal_order = list(MEAL_NAMES.values())
    df["Día"] = pd.Categorical(df["Día"], categories=day_order, ordered=True)
    df["Tiempo"] = pd.Categorical(df["Tiempo"], categories=meal_order, ordered=True)
    return df.sort_values(["Día", "Tiempo"]).reset_index(drop=True)


def make_purchases_df(results: dict) -> pd.DataFrame:
    """Compras diarias: Día | Insumo | Cantidad | Lotes | Costo (long format)."""
    x_vals = results["x_vals"]
    y_vals = results["y_vals"]
    cost = results["cost"]
    rows = []
    for (i, t), xval in x_vals.items():
        if xval is not None and xval > 1e-6:
            yval = y_vals.get((i, t), 0)
            spend = cost[i] * xval
            rows.append(
                {
                    "Día": DAY_NAMES[t],
                    "Insumo": INSUMO_NAMES[i],
                    "Cantidad": round(xval, 4),
                    "Lotes": int(round(yval)) if yval is not None else 0,
                    "Costo ($MXN)": round(spend, 2),
                }
            )
    if not rows:
        return pd.DataFrame(columns=["Día", "Insumo", "Cantidad", "Lotes", "Costo ($MXN)"])
    df = pd.DataFrame(rows)
    day_order = list(DAY_NAMES.values())
    df["Día"] = pd.Categorical(df["Día"], categories=day_order, ordered=True)
    return df.sort_values(["Día", "Insumo"]).reset_index(drop=True)


def make_inventory_df(results: dict) -> pd.DataFrame:
    """Inventario al final de cada día: Insumo × Día (wide format)."""
    mu_vals = results["mu_vals"]
    rows = {}
    for (i, t), val in mu_vals.items():
        name = INSUMO_NAMES[i]
        day = DAY_NAMES[t]
        if name not in rows:
            rows[name] = {}
        rows[name][day] = round(val, 4) if val is not None else 0.0

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows).T
    df.index.name = "Insumo"
    # Ordenar columnas por día
    day_cols = [DAY_NAMES[t] for t in range(1, 8) if DAY_NAMES[t] in df.columns]
    df = df[day_cols]
    # Mostrar solo filas con algún valor distinto de cero
    df = df[(df > 1e-6).any(axis=1)]
    return df.reset_index()


def make_consumption_df(results: dict) -> pd.DataFrame:
    """Consumo interno diario: Insumo × Día (wide format)."""
    gamma_vals = results["gamma_vals"]
    rows = {}
    for (i, t), val in gamma_vals.items():
        name = INSUMO_NAMES[i]
        day = DAY_NAMES[t]
        if name not in rows:
            rows[name] = {}
        rows[name][day] = round(val, 4) if val is not None else 0.0

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows).T
    df.index.name = "Insumo"
    day_cols = [DAY_NAMES[t] for t in range(1, 8) if DAY_NAMES[t] in df.columns]
    df = df[day_cols]
    df = df[(df > 1e-6).any(axis=1)]
    return df.reset_index()


def make_cost_summary_df(results: dict) -> pd.DataFrame:
    """Resumen de costos: Día | Gasto | Acumulado."""
    daily_costs = results["daily_costs"]
    rows = []
    acum = 0.0
    for t in range(1, 8):
        gasto = daily_costs.get(t, 0.0)
        acum += gasto
        rows.append(
            {
                "Día": DAY_NAMES[t],
                "Gasto ($MXN)": round(gasto, 2),
                "Acumulado ($MXN)": round(acum, 2),
            }
        )
    return pd.DataFrame(rows)
