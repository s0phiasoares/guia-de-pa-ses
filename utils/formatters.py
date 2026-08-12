REGIOES_PT = {
    "Africa": "África",
    "Americas": "Américas",
    "Asia": "Ásia",
    "Europe": "Europa",
    "Oceania": "Oceania",
    "Antarctic": "Antártida",
}

SUBREGIOES_PT = {
    "Northern Africa": "Norte da África",
    "Western Africa": "África Ocidental",
    "Middle Africa": "África Central",
    "Eastern Africa": "África Oriental",
    "Southern Africa": "África Austral",
    "Northern America": "América do Norte",
    "Central America": "América Central",
    "Caribbean": "Caribe",
    "South America": "América do Sul",
    "Central Asia": "Ásia Central",
    "Eastern Asia": "Ásia Oriental",
    "South-Eastern Asia": "Sudeste Asiático",
    "Southern Asia": "Ásia Meridional",
    "Western Asia": "Ásia Ocidental",
    "Northern Europe": "Europa do Norte",
    "Western Europe": "Europa Ocidental",
    "Eastern Europe": "Europa Oriental",
    "Southern Europe": "Europa do Sul",
    "Australia and New Zealand": "Austrália e Nova Zelândia",
    "Melanesia": "Melanésia",
    "Micronesia": "Micronésia",
    "Polynesia": "Polinésia",
}


def extrair_nome_pt(pais_dados: dict) -> str:
    traducoes = pais_dados.get("names", {}).get("translations", {})
    nome_pt = traducoes.get("por", {}).get("common")
    if nome_pt:
        return nome_pt
    return pais_dados.get("names", {}).get("common", "N/A")


def extrair_emoji(pais_dados: dict) -> str:
    return pais_dados.get("flag", {}).get("emoji", "")


def extrair_capital(pais_dados: dict) -> str:
    capitais = pais_dados.get("capitals", [])
    if not capitais:
        return "N/A"
    return ", ".join(c.get("name", "N/A") for c in capitais)


def formatar_populacao(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


def formatar_area(pais_dados: dict) -> str:
    km = pais_dados.get("area", {}).get("kilometers", 0)
    return f"{km:,.0f}".replace(",", ".")


def formatar_regiao(regiao: str) -> str:
    return REGIOES_PT.get(regiao, regiao)


def formatar_subregiao(subregiao: str) -> str:
    return SUBREGIOES_PT.get(subregiao, subregiao)


def extrair_moedas(pais_dados: dict) -> str:
    currencies = pais_dados.get("currencies", [])
    if not currencies:
        return "N/A"
    return ", ".join(
        f"{moeda.get('name', 'N/A')} ({moeda.get('code', '')})"
        for moeda in currencies
    )


def extrair_idiomas(pais_dados: dict) -> str:
    languages = pais_dados.get("languages", [])
    if not languages:
        return "N/A"
    return ", ".join(lang.get("name", "N/A") for lang in languages)


def extrair_bandeira_url(pais_dados: dict) -> str | None:
    return pais_dados.get("flag", {}).get("url_png")


def extrair_coordenadas(pais_dados: dict) -> tuple[float | None, float | None]:
    coords = pais_dados.get("coordinates", {})
    return coords.get("lat"), coords.get("lng")
