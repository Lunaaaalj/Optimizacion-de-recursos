# %%
import pandas as pd
df = pd.read_excel("data/raw/Inventario bodega.xlsx",header = 2)
print(df.head(5))
df.to_csv("data/processed/inventario_bodega.csv",index = False)

# %%
df = pd.read_excel("data/raw/beneficiarios 2025 (2).xlsx")
print(df.head(10))
df.to_csv("data/processed/beneficiarios.csv",index = False)
