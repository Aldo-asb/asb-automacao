import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="ASB Automação")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- FUNÇÕES ---
def enviar_comando(estado):
    try:
        requests.put(f"{URL_FB}controle/led.json", json=estado)
    except:
        pass

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status = requests.get(f"{URL_FB}controle/led.json").json()
        return temp, status
    except:
        return "---", "OFF"

# --- INTERFACE (SIMPLES E DIRETA) ---
st.title("ASB AUTOMAÇÃO INDUSTRIAL")

temperatura, status_atual = buscar_dados()

# Exibição simples
st.subheader(f"Temperatura: {temperatura} °C")
st.write(f"Status Atual: {'OPERANDO' if status_atual == 'ON' else 'PAUSADO'}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    # LED Verde dentro do botão quando ligado
    label_on = "🟢 INICIAR OPERAÇÃO" if status_atual == "ON" else "⚪ INICIAR OPERAÇÃO"
    if st.button(label_on):
        enviar_comando("ON")
        st.rerun()

with col2:
    # LED Vermelho dentro do botão quando pausado
    label_off = "🔴 PAUSAR OPERAÇÃO" if status_atual == "OFF" else "⚪ PAUSAR OPERAÇÃO"
    if st.button(label_off):
        enviar_comando("OFF")
        st.rerun()

# Atualização automática
time.sleep(2)
st.rerun()
