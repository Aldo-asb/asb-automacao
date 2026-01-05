import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="ASB Automação", layout="wide")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

def enviar_comando(estado):
    try:
        # Envia no formato que o seu ESP32 já reconhece
        requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")
    except:
        pass

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_raw = requests.get(f"{URL_FB}controle/led.json").json()
        # Limpa o texto para mostrar apenas ON ou OFF
        status = status_raw.replace("LED:", "") if status_raw else "OFF"
        return temp, status
    except:
        return "--", "OFF"

st.title("🏗️ ASB AUTOMAÇÃO INDUSTRIAL")

temp_atual, status_atual = buscar_dados()

st.metric("TEMPERATURA ATUAL", f"{temp_atual} °C")
st.write(f"O LED está: **{status_atual}**")

st.divider()

col1, col2 = st.columns(2)

with col1:
    # Botão Iniciar
    if st.button("🟢 INICIAR OPERAÇÃO (ON)", use_container_width=True):
        enviar_comando("ON")
        st.rerun()

with col2:
    # Botão Pausar
    if st.button("🔴 PAUSAR OPERAÇÃO (OFF)", use_container_width=True):
        enviar_comando("OFF")
        st.rerun()

# Atualização automática
time.sleep(3)
st.rerun()
