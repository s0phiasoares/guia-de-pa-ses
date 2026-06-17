import streamlit as st
import requests

st.title("INFOWORLD 🌍")
st.subheader("Descubra informações sobre o país que você deseja pesquisar 🗺️")

# Entrada de texto
pais = st.text_input(
    "Digite o nome de um país (em inglês):",
    placeholder="Exemplo: Brazil, Japan, Germany..."
)

# Botão para buscar
if st.button("🔍 Buscar País"):
    if pais:
        pais = pais.strip()

        try:
            with st.spinner("Buscando informações..."):
                resposta = requests.get(
                    f"https://restcountries.com/v3.1/name/{pais}?fullText=true",
                    timeout=10
                )

            if resposta.status_code == 200:
                dados = resposta.json()

                # Verifica se a resposta é uma lista válida
                if isinstance(dados, list) and len(dados) > 0:

                    pais_dados = dados[0]

                    nome = pais_dados.get("name", {}).get("common", "N/A")
                    capital = ", ".join(
                        pais_dados.get("capital", ["N/A"])
                    )
                    regiao = pais_dados.get("region", "N/A")
                    subregiao = pais_dados.get("subregion", "N/A")

                    populacao = f"{pais_dados.get('population', 0):,}".replace(",", ".")
                    area = f"{pais_dados.get('area', 0):,}".replace(",", ".")

                    bandeira = pais_dados.get("flags", {}).get("png", "")

                    currencies = pais_dados.get("currencies", {})
                    moedas = ", ".join(
                        [
                            f"{info.get('name', codigo)} ({codigo})"
                            for codigo, info in currencies.items()
                        ]
                    ) or "N/A"

                    idiomas = ", ".join(
                        pais_dados.get("languages", {}).values()
                    ) or "N/A"

                    emoji = pais_dados.get("flag", "")

                    # Exibe resultados
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

                else:
                    st.error("❌ País não encontrado.")

            elif resposta.status_code == 404:
                st.error("❌ País não encontrado.")

            else:
                st.error("❌ Erro ao consultar a API.")

        except requests.exceptions.Timeout:
            st.error("⏳ A consulta demorou muito. Tente novamente.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro de conexão: {e}")

        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")

    else:
        st.warning("⚠️ Por favor, digite o nome de um país antes de buscar.")

else:
    st.info("Digite o nome de um país e clique em **Buscar País** para começar.")
