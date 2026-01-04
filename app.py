import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="ASB Automação - IHM", layout="wide")
URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- ESTILO IHM PRETO ---
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #000000 !important;
        color: white !important;
        width: 100%; height: 100px;
        border-radius: 12px; border: 2px solid #333 !important;
        font-size: 20px !important; font-weight: bold !important;
    }
    .metric-card {
        background-color: #161b22; padding: 20px;
        border-radius: 10px; border-left: 5px solid #00FF00;
    }
    </style>
    """, unsafe_allow_html=True)

def enviar_comando(estado):
    try:
        # Força a atualização do campo 'led' sem apagar outros campos
        requests.patch(f"{URL_FB}controle.json", json={"led": estado})
        st.success(f"Comando {estado} enviado!")
    except:
        st.error("Erro de conexão")

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status = requests.get(f"{URL_FB}controle/led.json").json()
        return (temp if temp else "0.00"), (status if status else "OFF")
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("🏗️ ASB IHM PROFISSIONAL")
temperatura, status_atual = buscar_dados()

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card">TEMPERATURA: {temperatura} °C</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card">STATUS: {"OPERANDO" if status_atual == "ON" else "PAUSADO"}</div>', unsafe_allow_html=True)

st.write("---")

c1, c2 = st.columns(2)
# O LED agora é parte do texto do botão
with c1:
    label_on = "🟢 CICLO ATIVO" if status_atual == "ON" else "⚪ INICIAR CICLO"
    if st.button(label_on):
        enviar_comando("ON")
        st.rerun()

with c2:
    label_off = "🔴 CICLO PAUSADO" if status_atual == "OFF" else "⚪ PAUSAR CICLO"
    if st.button(label_off):
        enviar_comando("OFF")
        st.rerun()

time.sleep(2)
st.rerun()
