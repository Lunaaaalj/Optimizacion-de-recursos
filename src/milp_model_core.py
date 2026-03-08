"""
milp_model_core.py – Núcleo del modelo MILP para Casa Monarca
=============================================================
Exporta DEFAULT_* constants y solve_milp(params) para ser usados
tanto por la GUI de Streamlit como por otros módulos.
"""

import pyomo.environ as pyo

# ──────────────────────────────────────────────────────────────────────────────
# METADATOS (nombres de índices)
# ──────────────────────────────────────────────────────────────────────────────

INSUMO_NAMES = {
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

DISH_NAMES = {
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

DAY_NAMES = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo",
}

MEAL_NAMES = {1: "Desayuno", 2: "Comida", 3: "Cena"}

# ──────────────────────────────────────────────────────────────────────────────
# PARÁMETROS POR DEFECTO
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_COST = {
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

DEFAULT_LOT_SIZE = {i: 1 for i in range(1, 31)}
DEFAULT_LOT_SIZE[15] = 30

DEFAULT_B = 50_000.0

DEFAULT_DEMAND = 100  # porciones por tiempo de comida (uniforme)

DEFAULT_INITIAL_INV = {i: 0.0 for i in range(1, 31)}
DEFAULT_INITIAL_INV.update(
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

# Donaciones: {(insumo, día): cantidad}
DEFAULT_DONATIONS = {(1, 1): 50.0, (2, 1): 50.0}

# Calendario: {(platillo, día): tiempo_comida}  – 21 entradas (3 por día × 7 días)
DEFAULT_SCHEDULE = {
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

# Coeficientes técnicos a_{i,m}: insumo i por porción de platillo m (fijo)
_TECH = {
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

BIG_M = 150  # constante Big-M para el filtro de calendario


# ──────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────


def solve_milp(params: dict) -> dict:
    """Construye y resuelve el MILP de Casa Monarca.

    Parameters
    ----------
    params : dict
        Claves opcionales (todas caen en defaults si se omiten):
          cost        – dict {i: float}
          lot_size    – dict {i: int}
          B           – float  (presupuesto global)
          demand      – int    (porciones uniformes por tiempo de comida)
          initial_inv – dict {i: float}
          donations   – dict {(i, t): float}
          schedule    – dict {(m, t): c}  (21 entradas)

    Returns
    -------
    dict con claves:
        status, termination, total_cost, B,
        z_vals, x_vals, y_vals, gamma_vals, mu_vals,
        daily_costs, cost
    """
    # ── Combinar con defaults ─────────────────────────────────────────────────
    cost = params.get("cost", DEFAULT_COST)
    lot_size = params.get("lot_size", DEFAULT_LOT_SIZE)
    B = float(params.get("B", DEFAULT_B))
    demand_val = int(params.get("demand", DEFAULT_DEMAND))
    initial_inv = params.get("initial_inv", DEFAULT_INITIAL_INV)
    donations_raw = params.get("donations", DEFAULT_DONATIONS)
    schedule_raw = params.get("schedule", DEFAULT_SCHEDULE)

    # ── Expandir donaciones al tensor completo ────────────────────────────────
    donation = {(i, t): 0.0 for i in range(1, 31) for t in range(1, 8)}
    for (i, t), v in donations_raw.items():
        donation[i, t] = float(v)

    # ── Construir tensor alpha desde schedule compacto ────────────────────────
    alpha = {
        (m, t, c): 0 for m in range(1, 13) for t in range(1, 8) for c in range(1, 4)
    }
    for (m, t), c in schedule_raw.items():
        alpha[m, t, c] = 1

    # ── Demanda uniforme ──────────────────────────────────────────────────────
    demand = {(t, c): demand_val for t in range(1, 8) for c in range(1, 4)}

    # ── Coeficientes técnicos ─────────────────────────────────────────────────
    a = {(i, m): 0.0 for i in range(1, 31) for m in range(1, 13)}
    for k, v in _TECH.items():
        a[k] = v

    # ── Modelo Pyomo ──────────────────────────────────────────────────────────
    model = pyo.ConcreteModel(name="CasaMonarca_MILP")

    model.I = pyo.Set(initialize=range(1, 31))
    model.T = pyo.Set(initialize=range(1, 8))
    model.C = pyo.Set(initialize=range(1, 4))
    model.M = pyo.Set(initialize=range(1, 13))

    model.c_cost = pyo.Param(model.I, initialize=cost)
    model.l = pyo.Param(model.I, initialize=lot_size)
    model.B = pyo.Param(initialize=B)
    model.d = pyo.Param(model.T, model.C, initialize=demand)
    model.I0 = pyo.Param(model.I, initialize=initial_inv)
    model.delta = pyo.Param(model.I, model.T, initialize=donation)
    model.alpha = pyo.Param(model.M, model.T, model.C, initialize=alpha)
    model.a = pyo.Param(model.I, model.M, initialize=a)

    model.z = pyo.Var(model.M, model.T, model.C, domain=pyo.NonNegativeIntegers)
    model.y = pyo.Var(model.I, model.T, domain=pyo.NonNegativeIntegers)
    model.x = pyo.Var(model.I, model.T, domain=pyo.NonNegativeReals)
    model.gamma = pyo.Var(model.I, model.T, domain=pyo.NonNegativeReals)
    model.mu = pyo.Var(model.I, model.T, domain=pyo.NonNegativeReals)

    model.obj = pyo.Objective(
        expr=pyo.quicksum(
            model.c_cost[i] * model.x[i, t] for i in model.I for t in model.T
        ),
        sense=pyo.minimize,
    )

    def demand_rule(mdl, t, c):
        return pyo.quicksum(mdl.z[m, t, c] for m in mdl.M) >= mdl.d[t, c]

    model.demand_con = pyo.Constraint(model.T, model.C, rule=demand_rule)

    def calendar_rule(mdl, m, t, c):
        return mdl.z[m, t, c] <= BIG_M * mdl.alpha[m, t, c]

    model.calendar_con = pyo.Constraint(model.M, model.T, model.C, rule=calendar_rule)

    def consumption_rule(mdl, i, t):
        return mdl.gamma[i, t] == pyo.quicksum(
            mdl.a[i, m] * mdl.z[m, t, c] for c in mdl.C for m in mdl.M
        )

    model.consumption_con = pyo.Constraint(model.I, model.T, rule=consumption_rule)

    def lots_rule(mdl, i, t):
        return mdl.x[i, t] == mdl.l[i] * mdl.y[i, t]

    model.lots_con = pyo.Constraint(model.I, model.T, rule=lots_rule)

    model.budget_con = pyo.Constraint(
        expr=pyo.quicksum(
            model.c_cost[i] * model.x[i, t] for i in model.I for t in model.T
        )
        <= model.B
    )

    def inventory_rule(mdl, i, t):
        prev = mdl.I0[i] if t == 1 else mdl.mu[i, t - 1]
        return mdl.mu[i, t] == prev + mdl.x[i, t] + mdl.delta[i, t] - mdl.gamma[i, t]

    model.inventory_con = pyo.Constraint(model.I, model.T, rule=inventory_rule)

    def terminal_rule(mdl, i):
        return mdl.mu[i, 7] >= mdl.I0[i]

    model.terminal_con = pyo.Constraint(model.I, rule=terminal_rule)

    # ── Resolución ────────────────────────────────────────────────────────────
    solver = pyo.SolverFactory("glpk")
    if not solver.available():
        raise RuntimeError("GLPK no está disponible. Instálalo con: brew install glpk")

    res = solver.solve(model, tee=False)

    termination = str(res.solver.termination_condition)
    status = str(res.solver.status)

    if termination not in ("optimal", "feasible"):
        return {
            "status": status,
            "termination": termination,
            "total_cost": None,
            "B": B,
            "z_vals": {},
            "x_vals": {},
            "y_vals": {},
            "gamma_vals": {},
            "mu_vals": {},
            "daily_costs": {},
            "cost": cost,
        }

    # ── Extracción de resultados ──────────────────────────────────────────────
    total_cost = pyo.value(model.obj)

    z_vals = {
        (m, t, c): pyo.value(model.z[m, t, c])
        for m in model.M
        for t in model.T
        for c in model.C
    }
    x_vals = {
        (i, t): pyo.value(model.x[i, t]) for i in model.I for t in model.T
    }
    y_vals = {
        (i, t): pyo.value(model.y[i, t]) for i in model.I for t in model.T
    }
    gamma_vals = {
        (i, t): pyo.value(model.gamma[i, t]) for i in model.I for t in model.T
    }
    mu_vals = {
        (i, t): pyo.value(model.mu[i, t]) for i in model.I for t in model.T
    }

    daily_costs = {}
    for t in range(1, 8):
        daily_costs[t] = sum(
            cost[i] * (x_vals[i, t] or 0.0) for i in range(1, 31)
        )

    return {
        "status": status,
        "termination": termination,
        "total_cost": total_cost,
        "B": B,
        "z_vals": z_vals,
        "x_vals": x_vals,
        "y_vals": y_vals,
        "gamma_vals": gamma_vals,
        "mu_vals": mu_vals,
        "daily_costs": daily_costs,
        "cost": cost,
    }
