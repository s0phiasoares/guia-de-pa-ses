import streamlit as st

from utils.formatters import (
    extrair_bandeira_url,
    extrair_capital,
    extrair_emoji,
    extrair_idiomas,
    extrair_moedas,
    extrair_nome_pt,
    formatar_area,
    formatar_populacao,
    formatar_regiao,
    formatar_subregiao,
)
from utils.session import obter_pais

st.set_page_config(
    page_title="Informações — INFOWORLD",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Informações do País")

dados = obter_pais()

if not dados:
    st.warning("Nenhum país selecionado.")
    st.info("Volte à página **Início** e selecione um país para ver as informações completas.")
    st.stop()

nome = extrair_nome_pt(dados)
emoji = extrair_emoji(dados)
bandeira = extrair_bandeira_url(dados)
capital = extrair_capital(dados)
regiao = formatar_regiao(dados.get("region", "N/A"))
subregiao = formatar_subregiao(dados.get("subregion", "N/A"))
populacao = dados.get("population", 0)
moedas = extrair_moedas(dados)
idiomas = extrair_idiomas(dados)
nome_en = dados.get("names", {}).get("common", "")

col_bandeira, col_detalhes = st.columns([1, 2])

with col_bandeira:
    if bandeira:
        st.image(bandeira, width=300)
    st.markdown(f"## {emoji} {nome}")
    if nome_en and nome_en != nome:
        st.caption(f"Nome em inglês: {nome_en}")

with col_detalhes:
    m1, m2 = st.columns(2)
    m1.metric("População", f"{formatar_populacao(populacao)} hab.")
    m2.metric("Área", f"{formatar_area(dados)} km²")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Localização")
        st.write(f"**Capital:** {capital}")
        st.write(f"**Região:** {regiao}")
        st.write(f"**Sub-região:** {subregiao}")
    with c2:
        st.subheader("Cultura e economia")
        st.write(f"**Moeda(s):** {moedas}")
        st.write(f"**Idioma(s):** {idiomas}")

st.divider()
st.caption("Dados fornecidos pela REST Countries API.")
