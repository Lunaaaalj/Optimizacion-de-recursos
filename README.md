# Optimización de Recursos – Casa Monarca 🦋

Modelo de **Programación Lineal Entera Mixta (MILP)** para optimizar la adquisición y distribución de insumos alimentarios en el albergue para migrantes [Casa Monarca](https://www.facebook.com/CasaMonarcaAyudaHumanitaria/) (Santa Catarina, Nuevo León, México).

---

## El Problema

Casa Monarca brinda alimentación a personas en situación de migración. Con un presupuesto limitado, la organización debe garantizar **tres tiempos de comida diarios** (desayuno, comida y cena) para aproximadamente **100 personas** a lo largo de una semana, respetando:

- Los inventarios actuales de la bodega.
- Un menú semanal predefinido (21 platillos asignados a días y tiempos de comida).
- Los tamaños de lote comerciales de cada insumo.
- Las donaciones externas programadas.
- La restricción presupuestal global.
- La condición de que el inventario final no sea menor al inventario inicial (continuidad operativa).

El objetivo es **minimizar el costo total de compras** a lo largo de los 7 días, determinando cuántos lotes de cada insumo adquirir en cada día.

---

## El Modelo MILP

El modelo está formulado sobre los siguientes conjuntos:

| Conjunto | Descripción | Cardinalidad |
|----------|-------------|--------------|
| **I** | Insumos (arroz, frijol, huevo, etc.) | 30 |
| **T** | Días de la semana (lunes–domingo) | 7 |
| **C** | Tiempos de comida (desayuno/comida/cena) | 3 |
| **M** | Platillos disponibles | 12 |

### Variables de decisión

| Variable | Tipo | Descripción |
|----------|------|-------------|
| $z_{m,t,c}$ | Entera ≥ 0 | Porciones del platillo *m* preparadas en día *t*, tiempo *c* |
| $y_{i,t}$ | Entera ≥ 0 | Lotes comerciales del insumo *i* comprados en día *t* |
| $x_{i,t}$ | Real ≥ 0 | Volumen (masa/cantidad) comprado del insumo *i* en día *t* |
| $\gamma_{i,t}$ | Real ≥ 0 | Consumo interno del insumo *i* durante el día *t* |
| $\mu_{i,t}$ | Real ≥ 0 | Inventario del insumo *i* al final del día *t* |

### Función objetivo

$$\min \; \Phi = \sum_{t \in T} \sum_{i \in I} c_i \cdot x_{i,t}$$

### Restricciones principales

1. **Demanda**: $\sum_{m} z_{m,t,c} \ge d_{t,c}$ — se cubren las porciones requeridas.
2. **Calendario** (Big-M): $z_{m,t,c} \le \mathcal{M} \cdot \alpha_{m,t,c}$ — sólo se preparan platillos programados.
3. **Recetas**: $\gamma_{i,t} = \sum_{c,m} a_{i,m} \cdot z_{m,t,c}$ — consumo dictado por los coeficientes técnicos.
4. **Lotes**: $x_{i,t} = \ell_i \cdot y_{i,t}$ — compras en múltiplos comerciales.
5. **Presupuesto**: $\sum_{t,i} c_i \cdot x_{i,t} \le B$.
6. **Balance de inventario**: $\mu_{i,t} = \mu_{i,t-1} + x_{i,t} + \delta_{i,t} - \gamma_{i,t}$.
7. **Inventario terminal**: $\mu_{i,7} \ge I_{i,0}$ — continuidad operativa.

El modelo es resuelto con el solver **GLPK** a través de **Pyomo**.

---

## La Aplicación

Se incluye una interfaz web interactiva construida con **Streamlit** que permite:

- Configurar el presupuesto global y la demanda de porciones.
- Editar los costos unitarios de los 30 insumos.
- Ajustar el inventario inicial y los tamaños de lote.
- Registrar donaciones externas programadas.
- Definir el calendario semanal de platillos.
- Resolver el modelo MILP con un clic y visualizar los resultados en cinco pestañas:
  - **Plan de comidas** – porciones preparadas por día y tiempo.
  - **Compras diarias** – cantidades, lotes y gasto por insumo.
  - **Inventario** – nivel de stock al final de cada día.
  - **Consumo interno** – insumos consumidos por la cocina cada día.
  - **Resumen de costos** – gasto diario con gráfica de barras.
- Descargar los resultados completos en formato `.txt`.

### Ejecutar la aplicación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Instalar el solver GLPK
#    macOS:  brew install glpk
#    Ubuntu: sudo apt-get install glpk-utils
#    Windows: descarga desde https://winglpk.sourceforge.net/

# 3. Verificar que GLPK está disponible
glpsol --version

# 4. Lanzar la interfaz
streamlit run src/gui_streamlit.py
```

La aplicación se abrirá en `http://localhost:8501`.

---

## Estructura del Proyecto

```
Optimizacion-de-recursos/
│
├── data/
│   ├── raw/               # Datos originales (Excel)
│   └── processed/         # Datos procesados (CSV)
│
├── notebooks/             # Scripts de exploración y exportación de datos
│
├── src/                   # Código fuente principal
│   ├── milp_model_core.py # Núcleo del modelo MILP (parámetros + solve_milp)
│   ├── gui_streamlit.py   # Interfaz Streamlit
│   └── result_tables.py   # Generación de tablas de resultados
│
├── reports/
│   ├── COMPLETE_REPORT/   # Reporte completo en LaTeX (contexto y formulación)
│   └── model/             # Especificación formal del modelo en LaTeX
│
├── models/                # Artefactos y metadatos del modelo
├── tests/                 # Pruebas unitarias
├── docs/                  # Documentación adicional
├── requirements.txt       # Dependencias Python
└── README.md
```

---

## Dependencias

| Paquete | Versión mínima | Uso |
|---------|----------------|-----|
| `pyomo` | 6.9.5 | Modelado y resolución MILP |
| `streamlit` | 1.35.0 | Interfaz web interactiva |
| `pandas` | 2.0.0 | Manipulación de datos y tablas |
| `numpy` | 1.24.0 | Cómputo numérico |
| GLPK | — | Solver de optimización (instalación externa) |

---

## Autores

Proyecto desarrollado como parte del curso de **Optimización Determinista** en el Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM).

- Angel Luna
- Ruben Galindo
- Noé Villarreal
- Ignacio Kume

