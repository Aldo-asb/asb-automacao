import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="ASB Automação")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- FUNÇÕES ---
def enviar_comando(estado):
    try:
        # Envia o comando para a pasta controle
        requests.put(f"{URL_FB}controle.json", json={"led": estado})
    except:
        pass

def buscar_dados():
    try:
        # Busca temperatura e status
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        controle = requests.get(f"{URL_FB}controle.json").json()
        
        status = controle.get('led', 'OFF') if controle else "OFF"
        return temp, status
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("ASB AUTOMAÇÃO INDUSTRIAL")

temperatura, status_atual = buscar_dados()

# Mostra os dados de forma fixa para evitar o erro de 'removeChild'
st.metric(label="Temperatura Atual", value=f"{temperatura} °C")
st.write(f"Sistema está atualmente: **{status_atual}**")

st.divider()

col1, col2 = st.columns(2)

with col1:
    label_on = "🟢 INICIAR OPERAÇÃO" if status_atual == "ON" else "⚪ INICIAR OPERAÇÃO"
    if st.button(label_on, key="btn_on"):
        enviar_comando("ON")
        st.rerun()

with col2:
    label_off = "🔴 PAUSAR OPERAÇÃO" if status_atual == "OFF" else "⚪ PAUSAR OPERAÇÃO"
    if st.button(label_off, key="btn_off"):
        enviar_comando("OFF")
        st.rerun()

# --- ATUALIZAÇÃO AUTOMÁTICA SEGURA ---
# Usamos um tempo um pouco maior (3 segundos) para não dar conflito no navegador
time.sleep(3)
st.rerun()
