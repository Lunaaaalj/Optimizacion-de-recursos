# Notación Matemática - Referencia Rápida

## Conjuntos (Sets)
| Símbolo | Descripción | Tamaño |
|---------|-------------|--------|
| $I$ | Insumos (ingredientes) | 30 |
| $T$ | Periodos de tiempo (días) | 7 |
| $C$ | Comidas del día | 3 |
| $M$ | Menú disponible (platos) | 12 |

---

## Parámetros (Constantes)

### Económicos
| Símbolo | Nombre | Tipo | Descripción |
|---------|--------|------|-------------|
| $\mathbf{c}$ | Costos | $\mathbb{R}^{\|I\|}$ | Vector de precios unitarios por insumo |
| $c_i$ | Costo del insumo $i$ | $\mathbb{R}^+$ | Precio en MXN del insumo $i$ |
| $B$ | Presupuesto | $\mathbb{R}^+$ | Límite de gasto total (50,000) |

### Oferta y Demanda
| Símbolo | Nombre | Tipo | Descripción |
|---------|--------|------|-------------|
| $d_{t,c}$ | Demanda | $\mathbb{Z}^+$ | Porciones requeridas en día $t$, comida $c$ |
| $\delta_{i,t}$ | Donaciones | $\mathbb{R}^+$ | Cantidad externa del insumo $i$ en día $t$ |
| $I_{i,0}$ | Inventario Inicial | $\mathbb{R}^+$ | Stock inicial del insumo $i$ |

### Compra y Producción
| Símbolo | Nombre | Tipo | Descripción |
|---------|--------|------|-------------|
| $\ell_i$ | Lote Comercial | $\mathbb{Z}^+$ | Tamaño de empaque del insumo $i$ |
| $a_{i,m}$ | Coef. Técnico | $\mathbb{R}^+$ | Cantidad de insumo $i$ por porción del plato $m$ |
| $\alpha_{m,t,c}$ | Calendario | $\{0,1\}$ | Disponibilidad: plato $m$ en día $t$, comida $c$ |

---

## Variables de Decisión

### Producción
| Símbolo | Nombre | Tipo | Dominio | Descripción |
|---------|--------|------|---------|-------------|
| $z_{m,t,c}$ | Producción | $\mathbb{Z}$ | $\geq 0$ | Porciones del plato $m$ en día $t$, comida $c$ |

### Compra
| Símbolo | Nombre | Tipo | Dominio | Descripción |
|---------|--------|------|---------|-------------|
| $y_{i,t}$ | Lotes Comprados | $\mathbb{Z}$ | $\geq 0$ | Número de lotes del insumo $i$ en día $t$ |
| $x_{i,t}$ | Volumen Comprado | $\mathbb{R}$ | $\geq 0$ | Masa/cantidad del insumo $i$ en día $t$ |

### Estado del Sistema
| Símbolo | Nombre | Tipo | Dominio | Descripción |
|---------|--------|------|---------|-------------|
| $\gamma_{i,t}$ | Consumo | $\mathbb{R}$ | $\geq 0$ | Insumo $i$ usado/destruido en día $t$ |
| $\mu_{i,t}$ | Inventario | $\mathbb{R}$ | $\geq 0$ | Stock del insumo $i$ al final del día $t$ |

### Función Objetivo
| Símbolo | Nombre | Tipo | Descripción |
|---------|--------|------|-------------|
| $\Phi$ | Costo Total | $\mathbb{R}^+$ | Suma de costos en el horizonte $T$ |

---

## Restricciones Principales

### (1) Demanda
$$\sum_{m \in M} z_{m,t,c} \geq d_{t,c} \quad \forall t, c$$

### (2) Calendario
$$z_{m,t,c} \leq \mathcal{M} \cdot \alpha_{m,t,c} \quad \forall m, t, c$$

### (3) Receta (Menú → Insumo)
$$\gamma_{i,t} = \sum_{c,m} a_{i,m} \cdot z_{m,t,c} \quad \forall i, t$$

### (4) Lotes de Compra
$$x_{i,t} = \ell_i \cdot y_{i,t} \quad \forall i, t$$

