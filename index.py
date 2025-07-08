import ollama
import streamlit as st

# Configuração do streamlit
st.set_page_config(
    page_title='Chatbot Local',
    layout='wide'
)

st.markdown("----------")

with st.sidebar:
    st.header("Configurações")

    modelos = ['llama3:8b']

    modelo_selecionado = st.selectbox("Escolha um modelo",
                                      options=modelos,
                                      index=0)
    
    st.markdown("----------")

    # Caso o botão de limpar chat seja acionado
    if st.button('Limpar Chat'):
        st.session_state.messages = []
        st.rerun()

# Caso não tiver mensagem na sessão
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Caso tiver mensagem na sessão
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem aqui: "):
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('user'):
        st.markdown(prompt)
    
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        
        full_response = ''

        try:
            stream = ollama.chat(
                model=modelo_selecionado,
                messages=[
                    {'role': m['role'], 'content': m['content']}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            for chunk in stream:
                if chunk['message']['content']:
                    full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + '')
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Erro: {e}")