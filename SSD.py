import streamlit as st
import requests
import json
import matplotlib.pyplot as plt

# Chave API do usuário
API_KEY = "m09zqIvUzaRmoXDpnES_cT0hT59ajW__15rCrCsQVPNuLM5B0eszpLXPzObpnUYA"

# URL da API do DecisionRules.io (substitua pelo URL correto da sua regra)
API_URL = (
    "https://api.decisionrules.io/rule/solve/06525799-7b9a-9591-e83f-78ce2df04c9c/1"
)


# Função para enviar o arquivo JSON e obter os resultados
def get_results(file_content):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(API_URL, headers=headers, json=file_content)
        print(f"Status da resposta: {response.status_code}")
        print(f"Corpo da resposta: {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Request failed with status code {response.status_code}: {response.text}"
            )
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None


# Função para contar as soluções distintas e criar o gráfico de barras
def plot_solution_counts(results):
    if not results:
        st.error("Não há resultados para processar.")
        return

    try:
        # Contagem das soluções
        count = {}
        for result in results:
            solution = result[0].get(
                "Telemóvel", "N/A"
            )  # Supondo que "Telemóvel" seja o campo de interesse
            if solution in count:
                count[solution] += 1
            else:
                count[solution] = 1

        # Preparação dos dados para o gráfico de barras
        labels = [f"{label}" for i, label in enumerate(count.keys())]
        values = list(count.values())

        # Criando o gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color="blue")
        plt.xlabel("Solução")
        plt.ylabel("Contagem")
        plt.title("Contagem de Soluções Distintas")
        plt.tight_layout()

        # Exibindo o gráfico no Streamlit
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Erro ao processar os resultados: {e}")


# Interface Streamlit
st.title("SSD para escolha de telemóvel")

uploaded_file = st.file_uploader("Escolha um arquivo JSON", type="json")

if uploaded_file is not None:
    try:
        file_content = json.load(uploaded_file)

        results = get_results(file_content)
        if results is not None:
            st.success("Resposta da API:")

            # Exibindo os resultados em uma tabela
            st.subheader("Resultados por Utilizador:")
            for i, result in enumerate(results):
                st.write(f"Utilizador {i + 1}: {result[0].get('Telemóvel', 'N/A')}")

            # Plotando o gráfico de contagem de soluções
            plot_solution_counts(results)

        else:
            st.error("Não foi possível obter os resultados da API.")
    except json.JSONDecodeError:
        st.error("Erro ao ler o arquivo JSON. Verifique se o arquivo é válido.")
