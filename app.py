import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="ASB Automação - Dashboard Profissional",
    layout="wide",
    page_icon="⚙️"
)

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- LÓGICA DE MEMÓRIA DE ESTADO (CRUCIAL PARA O SEU ERRO) ---
# Usamos o session_state para garantir que o site "lembre" o que VOCÊ clicou
if 'last_status' not in st.session_state:
    st.session_state.last_status = None

# --- ESTILO CSS PROFISSIONAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; height: 70px;
        font-size: 18px !important; font-weight: bold !important;
        border-radius: 8px; border: 1px solid #444;
    }
    .metric-card {
        background-color: #161b22; padding: 20px;
        border-radius: 10px; border-left: 5px solid #00FF00;
        margin-bottom: 10px;
    }
    .led-indicador {
        height: 18px; width: 18px; border-radius: 50%;
        display: inline-block; margin-right: 10px; vertical-align: middle;
    }
    .led-verde { background-color: #00FF00; box-shadow: 0 0 15px #00FF00; }
    .led-vermelho { background-color: #FF0000; box-shadow: 0 0 15px #FF0000; }
    .led-cinza { background-color: #333; }
    .relogio-container {
        font-family: 'Courier New', monospace; color: #00FF00;
        font-size: 24px; font-weight: bold; text-align: center;
        padding: 10px; background: #000; border-radius: 5px; border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def enviar_comando(estado):
    try:
        # 1. Atualiza a memória local IMEDIATAMENTE
        st.session_state.last_status = estado
        # 2. Envia para a nuvem
        requests.put(f"{URL_FB}controle.json", json={"led": estado})
    except:
        st.error("Erro de conexão com o servidor.")

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_nuvem = requests.get(f"{URL_FB}controle/led.json").json()
        
        # Se acabamos de clicar em algo, ignoramos a nuvem por um tempo para evitar o "pulo"
        if st.session_state.last_status is not None:
            status = st.session_state.last_status
        else:
            status = status_nuvem if status_nuvem else "OFF"
            
        return temp if temp else "0.00", status
    except:
        return "ERR", "OFF"

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("ASB AUTOMAÇÃO")
    st.write("---")
    agora = datetime.now()
    st.write("📅 **Data de Operação:**")
    st.info(agora.strftime("%d/%m/%Y"))
    st.write("⏰ **Relógio do Sistema:**")
    st.markdown(f'<div class="relogio-container">{agora.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.markdown("## 🏗️ Central de Monitoramento ASB")

temperatura, status_atual = buscar_dados()

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(label="TEMPERATURA ATUAL", value=f"{temperatura} °C")
    st.markdown('</div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    status_label = "OPERANDO" if status_atual == "ON" else "EM PAUSA"
    st.metric(label="STATUS DO PROCESSO", value=status_label)
    st.markdown('</div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(label="SISTEMA", value="ONLINE")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("### 🛠️ Painel de Comando")
c1, c2 = st.columns(2)

# Lógica dos LEDs - Agora mais rígida
with c1:
    # LED Verde só acende se for ON
    led_on_class = "led-verde" if status_atual == "ON" else "led-cinza"
    st.markdown(f'<span class="led-indicador {led_on_class}"></span> <b>SISTEMA ATIVO</b>', unsafe_allow_html=True)
    if st.button("🚀 INICIAR OPERAÇÃO"):
        enviar_comando("ON")
        st.rerun()

with c2:
    # LED Vermelho só acende se for OFF
    led_off_class = "led-vermelho" if status_atual == "OFF" else "led-cinza"
    st.markdown(f'<span class="led-indicador {led_off_class}"></span> <b>PROCESSO INTERROMPIDO</b>', unsafe_allow_html=True)
    if st.button("🛑 PAUSAR OPERAÇÃO"):
        enviar_comando("OFF")
        st.rerun()

# Reset da memória local após a interface renderizar
st.session_state.last_status = None

st.write("---")
st.caption("© 2026 ASB Automação Industrial")

time.sleep(2)
st.rerun()
