import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CONFIG ----------
st.set_page_config(
    page_title="ISALUD — COSTO_INTERCONSULTAS",
    layout="wide"
)

# ---------- ESTILO ISALUD ----------
st.markdown("""
<style>
.metric-card {
    background-color:#f3f7fb;
    padding:15px;
    border-radius:12px;
    border:1px solid #e1e7ef;
}
.title-isalud {
    color:#0b5cab;
    font-weight:700;
    font-size:28px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title-isalud">Dashboard COSTO_INTERCONSULTAS</div>', unsafe_allow_html=True)

# ---------- DATA ----------
df = pd.DataFrame({
    "Periodo":[2024,2024,2025,2025],
    "Division":["Chuquicamata","Salvador","Chuquicamata","Andina"],
    "Costo":[120000,300000,150000,200000]
})

# ---------- SIDEBAR FILTROS ----------
st.sidebar.header("Filtros")

cols_cat = df.select_dtypes(include="object").columns.tolist()

filtros = {}

for c in cols_cat[:4]:
    valores = df[c].dropna().unique()
    seleccion = st.sidebar.multiselect(c, valores, default=valores)
    filtros[c] = seleccion

df_f = df.copy()

for c, vals in filtros.items():
    df_f = df_f[df_f[c].isin(vals)]

# ---------- KPIs ----------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Registros", f"{len(df_f):,}")

num_cols = df_f.select_dtypes(include="number").columns

if len(num_cols) > 0:
    with k2:
        st.metric("Costo total", f"{df_f[num_cols[0]].sum():,.0f}")

    with k3:
        st.metric("Promedio", f"{df_f[num_cols[0]].mean():,.0f}")

    with k4:
        st.metric("Máximo", f"{df_f[num_cols[0]].max():,.0f}")

st.divider()

# ---------- CONTROLES INTERACTIVOS ----------
c1, c2 = st.columns(2)

with c1:
    x = st.selectbox("Eje X", df_f.columns)

with c2:
    y = st.selectbox("Eje Y", num_cols if len(num_cols) > 0 else df_f.columns)

# ---------- GRÁFICO ----------
if y:
    fig = px.bar(df_f, x=x, y=y)

# barras 40% más delgadas
fig.update_traces(width=0.6)

st.plotly_chart(fig, use_container_width=True)

# ---------- TABLA ----------
st.subheader("Detalle")

st.dataframe(
    df_f,
    use_container_width=True,
    height=450
)

# ---------- EXPORT ----------
st.download_button(
    "Descargar Excel",
    df_f.to_csv(index=False),
    file_name="consulta_interconsultas.csv"
)
