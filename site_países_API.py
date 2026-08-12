import streamlit as st
import requests

from utils.api import (
    buscar_por_codigo,
    buscar_por_nome_pt,
    filtrar_paises_por_regiao,
    listar_paises_pt,
)
from utils.formatters import (
    extrair_bandeira_url,
    extrair_capital,
    extrair_emoji,
    extrair_nome_pt,
    formatar_area,
    formatar_populacao,
    formatar_regiao,
)
from utils.session import obter_historico, obter_nome_pt, obter_pais, salvar_pais

st.set_page_config(
    page_title="INFOWORLD",
    page_icon="🌍",
    layout="centered",
)

PAISES_POPULARES = [
    "Brasil",
    "Portugal",
    "Argentina",
    "Japão",
    "França",
    "Estados Unidos",
]

st.markdown(
    """
    <style>
    .preview-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        margin-top: 1rem;
    }
    .chip-label {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("INFOWORLD 🌍")
st.subheader("Descubra informações sobre qualquer país 🗺️")
st.caption("Pesquise países em português e explore informações detalhadas e mapas.")

if "pais_selecionado_nome" not in st.session_state:
    st.session_state.pais_selecionado_nome = None


def carregar_pais(nome: str) -> None:
    paises = listar_paises_pt()
    codigo = paises.get(nome)
    if not codigo:
        st.error("❌ País não encontrado.")
        return

    try:
        with st.spinner(f"Carregando {nome}..."):
            dados = buscar_por_codigo(codigo)
        if not dados:
            st.error("❌ Não foi possível carregar os dados do país.")
            return
        salvar_pais(dados)
        st.session_state.pais_selecionado_nome = nome
    except requests.exceptions.Timeout:
        st.error("⏳ Tempo de conexão esgotado. Tente novamente.")
    except requests.exceptions.RequestException:
        st.error("❌ Erro ao conectar com a API.")


def render_preview(dados: dict) -> None:
    nome = extrair_nome_pt(dados)
    emoji = extrair_emoji(dados)
    bandeira = extrair_bandeira_url(dados)
    capital = extrair_capital(dados)
    regiao = formatar_regiao(dados.get("region", "N/A"))
    populacao = formatar_populacao(dados.get("population", 0))

    st.markdown('<div class="preview-card">', unsafe_allow_html=True)
    col_flag, col_info = st.columns([1, 2])
    with col_flag:
        if bandeira:
            st.image(bandeira, width=180)
    with col_info:
        st.markdown(f"### {emoji} {nome}")
        st.write(f"**Capital:** {capital}")
        st.write(f"**Região:** {regiao}")
        st.write(f"**População:** {populacao} habitantes")
        st.write(f"**Área:** {formatar_area(dados)} km²")
    st.markdown("</div>", unsafe_allow_html=True)

    st.success(
        "País selecionado! Use a barra lateral para ver **Informações** ou **Mapa Mundi**."
    )


try:
    with st.spinner("Carregando lista de países..."):
        todos_paises = listar_paises_pt()
except Exception:
    st.error("❌ Não foi possível carregar a lista de países. Verifique sua conexão e a chave da API.")
    st.stop()

if not todos_paises:
    st.error("❌ Lista de países vazia. Verifique a chave PAIS_API em .streamlit/secrets.toml.")
    st.stop()

st.markdown('<p class="chip-label">Países populares — clique para selecionar:</p>', unsafe_allow_html=True)
cols = st.columns(len(PAISES_POPULARES))
for i, pais_nome in enumerate(PAISES_POPULARES):
    if pais_nome in todos_paises and cols[i].button(pais_nome, key=f"pop_{pais_nome}", use_container_width=True):
        carregar_pais(pais_nome)

historico = obter_historico()
if historico:
    st.markdown('<p class="chip-label">Buscados recentemente:</p>', unsafe_allow_html=True)
    hist_cols = st.columns(min(len(historico), 5))
    for i, nome_hist in enumerate(historico[:5]):
        if hist_cols[i].button(nome_hist, key=f"hist_{nome_hist}", use_container_width=True):
            carregar_pais(nome_hist)

st.divider()

regiao_filtro = st.radio(
    "Filtrar por região:",
    options=["Todas", "Américas", "Europa", "Ásia", "África", "Oceania"],
    horizontal=True,
)

paises_filtrados = filtrar_paises_por_regiao(todos_paises, regiao_filtro)
nomes_paises = list(paises_filtrados.keys())

nome_atual = obter_nome_pt()
indice = None
if nome_atual and nome_atual in nomes_paises:
    indice = nomes_paises.index(nome_atual)

pais_escolhido = st.selectbox(
    "Escolha ou digite o nome de um país:",
    options=nomes_paises,
    index=indice,
    placeholder="Exemplo: Brasil, Alemanha, Japão...",
)

with st.expander("🔎 Busca por texto livre"):
    termo_livre = st.text_input(
        "Digite parte do nome em português:",
        placeholder="Exemplo: brasil, alemanha...",
    )
    if st.button("Buscar", key="busca_livre"):
        if not termo_livre.strip():
            st.warning("⚠️ Digite um termo para buscar.")
        else:
            try:
                with st.spinner("Buscando..."):
                    dados = buscar_por_nome_pt(termo_livre)
                if dados:
                    salvar_pais(dados)
                    st.session_state.pais_selecionado_nome = extrair_nome_pt(dados)
                    st.rerun()
                else:
                    st.error("❌ País não encontrado.")
            except requests.exceptions.Timeout:
                st.error("⏳ Tempo de conexão esgotado. Tente novamente.")
            except requests.exceptions.RequestException:
                st.error("❌ Erro ao conectar com a API.")

if pais_escolhido and pais_escolhido != st.session_state.get("pais_selecionado_nome"):
    carregar_pais(pais_escolhido)

dados_atuais = obter_pais()
if dados_atuais:
    st.divider()
    render_preview(dados_atuais)
else:
    st.info("Selecione um país na lista acima ou use os atalhos de países populares.")
