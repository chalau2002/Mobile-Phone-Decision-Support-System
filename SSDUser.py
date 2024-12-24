import streamlit as st
import requests
import json

# Chave API do usuário
API_KEY = "m09zqIvUzaRmoXDpnES_cT0hT59ajW__15rCrCsQVPNuLM5B0eszpLXPzObpnUYA"

# URL da API do DecisionRules.io (substitua pelo URL correto da sua regra)
API_URL = (
    "https://api.decisionrules.io/rule/solve/06525799-7b9a-9591-e83f-78ce2df04c9c/1"
)


# Função para enviar o arquivo JSON e obter os resultados
def get_results(data):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(API_URL, headers=headers, json=data)
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


# Interface Streamlit
st.title("SSD para escolha de telemóvel")

# Formulário de entrada de dados
with st.form("user_form"):
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    condicao_financeira = st.text_input("Condição Financeira")
    desastrado = st.text_input("Desastrado")
    entusiasta_tecnologia = st.text_input("Entusiasta de Tecnologia")
    preocupado_sustentabilidade = st.text_input("Preocupado Com Sustentabilidade")
    hobbies = st.text_input("Hobbies")
    viajante = st.text_input("Viajante")
    profissao_ocupacao = st.text_input("Profissão/Ocupação")
    limitacoes = st.text_input("Limitações")

    # Botão de submissão
    submit_button = st.form_submit_button(label="Submeter")

if submit_button:
    # Construindo o JSON a partir dos inputs do formulário
    user_data = {
        "Idade": idade,
        "Condição Financeira": condicao_financeira,
        "Desastrado": desastrado,
        "Entusiasta de Tecnologia": entusiasta_tecnologia,
        "Preocupado Com Sustentabilidade": preocupado_sustentabilidade,
        "Hobbies": hobbies,
        "Viajante": viajante,
        "Profissão/Ocupação": profissao_ocupacao,
        "Limitações": limitacoes,
    }

    # Estrutura de dados conforme esperado pela API
    data_to_send = {"data": [user_data]}

    # Enviando os dados para a API e obtendo resultados
    results = get_results(data_to_send)

    if results is not None:
        st.success("Resposta da API:")

        # Exibindo os resultados em uma tabela
        st.subheader("Resultados:")
        for result in results:
            if isinstance(result, list) and result:
                telemovel = result[0].get("Telemóvel", "N/A")
                preco = result[0].get("Preço", "N/A")
                imagem = result[0].get("Imagem", None)
                descricao = result[0].get("Descrição", "N/A")

                st.write(f"Telemóvel Sugerido: {telemovel}")
                st.write(f"Preço: {preco}")

                if imagem:
                    st.image(imagem, caption=f"Imagem do {telemovel}")
                st.write(descricao)
    else:
        st.error("Não foi possível obter os resultados da API.")
