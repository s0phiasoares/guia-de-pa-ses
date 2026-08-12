import streamlit as st

from utils.formatters import extrair_nome_pt

HISTORICO_MAX = 5


def _init_session() -> None:
    if "pais_dados" not in st.session_state:
        st.session_state.pais_dados = None
    if "nome_pt" not in st.session_state:
        st.session_state.nome_pt = None
    if "historico" not in st.session_state:
        st.session_state.historico = []


def salvar_pais(dados: dict) -> None:
    _init_session()
    st.session_state.pais_dados = dados
    nome = extrair_nome_pt(dados)
    st.session_state.nome_pt = nome

    historico = st.session_state.historico
    historico = [h for h in historico if h != nome]
    historico.insert(0, nome)
    st.session_state.historico = historico[:HISTORICO_MAX]


def obter_pais() -> dict | None:
    _init_session()
    return st.session_state.pais_dados


def obter_nome_pt() -> str | None:
    _init_session()
    return st.session_state.nome_pt


def obter_historico() -> list[str]:
    _init_session()
    return st.session_state.historico