### (5) Presupuesto
$$\sum_{t,i} c_i \cdot x_{i,t} \leq B$$

### (6) Balance de Inventario
$$\mu_{i,t} = \mu_{i,t-1} + x_{i,t} + \delta_{i,t} - \gamma_{i,t} \quad \forall i, t$$

### (7) Condiciones de Frontera
- **Inicial:** $\mu_{i,0} = I_{i,0}$
- **Terminal:** $\mu_{i,7} \geq I_{i,0}$

---

## Función Objetivo

$$\min \Phi = \sum_{t \in T} \sum_{i \in I} c_i \cdot x_{i,t}$$

---

## Tabla de Mapeo: Notación Antigua → Nueva

| Antigua | Nueva | Tipo |
|---------|-------|------|
| `Demanda_{t,c}` | $d_{t,c}$ | Parámetro |
| `Donaciones_{i,t}` | $\delta_{i,t}$ | Parámetro |
| `Inventario Inicial` | $I_{i,0}$ | Parámetro |
| `Presupuesto` | $B$ | Parámetro |
| `Coef. Técnicos` | $a_{i,m}$ | Parámetro |
| `Calendario` | $\alpha_{m,t,c}$ | Parámetro |
| `Lote` | $\ell_i$ | Parámetro |
| `Consumo_{i,t}` | $\gamma_{i,t}$ | Variable |
| `Inv_{i,t}` | $\mu_{i,t}$ | Variable |
| `Z` (costo total) | $\Phi$ | Función Objetivo |
| `X_{i,t}` | $x_{i,t}$ | Variable |
| `Y_{i,t}` | $y_{i,t}$ | Variable |
| `Z_{m,t,c}` | $z_{m,t,c}$ | Variable |

---

## Dimensiones del Problema

| Dimensión | Cantidad | Observación |
|-----------|----------|-------------|
| Insumos | 30 | Matriz de recetas: $30 \times 12$ |
| Periodos | 7 | Horizonte: 1 semana |
| Comidas/día | 3 | Desayuno, Comida, Cena |
| Platos disponibles | 12 | Variedad menú |
| **Variables enteras** | $\approx 336$ | $12 \times 7 \times 3$ producción + $30 \times 7$ lotes |
| **Variables continuas** | $\approx 420$ | Compras + consumo + inventario |
| **Restricciones** | $\approx 250$ | Balance + demanda + calendario + presupuesto |

---

## Notas de Implementación

### Para Pyomo
```python
# Conjuntos
model.I = pyo.Set(initialize=range(1, 31))  # Insumos
model.T = pyo.Set(initialize=range(1, 8))   # Días
model.C = pyo.Set(initialize=range(1, 4))   # Comidas
model.M = pyo.Set(initialize=range(1, 13))  # Platos

# Parámetros
model.c = pyo.Param(model.I)           # Costos c_i
model.d = pyo.Param(model.T, model.C)  # Demanda d_{t,c}
model.delta = pyo.Param(model.I, model.T)  # Donaciones δ_{i,t}
model.a = pyo.Param(model.I, model.M)  # Recetas a_{i,m}
model.alpha = pyo.Param(model.M, model.T, model.C)  # Calendario α_{m,t,c}

# Variables
model.z = pyo.Var(model.M, model.T, model.C, within=pyo.NonNegativeIntegers)
model.x = pyo.Var(model.I, model.T, within=pyo.NonNegativeReals)
model.gamma = pyo.Var(model.I, model.T, within=pyo.NonNegativeReals)
model.mu = pyo.Var(model.I, model.T, within=pyo.NonNegativeReals)

# Función objetivo
model.Phi = pyo.Objective(expr=pyo.summation(model.c, model.x), sense=pyo.minimize)
```

### Para Gurobi/CPLEX
Usar directamente los símbolos griegos en comentarios para documentación y utilizar nombres compactos en código:
```python
# z[m,t,c]: producción de plato m en día t, comida c
# x[i,t]: volumen comprado del insumo i en día t
# gamma[i,t]: consumo del insumo i en día t
# mu[i,t]: inventario del insumo i al final del día t
```

---

**Última actualización:** Marzo 2026
**Versión del modelo:** 2.0 (Notación optimizada)
