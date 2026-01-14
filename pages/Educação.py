import streamlit as st
import pandas as pd
from core.dados import prouni_agg, bolsas_por_ano
from core.utils import card_percentual
import altair as alt

st.set_page_config(
    page_title="Educação",
    layout="wide")
st.title("Educação")
st.markdown(
    """
    Esta página analisa a **evolução da concessão de bolsas do ProUni** a partir de recortes sociais fundamentais para o debate sobre desigualdades no acesso ao ensino superior no Brasil.

    A base utilizada foi construída a partir de dados disponibilizados pelo **MEC**, através de uma lógica de limpeza e agregação que permitisse interpretações gerais das informações sob ótica temporal. (https://dadosabertos.mec.gov.br/prouni).

    A análise compara os anos de **2015 a 2020**, permitindo observar
    mudanças estruturais no acesso à educação superior no Brasil.
    """, unsafe_allow_html=True)

"#474A49"
st.markdown(
    """
    <div style="
        background-color: #474A49;
        border-left: 4px solid #6b7280;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 14px;
        color: #ECF9F6;
    ">
        🔍 <strong>Como usar a visualização</strong><br>
        Através dos filtros abaixo, o usuário pode montar o perfil de estudante que deseja analisar e acompanhar a evolução da participação nas bolsas ao longo dos anos.
    </div>
    """,
    unsafe_allow_html=True
)
st.subheader("")
c1, c2, c3= st.columns(3)
with c1:
    sexo = st.selectbox(
    "Gênero",
    sorted(prouni_agg["SEXO_BENEFICIARIO"].unique()))
with c2:
    raca = st.selectbox(
    "Raça",
    sorted(prouni_agg["RACA_BENEFICIARIO"].unique()))
with c3:
    opcoes_regiao = sorted(
    prouni_agg["REGIAO_BENEFICIARIO"]
    .dropna()
    .unique())
    regiao = st.selectbox("Região", opcoes_regiao)

df_plot = prouni_agg[
    (prouni_agg["SEXO_BENEFICIARIO"] == sexo) &
    (prouni_agg["RACA_BENEFICIARIO"] == raca) &
    (prouni_agg["REGIAO_BENEFICIARIO"] == regiao)]
df_plot = (
    df_plot
    .groupby("ANO_CONCESSAO_BOLSA", as_index=False)["quantidade"]
    .sum())
chart = (
    alt.Chart(df_plot)
    .mark_bar(color="#97AAA6")
    .encode(
        x=alt.X(
            "ANO_CONCESSAO_BOLSA:O",
            title="Ano"),
        y=alt.Y(
            "quantidade:Q",
            title="Número de bolsas"),
        tooltip=[
            alt.Tooltip("ANO_CONCESSAO_BOLSA:O", title="Ano"),
            alt.Tooltip("quantidade:Q", title="Bolsas")])
    .properties(height=400))
st.altair_chart(chart, use_container_width=True)
st.subheader("Participação", divider='grey')
df_pct = df_plot.merge(
    bolsas_por_ano,
    on="ANO_CONCESSAO_BOLSA",
    how="left")

df_pct["percentual"] = (
    100 * df_pct["quantidade"] / df_pct["total_bolsas"])
pct_2015 = df_pct.loc[df_pct["ANO_CONCESSAO_BOLSA"] == 2015, "percentual"].iloc[0]
pct_2016 = df_pct.loc[df_pct["ANO_CONCESSAO_BOLSA"] == 2016, "percentual"].iloc[0]
pct_2017 = df_pct.loc[df_pct["ANO_CONCESSAO_BOLSA"] == 2017, "percentual"].iloc[0]
pct_2018 = df_pct.loc[df_pct["ANO_CONCESSAO_BOLSA"] == 2018, "percentual"].iloc[0]
pct_2019 = df_pct.loc[df_pct["ANO_CONCESSAO_BOLSA"] == 2019, "percentual"].iloc[0]
pct_2020 = df_pct.loc[df_pct["ANO_CONCESSAO_BOLSA"] == 2020, "percentual"].iloc[0]

c1, c2, c3, c4, c5, c6= st.columns(6)
with c1:
    card_percentual(pct_2015, 2015)
with c2:
    card_percentual(pct_2016, 2016)
with c3:
    card_percentual(pct_2017, 2017)
with c4:
    card_percentual(pct_2018, 2018)
with c5:
    card_percentual(pct_2019, 2019)
with c6:
    card_percentual(pct_2020, 2020)
