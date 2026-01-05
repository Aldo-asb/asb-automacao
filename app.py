import streamlit as st
import requests
import time

# Configuração de Interface Industrial
st.set_page_config(page_title="ASB Automação Industrial", layout="centered")

# Estilo CSS para melhorar os botões
st.markdown("""
    <style>
    div.stButton > button:first-child { height: 3em; font-size: 20px; font-weight: bold; border-radius: 10px; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #d1d5db; }
    </style>
    """, unsafe_allow_html=True)

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

def enviar_comando(estado):
    requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_raw = requests.get(f"{URL_FB}controle/led.json").json()
        status = status_raw.replace("LED:", "") if status_raw else "OFF"
        return temp, status
    except:
        return "--", "OFF"

st.title("🏗️ ASB AUTOMAÇÃO")
st.write("---")

temp_atual, status_atual = buscar_dados()

# Mostrador de Temperatura em destaque
col_info = st.columns(1)[0]
with col_info:
    st.metric(label="TEMPERATURA DO PROCESSO", value=f"{temp_atual} °C")

st.write(f"Status Atual: :blue[**{status_atual}**]")
st.write("---")

# Botões Grandes e Coloridos
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 INICIAR", use_container_width=True, type="primary"):
        enviar_comando("ON")
        st.toast("Comando de Partida Enviado!")
        time.sleep(0.5)
        st.rerun()

with col2:
    if st.button("🛑 PARAR", use_container_width=True):
        enviar_comando("OFF")
        st.toast("Comando de Parada Enviado!")
        time.sleep(0.5)
        st.rerun()

# Atualização rápida da tela
time.sleep(2)
st.rerun()
