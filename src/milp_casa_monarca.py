"""
MILP – Optimización de Flujos Alimentarios en Casa Monarca
==========================================================
Minimiza el costo total de adquisición de insumos durante una semana (7 días,
3 tiempos de comida) cubriendo la demanda de 100 porciones diarias.

Solver requerido: GLPK  (pip install glpk  o  brew install glpk)
Ejecutar desde la raíz del proyecto:
    python src/milp_casa_monarca.py
"""

import os
import pyomo.environ as pyo
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# DATOS
# ──────────────────────────────────────────────────────────────────────────────

insumo_names = {
    1: "Arroz (kg)",
    2: "Frijol (kg)",
    3: "Tortilla (kg)",
    4: "Tomate (kg)",
    5: "Cebolla (kg)",
    6: "Papa (kg)",
    7: "Zanahoria (kg)",
    8: "Espinaca (kg)",
    9: "Champiñones (kg)",
    10: "Cilantro (kg)",
    11: "Lechuga (pz)",
    12: "Pasta (paq)",
    13: "Chile (kg)",
    14: "Aceite (L)",
    15: "Huevo (unidad)",
    16: "Sal (kg)",
    17: "Leche (L)",
    18: "Café (kg)",
    19: "Agua (L)",
    20: "Azúcar (kg)",
    21: "Galletas (paq)",
    22: "Pasteles (pz)",
    23: "Pan (pz)",
    24: "Atún (lata)",
    25: "Pollo (kg)",
    26: "Res (kg)",
    27: "Refrescos (L)",
    28: "Saborizantes (sobres)",
    29: "Harina Maseca (kg)",
    30: "Cereal (caja)",
}

dish_names = {
    1: "Huevo con chorizo",
    2: "Huevo estrellado",
    3: "Huevo con jamón",
    4: "Tortas jamón/queso",
    5: "Huevo con papa",
    6: "Cereal con leche",
    7: "Huevo/salchicha",
    8: "Ensalada de atún",
    9: "Pollo frito/pasta",
    10: "Sándwich de pavo",
    11: "Milanesa de res",
    12: "Guiso de res",
}

day_names = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo",
}
meal_names = {1: "Desayuno", 2: "Comida", 3: "Cena"}

# Costo unitario c_i  ($ MXN)
cost = {
    1: 25.00,
    2: 38.00,
    3: 25.00,
    4: 30.00,
    5: 25.00,
    6: 35.00,
    7: 20.00,
    8: 30.00,
    9: 90.00,
    10: 50.00,
    11: 20.00,
    12: 10.00,
    13: 40.00,
    14: 38.00,
    15: 2.83,
    16: 20.00,
    17: 28.00,
    18: 150.00,
    19: 2.50,
    20: 35.00,
    21: 15.00,
    22: 100.00,
    23: 3.00,
    24: 20.00,
    25: 68.00,
    26: 180.00,
    27: 15.00,
    28: 5.00,
    29: 22.00,
    30: 60.00,
}

# Tamaño de lote ℓ_i  (todos = 1, salvo Huevo = 30)
lot_size = {i: 1 for i in range(1, 31)}
lot_size[15] = 30

# Presupuesto global
B = 50_000.0

# Demanda d_{t,c} = 100 porciones para todo t, c
demand = {(t, c): 100 for t in range(1, 8) for c in range(1, 4)}

# Inventario inicial I_{i,0}
initial_inv = {i: 0.0 for i in range(1, 31)}
initial_inv.update(
    {
        1: 100,
        2: 330,
        8: 0,
        12: 300,
        13: 0,
        14: 92,
        17: 7.5,
        20: 156,
        21: 35,
        24: 69,
        29: 100,
    }
)

# Donaciones δ_{i,t}  (solo t=1)
donation = {(i, t): 0.0 for i in range(1, 31) for t in range(1, 8)}
donation[1, 1] = 50.0
donation[2, 1] = 50.0

