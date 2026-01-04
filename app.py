import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="ASB Automação")

# URL ORIGINAL
URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- FUNÇÕES ORIGINAIS ---
def enviar_comando(estado):
    try:
        # Volta a enviar para a pasta 'controle' como no início
        requests.put(f"{URL_FB}controle.json", json={"led": estado})
    except:
        pass

def buscar_dados():
    try:
        # Busca temperatura e o dicionário de controle
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        controle = requests.get(f"{URL_FB}controle.json").json()
        
        status = controle.get('led', 'OFF') if controle else "OFF"
        return temp, status
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("ASB AUTOMAÇÃO INDUSTRIAL")

temperatura, status_atual = buscar_dados()

st.subheader(f"Temperatura: {temperatura} °C")
st.write(f"Status: {'OPERANDO' if status_atual == 'ON' else 'PAUSADO'}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    # Apenas adicionando o emoji ao texto original
    label_on = "🟢 INICIAR OPERAÇÃO" if status_atual == "ON" else "⚪ INICIAR OPERAÇÃO"
    if st.button(label_on):
        enviar_comando("ON")
        st.rerun()

with col2:
    label_off = "🔴 PAUSAR OPERAÇÃO" if status_atual == "OFF" else "⚪ PAUSAR OPERAÇÃO"
    if st.button(label_off):
        enviar_comando("OFF")
        st.rerun()

time.sleep(2)
st.rerun()
