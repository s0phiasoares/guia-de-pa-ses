import streamlit as st
import requests

from utils.formatters import extrair_nome_pt

API_BASE = "https://api.restcountries.com/countries/v5"
TIMEOUT = 10

REGIOES_FILTRO = {
    "Todas": None,
    "Américas": "Americas",
    "Europa": "Europe",
    "Ásia": "Asia",
    "África": "Africa",
    "Oceania": "Oceania",
}


def _headers() -> dict:
    chave = st.secrets.get("PAIS_API", "")
    return {"Authorization": f"Bearer {chave}"}


def _extrair_objetos(resposta_json: dict) -> list[dict]:
    if not isinstance(resposta_json, dict):
        return []
    data = resposta_json.get("data", {})
    if isinstance(data, dict):
        return data.get("objects", []) or []
    return []


def _primeiro_objeto(resposta_json: dict) -> dict | None:
    objetos = _extrair_objetos(resposta_json)
    return objetos[0] if objetos else None


@st.cache_data(ttl=86400)
def listar_paises_pt() -> dict[str, str]:
    """Retorna {nome_pt: codigo_alpha_2} de todos os países."""
    resposta = requests.get(
        f"{API_BASE}?response_fields=names,codes.alpha_2,region",
        headers=_headers(),
        timeout=TIMEOUT,
    )
    if resposta.status_code != 200:
        return {}

    paises: dict[str, str] = {}
    for pais in _extrair_objetos(resposta.json()):
        codigo = pais.get("codes", {}).get("alpha_2")
        if not codigo:
            continue
        nome = extrair_nome_pt(pais)
        paises[nome] = codigo

    return dict(sorted(paises.items()))


@st.cache_data(ttl=86400)
def listar_paises_por_regiao() -> dict[str, str]:
    """Retorna {codigo_alpha_2: regiao} para filtro por região."""
    resposta = requests.get(
        f"{API_BASE}?response_fields=codes.alpha_2,region",
        headers=_headers(),
        timeout=TIMEOUT,
    )
    if resposta.status_code != 200:
        return {}

    return {
        p.get("codes", {}).get("alpha_2"): p.get("region")
        for p in _extrair_objetos(resposta.json())
        if p.get("codes", {}).get("alpha_2")
    }


def buscar_por_codigo(codigo: str) -> dict | None:
    resposta = requests.get(
        f"{API_BASE}/codes.alpha_2/{codigo}",
        headers=_headers(),
        timeout=TIMEOUT,
    )
    if resposta.status_code != 200:
        return None
    return _primeiro_objeto(resposta.json())


def buscar_por_nome_pt(termo: str) -> dict | None:
    termo = termo.strip()
    if not termo:
        return None

    resposta = requests.get(
        f"{API_BASE}/names.translations?q={termo}",
        headers=_headers(),
        timeout=TIMEOUT,
    )
    if resposta.status_code == 200:
        pais = _primeiro_objeto(resposta.json())
        if pais:
            return pais

    resposta = requests.get(
        f"{API_BASE}?q={termo}",
        headers=_headers(),
        timeout=TIMEOUT,
    )
    if resposta.status_code != 200:
        return None
    return _primeiro_objeto(resposta.json())


def filtrar_paises_por_regiao(
    paises: dict[str, str], regiao_label: str
) -> dict[str, str]:
    regiao_api = REGIOES_FILTRO.get(regiao_label)
    if not regiao_api:
        return paises

    regioes_por_codigo = listar_paises_por_regiao()
    return {
        nome: codigo
        for nome, codigo in paises.items()
        if regioes_por_codigo.get(codigo) == regiao_api
    }