# Calendario α_{m,t,c}  – tensor binario
# Entrada: (platillo, día) → comida
_schedule = {
    (1, 1): 1,
    (9, 1): 2,
    (10, 1): 3,  # Lunes
    (5, 2): 1,
    (12, 2): 2,
    (4, 2): 3,  # Martes
    (2, 3): 1,
    (11, 3): 2,
    (8, 3): 3,  # Miércoles
    (3, 4): 1,
    (9, 4): 2,
    (10, 4): 3,  # Jueves
    (7, 5): 1,
    (12, 5): 2,
    (4, 5): 3,  # Viernes
    (6, 6): 1,
    (8, 6): 2,
    (10, 6): 3,  # Sábado
    (1, 7): 1,
    (11, 7): 2,
    (4, 7): 3,  # Domingo
}
alpha = {(m, t, c): 0 for m in range(1, 13) for t in range(1, 8) for c in range(1, 4)}
for (m, t), c in _schedule.items():
    alpha[m, t, c] = 1

# Coeficientes técnicos a_{i,m}  (insumo i por porción de platillo m)
a = {(i, m): 0.0 for i in range(1, 31) for m in range(1, 13)}
_tech = {
    # 1: Huevo con chorizo
    (15, 1): 1.2,
    (2, 1): 0.03,
    (3, 1): 0.18,
    (14, 1): 0.01,
    (18, 1): 0.005,
    # 2: Huevo estrellado
    (15, 2): 1.2,
    (2, 2): 0.03,
    (23, 2): 1.0,
    (14, 2): 0.01,
    (18, 2): 0.005,
    # 3: Huevo con jamón
    (15, 3): 1.2,
    (2, 3): 0.03,
    (3, 3): 0.18,
    (14, 3): 0.01,
    (18, 3): 0.005,
    # 4: Tortas jamón/queso
    (23, 4): 1.0,
    (4, 4): 0.02,
    (5, 4): 0.01,
    (15, 4): 0.5,
    (18, 4): 0.005,
    # 5: Huevo con papa
    (15, 5): 1.2,
    (6, 5): 0.05,
    (2, 5): 0.03,
    (3, 5): 0.18,
    (14, 5): 0.01,
    (18, 5): 0.005,
    # 6: Cereal con leche
    (30, 6): 0.08,
    (17, 6): 0.25,
    (18, 6): 0.005,
    # 7: Huevo/salchicha
    (15, 7): 1.2,
    (2, 7): 0.03,
    (3, 7): 0.18,
    (14, 7): 0.01,
    (18, 7): 0.005,
    # 8: Ensalada de atún
    (24, 8): 0.5,
    (11, 8): 0.05,
    (4, 8): 0.02,
    (21, 8): 0.10,
    # 9: Pollo frito/pasta
    (25, 9): 0.12,
    (12, 9): 0.06,
    (4, 9): 0.03,
    (14, 9): 0.015,
    (19, 9): 0.4,
    # 10: Sándwich de pavo
    (23, 10): 2.0,
    (4, 10): 0.02,
    (5, 10): 0.01,
    (6, 10): 0.04,
    (7, 10): 0.03,
    (19, 10): 0.4,
    # 11: Milanesa de res
    (26, 11): 0.10,
    (14, 11): 0.015,
    (3, 11): 0.15,
    (19, 11): 0.4,
    # 12: Guiso de res
    (26, 12): 0.10,
    (6, 12): 0.04,
    (4, 12): 0.03,
    (3, 12): 0.15,
    (19, 12): 0.4,
}
for k, v in _tech.items():
    a[k] = v

BIG_M = 150  # constante Big-M para el filtro de calendario

# ──────────────────────────────────────────────────────────────────────────────
# MODELO PYOMO
# ──────────────────────────────────────────────────────────────────────────────

model = pyo.ConcreteModel(name="CasaMonarca_MILP")

# Conjuntos
model.I = pyo.Set(initialize=range(1, 31))  # Insumos
model.T = pyo.Set(initialize=range(1, 8))  # Días
model.C = pyo.Set(initialize=range(1, 4))  # Tiempos de comida
model.M = pyo.Set(initialize=range(1, 13))  # Platillos

# Parámetros
model.c_cost = pyo.Param(model.I, initialize=cost)
model.l = pyo.Param(model.I, initialize=lot_size)
model.B = pyo.Param(initialize=B)
model.d = pyo.Param(model.T, model.C, initialize=demand)
model.I0 = pyo.Param(model.I, initialize=initial_inv)
model.delta = pyo.Param(model.I, model.T, initialize=donation)
model.alpha = pyo.Param(model.M, model.T, model.C, initialize=alpha)
model.a = pyo.Param(model.I, model.M, initialize=a)

