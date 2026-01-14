import streamlit as st
import pandas as pd
from core.dados import dados_genero
import altair as alt

st.set_page_config(
    page_title="Gênero e Trabalho",
    layout="wide")
st.title("Gênero e Trabalho")
st.markdown(
    """
    Esta página apresenta a **distribuição das mulheres ocupadas segundo tipo de atividade exercida**.

    A base utilizada foram os dados do **Atlas do Desenvolvimento Humano (Censo Demográfico)**, que foram retirados dos indicadores sociais do **IPEA Data** (https://www.ipeadata.gov.br/Default.aspx).

    A análise compara os anos de **2000 e 2010**, permitindo observar
    mudanças estruturais no mercado de trabalho feminino no Brasil.
    """, unsafe_allow_html=True)
st.subheader("  ")

st.subheader("Comparativo de atividades femininas entre os anos de 2000 e 2010 por Estado", divider='grey')
st.badge("Selecione, abaixo, o Estado para o qual deseja visualizar os dados.", color="green")
estado_selecionado = st.selectbox(
    "",
    sorted(dados_genero["Estado"].unique()),
    index=0)
col1, col2 =st.columns(2)
dados_genero_plot = dados_genero[dados_genero["Estado"] == estado_selecionado]
paleta_atividades = [
    "#1F7891",  # Verde petróleo
    "#1E6F5C",  # Verde azulado
    "#5E548E",  # Roxo acinzentado
    "#7D6B91",  # Roxo suave
    "#9F86C0"   # Lilás
]
ordem_atividades = [
    "Com carteira",
    "Sem carteira",
    "Conta Própria",
    "Empregadoras",
    "Setor Público"
]
chart = (
    alt.Chart(dados_genero_plot)
    .mark_bar()
    .encode(
        x=alt.X(
            "atividade:N",
            title="Posição na ocupação",
            sort='-y',
            axis=alt.Axis(labelAngle=0)),
        xOffset="ano:N",
        y=alt.Y(
            "percentual:Q",
            title="Percentual (%)",
            axis=alt.Axis(
                grid=True,
                gridColor="#dddddd",
                gridOpacity=0.2)),
        color=alt.Color(
            "atividade:N",
            scale=alt.Scale(
                domain=ordem_atividades,
                range=paleta_atividades),
            legend=alt.Legend(
                title="Atividade",
                orient="bottom",
                direction="horizontal")),
        tooltip=[
            alt.Tooltip("atividade:N", title="Atividade"),
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("percentual:Q", title="Percentual", format=".2f")])
    .properties(height=400))
resumo = (dados_genero_plot
    .pivot_table(
        index="atividade",
        columns="ano",
        values="percentual")
    .reset_index())

resumo["variacao"] = resumo[2010] - resumo[2000]
atividade_maior_alta = resumo.sort_values("variacao", ascending=False).iloc[0]
atividade_maior_queda = resumo.sort_values("variacao").iloc[0]

st.markdown(
    f"""
    <p style="font-size:16px; color:#E6F5EC; margin-bottom:10px;">
        Entre 2000 e 2010, <strong>{atividade_maior_alta['atividade']}</strong> foi a modalidade de atividade
        que mais cresceu entre as mulheres em {estado_selecionado}, enquanto a modalidade
        <strong>{atividade_maior_queda['atividade']}</strong> apresentou a maior retração.
    </p>
    """,
    unsafe_allow_html=True
)
st.altair_chart(chart, use_container_width=True)
st.caption(
    "As barras representam a participação percentual das mulheres ocupadas por posição na ocupação. "
    "As variações entre 2000 e 2010 são expressas em pontos percentuais.")
linhas_texto = []
for _, row in resumo.iterrows():
    atividade = row["atividade"]
    var = row["variacao"]
    if var > 0:
        frase = f"<strong>{atividade}</strong>: aumento de <strong>{var:.1f} p.p.</strong> entre 2000 e 2010."
    elif var < 0:
        frase = f"<strong>{atividade}</strong>: redução de <strong>{abs(var):.1f} p.p.</strong> no período."
    else:
        frase = f"<strong>{atividade}</strong>: manteve-se estável entre 2000 e 2010."
    linhas_texto.append(f"<li>{frase}</li>")
texto_html = "".join(linhas_texto)

st.markdown(
    f"""
    <div style="
        background-color: #4E525A;
        border-left: 6px solid #238B45;
        padding: 18px 22px;
        border-radius: 10px;
        margin-top: 20px;
        margin-bottom: 30px;
    ">
        <h4 style="margin-top: 0; color: #E6F5EC;">
            Principais mudanças no mercado de trabalho feminino ({estado_selecionado})
        </h4>
        <p style="color: #BCC0C8; font-size: 15px;">
            A comparação entre os anos de 2000 e 2010 evidencia transformações
            na forma de inserção das mulheres no mercado de trabalho:
        </p>
        <ul style="color: #BCC0C8; font-size: 15px;">
            {texto_html}
        </ul>
        <p style="font-size: 13px; color: #E6F5EC;">
            <em>Variação expressa em pontos percentuais (p.p.).</em>
        </p>
    </div>
    """,
    unsafe_allow_html=True)