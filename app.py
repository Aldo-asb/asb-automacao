import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="ASB Automação - Dashboard IHM",
    layout="wide",
    page_icon="⚙️"
)

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

if 'last_status' not in st.session_state:
    st.session_state.last_status = None

# --- ESTILO CSS AVANÇADO (BOTÕES PRETOS COM LED INTERNO) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Estilização do Botão para parecer uma tecla de painel */
    div.stButton > button {
        background-color: #000000 !important;
        color: white !important;
        width: 100%;
        height: 100px;
        border-radius: 12px;
        border: 2px solid #333 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Efeito de brilho ao passar o mouse */
    div.stButton > button:hover {
        border-color: #555 !important;
        background-color: #111 !important;
    }

    /* Círculo do LED dentro do botão (simulado via HTML no texto) */
    .led-btn {
        height: 15px;
        width: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 12px;
        border: 1px solid #000;
    }
    .led-on { background-color: #00FF00; box-shadow: 0 0 12px #00FF00; }
    .led-off { background-color: #FF0000; box-shadow: 0 0 12px #FF0000; }
    .led-null { background-color: #333; }

    .metric-card {
        background-color: #161b22; padding: 20px;
        border-radius: 10px; border-left: 5px solid #00FF00;
        margin-bottom: 10px;
    }
    
    .relogio-container {
        font-family: 'Courier New', monospace; color: #00FF00;
        font-size: 22px; font-weight: bold; text-align: center;
        padding: 8px; background: #000; border-radius: 5px; border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def enviar_comando(estado):
    try:
        st.session_state.last_status = estado
        requests.patch(f"{URL_FB}controle.json", json={"led": estado})
    except:
        st.error("Erro de conexão.")

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_nuvem = requests.get(f"{URL_FB}controle/led.json").json()
        status = st.session_state.last_status if st.session_state.last_status else (status_nuvem if status_nuvem else "OFF")
        return temp if temp else "0.00", status
    except:
        return "---", "OFF"

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("ASB AUTOMAÇÃO")
    st.write("---")
    agora = datetime.now()
    st.write("📅 Data:", agora.strftime("%d/%m/%Y"))
    st.markdown(f'<div class="relogio-container">{agora.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.markdown("## 🏗️ Painel de Operação IHM")

temperatura, status_atual = buscar_dados()

c_temp, c_stat = st.columns(2)
with c_temp:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(label="TEMPERATURA", value=f"{temperatura} °C")
    st.markdown('</div>', unsafe_allow_html=True)
with c_stat:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(label="STATUS ATUAL", value="OPERANDO" if status_atual == "ON" else "PAUSADO")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("### 🛠️ Comandos do Sistema")
col1, col2 = st.columns(2)

# Lógica para os LEDs dentro dos botões
# Criamos uma string HTML que será passada para o label do botão
label_on = "🟢 INICIAR CICLO" if status_atual == "ON" else "⚪ INICIAR CICLO"
label_off = "🔴 PAUSAR CICLO" if status_atual == "OFF" else "⚪ PAUSAR CICLO"

with col1:
    if st.button(label_on):
        enviar_comando("ON")
        st.rerun()

with col2:
    if st.button(label_off):
        enviar_comando("OFF")
        st.rerun()

st.write("---")
st.caption("© 2026 ASB Automação Industrial | v1.5")

# --- ATUALIZAÇÃO ---
st.session_state.last_status = None
time.sleep(2)
st.rerun()