# Variables de decisión
model.z = pyo.Var(
    model.M, model.T, model.C, domain=pyo.NonNegativeIntegers
)  # porciones
model.y = pyo.Var(model.I, model.T, domain=pyo.NonNegativeIntegers)  # lotes
model.x = pyo.Var(model.I, model.T, domain=pyo.NonNegativeReals)  # compras netas
model.gamma = pyo.Var(model.I, model.T, domain=pyo.NonNegativeReals)  # consumo interno
model.mu = pyo.Var(model.I, model.T, domain=pyo.NonNegativeReals)  # inventario final

# ── Función objetivo ──────────────────────────────────────────────────────────
model.obj = pyo.Objective(
    expr=pyo.quicksum(
        model.c_cost[i] * model.x[i, t] for i in model.I for t in model.T
    ),
    sense=pyo.minimize,
)

# ── Restricciones ─────────────────────────────────────────────────────────────


# (8) Satisfacción de demanda
def demand_rule(mdl, t, c):
    return pyo.quicksum(mdl.z[m, t, c] for m in mdl.M) >= mdl.d[t, c]


model.demand_con = pyo.Constraint(model.T, model.C, rule=demand_rule)


# (9) Apego al calendario – Filtro Big-M
def calendar_rule(mdl, m, t, c):
    return mdl.z[m, t, c] <= BIG_M * mdl.alpha[m, t, c]


model.calendar_con = pyo.Constraint(model.M, model.T, model.C, rule=calendar_rule)


# (10) Relación menú → insumo (consumo interno)
def consumption_rule(mdl, i, t):
    return mdl.gamma[i, t] == pyo.quicksum(
        mdl.a[i, m] * mdl.z[m, t, c] for c in mdl.C for m in mdl.M
    )


model.consumption_con = pyo.Constraint(model.I, model.T, rule=consumption_rule)


# (11) Lotes de compra
def lots_rule(mdl, i, t):
    return mdl.x[i, t] == mdl.l[i] * mdl.y[i, t]


model.lots_con = pyo.Constraint(model.I, model.T, rule=lots_rule)

# (12) Límite presupuestal
model.budget_con = pyo.Constraint(
    expr=pyo.quicksum(model.c_cost[i] * model.x[i, t] for i in model.I for t in model.T)
    <= model.B
)


# (13) + (14) Inventario inicial + balance de inventario
def inventory_rule(mdl, i, t):
    prev = mdl.I0[i] if t == 1 else mdl.mu[i, t - 1]
    return mdl.mu[i, t] == prev + mdl.x[i, t] + mdl.delta[i, t] - mdl.gamma[i, t]


model.inventory_con = pyo.Constraint(model.I, model.T, rule=inventory_rule)


# (15) Condición de frontera terminal
def terminal_rule(mdl, i):
    return mdl.mu[i, 7] >= mdl.I0[i]


model.terminal_con = pyo.Constraint(model.I, rule=terminal_rule)

# ──────────────────────────────────────────────────────────────────────────────
# RESOLUCIÓN
# ──────────────────────────────────────────────────────────────────────────────

solver = pyo.SolverFactory("glpk")
if not solver.available():
    raise RuntimeError("GLPK no está disponible. Instálalo con: brew install glpk")

print("Resolviendo el modelo MILP...")
results = solver.solve(model, tee=True)

# ──────────────────────────────────────────────────────────────────────────────
# RESULTADOS → TXT
# ──────────────────────────────────────────────────────────────────────────────


timestap = datetime.now().strftime("%Y%m%d_%H%M%S")
outputname = f"results_{timestap}.txt"
directory = "./OUTPUT/"

status = results.solver.termination_condition
solver_stat = results.solver.status

# output_path = os.path.join(os.path.dirname(__file__), "resultados_milp.txt")

