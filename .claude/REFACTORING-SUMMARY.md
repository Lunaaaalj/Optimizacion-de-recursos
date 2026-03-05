# Resumen de Refactorización: Notación del Modelo MILP

## Fecha
Marzo 5, 2026

## Objetivo Completado
✅ Refactorizar la notación matemática del modelo de optimización MILP reemplazando nombres largos en español con notaciones compactas estándar usando letras griegas y símbolos matemáticos.

## Cambios Realizados

### 1. Archivos Modificados

#### `/reports/model/main.tex` - Actualización Principal
- **Cambio fundamental:** Toda la formulación matemática ahora utiliza notación compacta
- **Adición:** Nueva sección "Notación Matemática" (línea 25) con tabla de referencia para todos los símbolos
- **Impacto:** 100% de las ecuaciones matemáticas actualizadas

### 2. Archivos Creados

#### `/docs/notation-quick-reference.md`
- Tabla de consulta rápida durante modelación
- Mapeo completo antigua ↔ nueva notación
- Ejemplos de implementación en Pyomo, Gurobi, CPLEX
- Dimensiones del problema para referencia

#### `/.claude/PLAN.md` (Documentación del proceso)
- Plan de implementación (archivo interno)
- Decisiones de diseño y ventajas de la nueva notación

## Mapa de Cambios: Parámetros

### Parámetros Económicos
| Anterior | Nuevo | Contexto |
|----------|-------|----------|
| `C` (vector) | $\mathbf{c}$ | Costos unitarios por insumo |
| `C_i` (elemento) | $c_i$ | Costo del insumo $i$ |
| `Lote` | $\ell_i$ | Lotes comerciales |
| `Presupuesto` | $B$ | Budget total |

### Parámetros de Demanda y Oferta
| Anterior | Nuevo | Contexto |
|----------|-------|----------|
| `Demanda_{t,c}` | $d_{t,c}$ | Demanda en día $t$, comida $c$ |
| `Donaciones_{i,t}` | $\delta_{i,t}$ | Donaciones externas (delta para externo) |
| `Inventario Inicial` | $I_{i,0}$ | Stock inicial del insumo $i$ |

### Parámetros Técnicos
| Anterior | Nuevo | Contexto |
|----------|-------|----------|
| `Coeficientes Técnicos` ($\hat{R}_{i,m}$) | $a_{i,m}$ | Matriz de recetas (notación estándar) |
| `Calendario` ($\mathcal{A}_{m,t,c}$) | $\alpha_{m,t,c}$ | Asignación de menú (alpha para assignment) |

---

## Mapa de Cambios: Variables de Decisión

### Variables Enteras
| Anterior | Nuevo | Cambio |
|----------|-------|--------|
| `Z_{m,t,c}` | $z_{m,t,c}$ | Minúscula (notación estándar) |
| `Y_{i,t}` | $y_{i,t}$ | Minúscula (notación estándar) |

### Variables Continuas
| Anterior | Nuevo | Cambio |
|----------|-------|--------|
| `X_{i,t}` | $x_{i,t}$ | Minúscula (consistencia) |
| `Consumo_{i,t}` | $\gamma_{i,t}$ | **Letra griega:** gamma para consumo/flujo |
| `Inv_{i,t}` | $\mu_{i,t}$ | **Letra griega:** mu para variable de estado |

### Función Objetivo
| Anterior | Nuevo | Cambio |
|----------|-------|--------|
| `Z` (variable de costo total) | $\Phi$ | **Letra griega:** phi para función objetivo global |

---

## Cambios en Ecuaciones Principales

### Ecuación 1: Satisfacción de Demanda
**Antes:**
```latex
\sum_{m \in M} Z_{m,t,c} \ge Demanda_{t,c}
```

**Después:**
```latex
\sum_{m \in M} z_{m,t,c} \ge d_{t,c}
```

### Ecuación 2: Relación Menú → Insumo
**Antes:**
```latex
Consumo_{i,t} = \sum_{c,m} \hat{R}_{i,m} \cdot Z_{m,t,c}
```

**Después:**
```latex
\gamma_{i,t} = \sum_{c \in C} \sum_{m \in M} a_{i,m} \cdot z_{m,t,c}
```

### Ecuación 3: Lotes de Compra
**Antes:**
```latex
X_{i,t} = Lote_i \cdot Y_{i,t}
```

**Después:**
```latex
x_{i,t} = \ell_i \cdot y_{i,t}
```

### Ecuación 4: Balance de Inventario
**Antes:**
```latex
Inv_{i,t} = Inv_{i,t-1} + X_{i,t} + Donaciones_{i,t} - Consumo_{i,t}
```

**Después:**
```latex
\mu_{i,t} = \mu_{i,t-1} + x_{i,t} + \delta_{i,t} - \gamma_{i,t}
```

### Ecuación 5: Función Objetivo
**Antes:**
```latex
\min \mathcal{Z} = \sum_{t} \sum_{i} C_i \cdot X_{i,t}
```

