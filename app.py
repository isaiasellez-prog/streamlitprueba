import streamlit as st
import pandas as pd

st.title("Consulta COSTOS_SALUD")

data = pd.DataFrame({
    "Periodo": [2024, 2024, 2025, 2025],
    "Division": ["Chuquicamata", "Salvador", "Chuquicamata", "Andina"],
    "Costo": [120000, 300000, 150000, 200000]
})

division = st.selectbox("División", data["Division"].unique())

df = data[data["Division"] == division]

st.dataframe(df)
