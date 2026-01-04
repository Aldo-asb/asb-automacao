import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="ASB Automação", layout="wide")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# Funções de comunicação
def enviar_comando(estado):
    try:
        # Envia no formato exato que o seu ESP32 reconhece: LED:ON ou LED:OFF
        requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")
    except:
        pass

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_raw = requests.get(f"{URL_FB}controle/led.json").json()
        status = status_raw.replace("LED:", "") if status_raw else "OFF"
        return (temp if temp else "--"), status
    except:
        return "--", "OFF"

# Interface
st.title("🏗️ ASB AUTOMAÇÃO INDUSTRIAL")

temp_atual, status_atual = buscar_dados()

# Exibição dos dados
c1, c2 = st.columns(2)
with c1:
    st.metric("Temperatura", f"{temp_atual} °C")
with c2:
    st.write(f"Sistema em estado: **{status_atual}**")

st.divider()

# Botões de controle
col1, col2 = st.columns(2)
with col1:
    if st.button(f"🟢 INICIAR OPERAÇÃO"):
        enviar_comando("ON")
        st.rerun()

with col2:
    if st.button(f"🔴 PAUSAR OPERAÇÃO"):
        enviar_comando("OFF")
        st.rerun()

# Atualização automática a cada 3 segundos
time.sleep(3)
st.rerun()
