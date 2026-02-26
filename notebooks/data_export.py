# %%
import pandas as pd
df = pd.read_excel("data/raw/Inventario bodega.xlsx",header = 2)
print(df.head(5))
df.to_csv("data/processed/inventario_bodega.csv")
