import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="ASB Automação")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- FUNÇÕES ---
def enviar_comando(estado):
    try:
        # Mantendo o padrão exato exigido pelo seu ESP32: LED:ON ou LED:OFF
        comando_completo = f"LED:{estado}"
        requests.put(f"{URL_FB}controle/led.json", json=comando_completo)
    except:
        pass

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_raw = requests.get(f"{URL_FB}controle/led.json").json()
        
        # Apenas remove o prefixo para mostrar no site de forma limpa
        status = status_raw.replace("LED:", "") if status_raw else "OFF"
        return temp, status
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("ASB AUTOMAÇÃO INDUSTRIAL")

temperatura, status_atual = buscar_dados()

st.subheader(f"Temperatura: {temperatura} °C")
st.write(f"Status Atual: **{status_atual}**")

st.divider()

col1, col2 = st.columns(2)

with col1:
    # Apenas o LED (emoji) dentro do botão conforme sua solicitação
    label_on = "🟢 INICIAR OPERAÇÃO" if status_atual == "ON" else "⚪ INICIAR OPERAÇÃO"
    if st.button(label_on):
        enviar_comando("ON")
        st.rerun()

with col2:
    label_off = "🔴 PAUSAR OPERAÇÃO" if status_atual == "OFF" else "⚪ PAUSAR OPERAÇÃO"
    if st.button(label_off):
        enviar_comando("OFF")
        st.rerun()

# Atualização automática simples
time.sleep(3)
st.rerun()
