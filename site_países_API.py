import streamlit as st
import requests

st.set_page_config(
    page_title="INFOWORLD",
    page_icon="🌍",
    layout="centered"
)

chave_api = st.secrets.get("PAIS_API")

st.title("INFOWORLD 🌍")
st.subheader("Descubra informações sobre qualquer país 🗺️")

# Campo de pesquisa
pais = st.text_input(
    "Digite o nome de um país (em inglês):",
    placeholder="Exemplo: Brazil, Japan, Germany..."
)

if st.button("🔍 Buscar País"):

    if not pais.strip():
        st.warning("⚠️ Digite o nome de um país.")
        st.stop()

    try:
        with st.spinner("Buscando informações..."):
            resposta = requests.get(
                f"https://api.restcountries.com/countries/v5?q={pais}",
                headers={'Authorization': f"Bearer {chave_api}"}, timeout=10
            )

        if resposta.status_code != 200:
            st.error("❌ País não encontrado.")
            st.stop()

        dados = resposta.json()

        # Garante que a API retornou o dicionário e possui objetos na lista
        if not isinstance(dados, dict) or "data" not in dados or not dados["data"].get("objects"):
            st.error("❌ País não encontrado.")
            st.stop()

        # Acessa o primeiro item dentro da nova estrutura
        pais_dados = dados["data"]["objects"][0]

        # Extração de Nome e Emoji
        nome = pais_dados.get("names", {}).get("common", "N/A")
        emoji = pais_dados.get("flag", {}).get("emoji", "")

        # A capital agora é uma lista de dicionários
        capitais_lista = pais_dados.get("capitals", [])
        capital = ", ".join([c.get("name", "N/A") for c in capitais_lista]) if capitais_lista else "N/A"

        regiao = pais_dados.get("region", "N/A")
        subregiao = pais_dados.get("subregion", "N/A")

        populacao = f"{pais_dados.get('population', 0):,}".replace(",", ".")
        
        # A área agora é um dicionário contendo kilometers e miles
        area = f"{pais_dados.get('area', {}).get('kilometers', 0):,.0f}".replace(",", ".")

        # A bandeira agora fica dentro do objeto 'flag'
        bandeira = pais_dados.get("flag", {}).get("url_png")

        # Moedas agora são uma lista de dicionários
        currencies = pais_dados.get("currencies", [])
        if currencies:
            moedas = ", ".join([f"{moeda.get('name', 'N/A')} ({moeda.get('code', '')})" for moeda in currencies])
        else:
            moedas = "N/A"

        # Idiomas agora são uma lista de dicionários
        languages = pais_dados.get("languages", [])
        if languages:
            idiomas = ", ".join([lang.get("name", "N/A") for lang in languages])
        else:
            idiomas = "N/A"

        # Exibição
        if bandeira:
            st.image(bandeira, width=250)

        st.markdown(f"## {emoji} {nome}")

        st.write(f"**Capital:** {capital}")
        st.write(f"**Região:** {regiao}")
        st.write(f"**Sub-região:** {subregiao}")
        st.write(f"**População:** {populacao} habitantes")
        st.write(f"**Área:** {area} km²")
        st.write(f"**Moeda(s):** {moedas}")
        st.write(f"**Idioma(s):** {idiomas}")

        # Mapa - Coordenadas agora são um dicionário {lat: x, lng: y}
        coordenadas = pais_dados.get("coordinates", {})
        lat = coordenadas.get("lat")
        lng = coordenadas.get("lng")

        # Verifica se as coordenadas existem antes de plotar no mapa
        if lat is not None and lng is not None:
            st.map(
                {
                    "lat": [lat],
                    "lon": [lng]
                }
            )

    except requests.exceptions.Timeout:
        st.error("⏳ Tempo de conexão esgotado. Tente novamente.")

    except requests.exceptions.RequestException:
        st.error("❌ Erro ao conectar com a API.")

    except Exception as erro:
        st.error(f"❌ Erro inesperado: {erro}")

else:
    st.info("Digite o nome de um país e clique em Buscar País.")