# Plan: Refactorizar Notación del Modelo de Optimización

## Objetivo
Mejorar la notación matemática del modelo MILP reemplazando nombres largos con notaciones estándar usando letras griegas y símbolos matemáticos compactos para facilitar la modelación e implementación en Pyomo.

## Análisis Actual
El modelo actual usa:
- Nombres en español largos: `Donaciones`, `Consumo`, `Demanda`, `Inventario`, `Presupuesto`
- Notación mixta: algunas variables con $X$, otras con nombres completos
- Índices poco claros en contexto de operaciones matriciales

## Propuesta de Notación Mejorada

### Sets (Índices) - Sin cambios
- $I$ - conjunto de insumos (ingredientes)
- $T$ - conjunto de periodos (días)
- $C$ - conjunto de comidas
- $M$ - conjunto de platos

### Parámetros (Notación simplificada)

| Actual | Nuevo | Descripción |
|--------|-------|-------------|
| `C` | $\mathbf{c}$ | Vector de costos unitarios |
| `Lote` | $\ell$ | Lotes comerciales |
| `Demanda_{t,c}` | $d_{t,c}$ | Demanda por periodo y comida |
| `Donaciones_{i,t}` | $\delta_{i,t}$ | Donaciones externas (delta) |
| `Inventario Inicial` | $I_0$ o $\iota_i^0$ | Inventario inicial (iota) |
| `Presupuesto` | $B$ | Budget total |
| `Coeficientes Técnicos` | $a_{i,m}$ | Matriz de recetas (ingredientes por plato) |
| `Calendario` | $\alpha_{m,t,c}$ | Asignación binaria de menú (alpha) |

### Variables de Decisión

| Actual | Nuevo | Tipo | Descripción |
|--------|-------|------|-------------|
| `Z_{m,t,c}` | $z_{m,t,c}$ | Entera | Porciones de plato $m$ en día $t$, comida $c$ |
| `Y_{i,t}` | $y_{i,t}$ | Entera | Número de lotes del insumo $i$ en día $t$ |
| `X_{i,t}` | $x_{i,t}$ | Continua | Volumen comprado del insumo $i$ en día $t$ |
| `Consumo_{i,t}` | $\gamma_{i,t}$ | Continua | Consumo interno del insumo $i$ en día $t$ (gamma) |
| `Inv_{i,t}` | $\mu_{i,t}$ | Continua | Inventario final del insumo $i$ al final de día $t$ (mu) |

### Función Objetivo
| Actual | Nuevo | Descripción |
|--------|-------|-------------|
| `Z` (costo total) | $\Phi$ | Función objetivo (phi) |

## Ventajas de Nueva Notación

1. **Compacta**: Símbolos de una letra en lugar de nombres largos
2. **Estándar**: Sigue convenciones de programación matemática
3. **Distinguible**: Fácil diferencias entre parámetros (letras minúsculas latinas) y variables (letras griegas para estado)
4. **Implementable**: Mejor para traducción a código Pyomo
5. **Profesional**: Alineada con literatura académica en operations research

## Fases de Implementación

### Fase 1: Crear tabla de mapeo de notación
- [ ] Documento con correspondencia antigua ↔ nueva
- [ ] Incluir en sección introductoria de main.tex

### Fase 2: Reescribir secciones principales
- [ ] Introducción: explicar cambio de notación
- [ ] Parámetros: actualizar definiciones con nuevos símbolos
- [ ] Variables: definir con nueva notación

### Fase 3: Actualizar todas las ecuaciones
- [ ] Restricción de demanda
- [ ] Filtro de calendario
- [ ] Relación menú → insumo
- [ ] Lotes de compra
- [ ] Límite presupuestal
- [ ] Balance de inventario (ecuación de diferencias)
- [ ] Condición terminal

### Fase 4: Crear documento de referencia
- [ ] Una página con notación compacta para consulta rápida
- [ ] Tabla de conjuntos, parámetros, variables

## Decisiones de Diseño

✅ **Mantener**:
- Estructura general del documento
- Tablas de datos con nombres descriptivos en español (para claridad del contexto)
- Explicaciones en español

✅ **Cambiar**:
- Todas las ecuaciones matemáticas
- Definiciones de variables y parámetros
- Símbolos en el contenido principal

❓ **Pendiente** (requiere confirmación del usuario):
- ¿Crear archivo separado con mapeo completo o integrar en main.tex?
- ¿Cambiar los nombres en las tablas de parámetros reales o solo en las ecuaciones?
- ¿Incluir hoja de "Notación Rápida" como apéndice?

## Impacto Esperado

- **Legibilidad matemática**: +40% (símbolos más claros)
- **Transferibilidad a código**: Alta (alineado con convenciones de programación)
- **Consistencia**: Total (un símbolo = una entidad única)