with open(directory + outputname, "w", encoding="utf-8") as f:

    def w(line=""):
        f.write(line + "\n")

    w("=" * 70)
    w("  MILP – Optimización de Flujos Alimentarios en Casa Monarca")
    w("=" * 70)
    w(f"  Estado del solver  : {solver_stat}")
    w(f"  Condición de término: {status}")

    if str(status) not in ("optimal", "feasible"):
        w("\n[!] No se encontró solución óptima. Revisar datos o solver.")
    else:
        total_cost = pyo.value(model.obj)
        w(f"  Costo total óptimo : $ {total_cost:,.2f} MXN")
        w("=" * 70)

        # ── Plan de comidas por día ──────────────────────────────────────────
        w("\n" + "─" * 70)
        w("  PLAN DE COMIDAS (porciones preparadas z_{m,t,c})")
        w("─" * 70)
        for t in model.T:
            w(f"\n  {day_names[t]}")
            for c in model.C:
                w(f"    {meal_names[c]}:")
                any_dish = False
                for m in model.M:
                    val = pyo.value(model.z[m, t, c])
                    if val is not None and val > 0.5:
                        w(
                            f"      Platillo {m:2d} ({dish_names[m]}): {int(round(val))} porciones"
                        )
                        any_dish = True
                if not any_dish:
                    w("      (ninguno)")

        # ── Compras por día ──────────────────────────────────────────────────
        w("\n" + "─" * 70)
        w("  COMPRAS DIARIAS (x_{i,t}  y  y_{i,t} lotes)")
        w("─" * 70)
        daily_costs = {}
        for t in model.T:
            purchases = []
            day_cost = 0.0
            for i in model.I:
                xval = pyo.value(model.x[i, t])
                yval = pyo.value(model.y[i, t])
                if xval is not None and xval > 1e-6:
                    spend = cost[i] * xval
                    day_cost += spend
                    purchases.append((i, xval, int(round(yval)), spend))
            daily_costs[t] = day_cost
            w(f"\n  {day_names[t]}  (gasto del día: $ {day_cost:,.2f} MXN)")
            if purchases:
                w(
                    f"    {'Insumo':<30s} {'Cantidad':>10s}  {'Lotes':>6s}  {'Costo ($MXN)':>13s}"
                )
                w("    " + "-" * 64)
                for i, xval, yval, spend in purchases:
                    w(
                        f"    {insumo_names[i]:<30s} {xval:>10.2f}  {yval:>6d}  {spend:>13,.2f}"
                    )
            else:
                w("    (sin compras este día)")

        # ── Inventario final por día ─────────────────────────────────────────
        w("\n" + "─" * 70)
        w("  INVENTARIO AL FINAL DE CADA DÍA (μ_{i,t})")
        w("─" * 70)
        w(f"\n  {'Insumo':<30s}" + "".join(f"  {day_names[t]:>10s}" for t in model.T))
        w("  " + "-" * (30 + 12 * 7))
        for i in model.I:
            row = f"  {insumo_names[i]:<30s}"
            has_nonzero = False
            for t in model.T:
                val = pyo.value(model.mu[i, t])
                val = val if val is not None else 0.0
                row += f"  {val:>10.2f}"
                if val > 1e-6:
                    has_nonzero = True
            if has_nonzero or initial_inv.get(i, 0) > 0:
                w(row)

        # ── Consumo interno por día ──────────────────────────────────────────
        w("\n" + "─" * 70)
        w("  CONSUMO INTERNO DIARIO (γ_{i,t})")
        w("─" * 70)
        w(f"\n  {'Insumo':<30s}" + "".join(f"  {day_names[t]:>10s}" for t in model.T))
        w("  " + "-" * (30 + 12 * 7))
        for i in model.I:
            row = f"  {insumo_names[i]:<30s}"
            has_nonzero = False
            for t in model.T:
                val = pyo.value(model.gamma[i, t])
                val = val if val is not None else 0.0
                row += f"  {val:>10.3f}"
                if val > 1e-6:
                    has_nonzero = True
            if has_nonzero:
                w(row)

        # ── Resumen de costos ────────────────────────────────────────────────
        w("\n" + "─" * 70)
        w("  RESUMEN DE COSTOS")
        w("─" * 70)
        for t in model.T:
            w(f"  {day_names[t]:<12s}: $ {daily_costs[t]:>10,.2f} MXN")
        w("  " + "-" * 30)
        w(f"  {'TOTAL':<12s}: $ {total_cost:>10,.2f} MXN")
        w(f"  Presupuesto   : $ {B:>10,.2f} MXN")
        w(f"  Remanente     : $ {B - total_cost:>10,.2f} MXN")
        w("=" * 70)

# print(f"\nResultados escritos en: {output_path}")
