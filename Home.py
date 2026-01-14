import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Portifólio- Vaga Gênero e Número",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🔎Observatório de Gênero, Raça e Educação no Brasil")
st.subheader("", divider='grey')
c1, c2= st.columns([1.5, 2])
with c1:
    d1, d2= st.columns(2)
    with d1:
        st.image(
            "assets/img/imagem_home.jpg",
            use_container_width=True)
        st.image(
            "assets/img/imagem2_home.jpg",
            use_container_width=True)
    with d2:
        st.image(
            "assets/img/imagem3_home.jpg",
            use_container_width=True)
        st.image(
            "assets/img/imagem4_home.jpg",
            use_container_width=True)
    st.caption("Imagens ilustrativas | Fonte: Unsplash")

with c2:
    st.markdown(
        """
        Esse projeto foi desenvolvido como um **exercício de demonstração prática das competências exigidas para atuação no cargo de Analista de Dados**.
        O portal simula um **observatório de dados baseado em fontes públicas oficiais**, com foco na **coleta, tratamento, análise e comunicação de informações sensíveis** relacionadas à gênero, raça e educação no Brasil. A abordagem adotada é **interseccional**, considerando recortes de **raça, território e temporalidade**.

        Todas as etapas do projeto, desde a **obtenção das bases de dados** até a **construção de indicadores e visualizações**, foram orientadas por critérios de **rigor metodológico, transparência e reprodutibilidade**, buscando refletir as **práticas adotadas pelo jornalismo de dados** e por organizações que atuam na produção de conhecimento voltado aos direitos humanos.
        """,
    unsafe_allow_html=True)

#botar imagem no Home