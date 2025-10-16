import streamlit as st
import requests 

st.title("INFOWORLD 🌍")
st.subheader ("Descubra informações sobre o país desejado 😁🗺️")


país = st.text_input("Digite o nome de um país:", placeholder="Exemplo: Brazil, Japan, Germany...")

# Quando o usuário digitar algo
if país:
    resposta = requests.get("https://restcountries.com/v3.1/name/{país}")

    if resposta.status_code == 200:
        dados = resposta.json()

        # Pega o primeiro resultado da API
        pais_dados = dados[0]

        nome = pais_dados["name"]["common"]
        capital = pais_dados.get("capital", ["N/A"])[0]
        regiao = pais_dados.get("region", "N/A")
        subregiao = pais_dados.get("subregion", "N/A")
        populacao = f"{pais_dados.get('population', 0):,}".replace(",", ".")
        area = f"{pais_dados.get('area', 0):,}".replace(",", ".")
        bandeira = pais_dados["flags"]["png"]
        moedas = ", ".join(pais_dados.get("currencies", {}).keys())
        idiomas = ", ".join(pais_dados.get("languages", {}).values())

        # Exibe resultados
        st.image(bandeira, width=250)
        st.markdown(f"### 🗺️ {nome}")
        st.write(f"**Capital:** {capital}")
        st.write(f"**Região:** {regiao}")
        st.write(f"**Sub-região:** {subregiao}")
        st.write(f"**População:** {populacao} habitantes")
        st.write(f"**Área:** {area} km²")
        st.write(f"**Moeda(s):** {moedas}")
        st.write(f"**Idioma(s):** {idiomas}")

    else:
        st.error("❌ País não encontrado. Verifique o nome e tente novamente.")
else:
    st.info("Digite o nome de um país acima para começar.")