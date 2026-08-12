import streamlit as st

from utils.formatters import extrair_coordenadas, extrair_emoji, extrair_nome_pt
from utils.session import obter_pais

st.set_page_config(
    page_title="Mapa Mundi — INFOWORLD",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ Mapa Mundi")

dados = obter_pais()

if not dados:
    st.warning("Nenhum país selecionado.")
    st.info("Volte à página **Início** e selecione um país para visualizá-lo no mapa.")
    st.stop()

nome = extrair_nome_pt(dados)
emoji = extrair_emoji(dados)
lat, lng = extrair_coordenadas(dados)

st.markdown(f"### {emoji} {nome}")

if lat is None or lng is None:
    st.error("❌ Coordenadas não disponíveis para este país.")
    st.stop()

st.caption(f"Latitude: {lat:.4f} | Longitude: {lng:.4f}")

st.map(
    {"lat": [lat], "lon": [lng]},
    zoom=4,
    use_container_width=True,
)

st.info("Use o zoom do mapa para explorar a região ao redor do país selecionado.")