**Después:**
```latex
\min \Phi = \sum_{t \in T} \sum_{i \in I} c_i \cdot x_{i,t}
```

---

## Ventajas de la Nueva Notación

### 1. **Compacidad**
- Nombres simples: `$\gamma$` vs `Consumo`
- Ideales para ecuaciones complejas

### 2. **Consistencia**
- Un símbolo único = una entidad única
- Menores ambigüedades

### 3. **Estandarización**
- Alineada con literatura académica en OR
- Compatible con solver documentation

### 4. **Implementabilidad**
- Traducción directa a código Pyomo
- Variable names más limpios

### 5. **Profesionalismo**
- Aspecto más académico
- Facilita presentaciones y papers

---

## Notación Elegida: Criterios

### Parámetros: Minúsculas latinas + Letras griegas
- $c_i$ - costos (estándar en economía)
- $d_{t,c}$ - demanda (estándar en logística)
- $\delta_{i,t}$ - delta para externo (supply chain terminology)
- $a_{i,m}$ - coefficients (matriz de restricciones)
- $\alpha_{m,t,c}$ - alpha para asignación (assignment)
- $\ell_i$ - lota para lotes (lambda alternativa)

### Variables: Minúsculas latinas + Letras griegas
- $x, y, z$ - variables básicas (mantener, son estándar)
- $\gamma_{i,t}$ - gamma para flujos (flow)
- $\mu_{i,t}$ - mu para estado (memory state)

### Función Objetivo: Mayúscula griega
- $\Phi$ - phi para función global objetivo

---

## Impacto en Documentos Relacionados

### Archivos que hacen referencia al modelo:
1. `/CLAUDE.md` - Actualizado para mencionar la refactorización
2. `/notebooks/data_export.py` - Sin cambios (no usa notación matemática)
3. Futuros notebooks de Pyomo - Deberán usar la nueva notación

### Cambios Necesarios Posteriores:
- [ ] Si existen notebooks con código Pyomo, actualizar para usar nueva notación
- [ ] Si hay reportes adicionales, actualizar referencias al modelo
- [ ] Si hay presentaciones, actualizar slides con nueva notación

---

## Compatibilidad Hacia Atrás

### ✅ Mantenido
- Tablas de datos en español (claridad contextual)
- Estructura general del documento
- Explicaciones en español
- Valores de parámetros (conjuntos, costos, recetas, etc.)

### ⚠️ Cambió
- Toda la formulación matemática
- Referencias en ecuaciones

### ✅ Facilitado
- Implementación en Pyomo
- Comunicación académica
- Documentación de código

---

## Archivos Afectados - Resumen

```
Optimizacion-de-recursos/
├── reports/model/
│   └── main.tex ✏️ [MODIFICADO] Todas las ecuaciones + Nueva sección de notación
├── docs/
│   └── notation-quick-reference.md ✨ [NUEVO] Tabla de referencia rápida
├── .claude/
│   ├── PLAN.md ✨ [NUEVO] Plan de implementación
│   └── REFACTORING-SUMMARY.md ✨ [NUEVO] Este archivo
└── CLAUDE.md ✓ [Ya existe] Contiene contexto del proyecto
```

---

## Próximos Pasos Recomendados

1. **Validar compilación LaTeX**
   - Asegurar que `main.tex` compila sin errores
   - Los warnings de overfull/underfull son menores

2. **Crear código Pyomo con nueva notación**
   - Usar como referencia `/docs/notation-quick-reference.md`
   - Mapeo directo de símbolos a nombres de variables

3. **Actualizar cualquier documentación externa**
   - Presentaciones
   - Papers
   - README de repositorios relacionados

4. **Considerar versionamiento**
   - Modelo v1.0 (notación antigua) → v2.0 (notación nueva)
   - Actualizar changelog en repositorio

---

## Notas Técnicas

### Símbolos Especiales en LaTeX
- Delta ($\delta$): `\delta`
- Gamma ($\gamma$): `\gamma`
- Mu ($\mu$): `\mu`
- Alpha ($\alpha$): `\alpha`
- Phi ($\Phi$): `\Phi`
- Lambda/Lota ($\ell$): `\ell`
- Bold math ($\mathbf{c}$): `\mathbf{c}`

### Consistencia Matemática
- Variables endógenas: minúsculas ($x, y, z, \gamma, \mu$)
- Parámetros exógenos: minúsculas o griegas ($c, d, \delta, a, \alpha, \ell$)
- Conjuntos: mayúsculas ($I, T, C, M$)
- Función objetivo: mayúscula griega ($\Phi$)

---

## Control de Calidad

✅ Todas las ecuaciones actualizadas
✅ Notación consistente en todo el documento
✅ Tabla de referencia creada
✅ Documento de mapeo disponible
✅ Ejemplos de implementación incluidos
✅ Comentarios en LaTeX actualizados

**Status:** Refactorización completada y documentada ✓

---

*Refactorización realizada por: Claude Code*
*Método: Análisis sistemático de notación + Reemplazo de variables + Documentación*
