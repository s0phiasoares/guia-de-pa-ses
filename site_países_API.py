
import streamlit as st
import requests

st.set_page_config(
    page_title="INFOWORLD",
    page_icon="🌍",
    layout="centered"
)

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
                f"https://restcountries.com/v3.1/name/{pais.strip()}",
                timeout=10
            )

        if resposta.status_code != 200:
            st.error("❌ País não encontrado.")
            st.stop()

        dados = resposta.json()

        # Garante que a API retornou uma lista válida
        if not isinstance(dados, list) or len(dados) == 0:
            st.error("❌ País não encontrado.")
            st.stop()

        pais_dados = dados[0]

        nome = pais_dados.get("name", {}).get("common", "N/A")
        emoji = pais_dados.get("flag", "")

        capital = ", ".join(
            pais_dados.get("capital", ["N/A"])
        )

        regiao = pais_dados.get("region", "N/A")
        subregiao = pais_dados.get("subregion", "N/A")

        populacao = f"{pais_dados.get('population', 0):,}".replace(",", ".")

        area = f"{pais_dados.get('area', 0):,.0f}".replace(",", ".")

        bandeira = pais_dados.get("flags", {}).get("png")

        # Moedas
        currencies = pais_dados.get("currencies", {})

        if currencies:
            moedas = ", ".join(
                [
                    f"{info.get('name', codigo)} ({codigo})"
                    for codigo, info in currencies.items()
                ]
            )
        else:
            moedas = "N/A"

        # Idiomas
        idiomas = ", ".join(
            pais_dados.get("languages", {}).values()
        ) or "N/A"

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

        # Mapa
        coordenadas = pais_dados.get("latlng", [])

        if len(coordenadas) == 2:
            st.map(
                {
                    "lat": [coordenadas[0]],
                    "lon": [coordenadas[1]]
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
```
