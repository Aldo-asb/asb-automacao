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

# Inicializa estados de sessão
if 'status_local' not in st.session_state:
    st.session_state.status_local = None

# --- ESTILO CSS PROFISSIONAL (IDENTIDADE ASB) ---
st.markdown("""
    <style>
    /* Fundo e Container Principal */
    .main {
        background-color: #0e1117;
    }
    
    /* Estilização dos Botões */
    .stButton>button {
        width: 100%;
        height: 70px;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px;
        transition: all 0.3s;
        border: 1px solid #444;
    }
    
    /* Efeito de Hover nos Botões */
    .stButton>button:hover {
        border: 1px solid #00FF00;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
    }

    /* Cards de Informação */
    .metric-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00FF00;
        margin-bottom: 10px;
    }

    /* LEDs Indicadores */
    .led-indicador {
        height: 15px;
        width: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
    }
    .led-verde { background-color: #00FF00; box-shadow: 0 0 15px #00FF00; }
    .led-vermelho { background-color: #FF0000; box-shadow: 0 0 15px #FF0000; }
    .led-cinza { background-color: #333; }

    /* Relógio e Data */
    .relogio-container {
        font-family: 'Courier New', Courier, monospace;
        color: #00FF00;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background: #000;
        border-radius: 5px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def enviar_comando(estado):
    try:
        st.session_state.status_local = estado
        requests.put(f"{URL_FB}controle.json", json={"led": estado})
    except:
        st.error("Falha na comunicação com o servidor.")

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_nuvem = requests.get(f"{URL_FB}controle/led.json").json()
        
        status = st.session_state.status_local if st.session_state.status_local else (status_nuvem if status_nuvem else "OFF")
        return temp if temp else "0.00", status
    except:
        return "ERR", "OFF"

# --- BARRA LATERAL (INFORMAÇÕES DE TEMPO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4252/4252327.png", width=100) # Ícone industrial genérico
    st.title("ASB AUTOMAÇÃO")
    st.write("---")
    
    # Data e Hora em Tempo Real
    agora = datetime.now()
    st.write("📅 **Data de Operação:**")
    st.info(agora.strftime("%d/%m/%Y"))
    
    st.write("⏰ **Relógio do Sistema:**")
    st.markdown(f'<div class="relogio-container">{agora.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.write("v1.2.0 - Dashboard Estável")

# --- CORPO PRINCIPAL ---
st.markdown("## 🏗️ Central de Monitoramento e Controle")
st.write("Monitoramento térmico e gestão de ativos em tempo real.")

temperatura, status_exibido = buscar_dados()

# Colunas de métricas principais
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(label="TEMPERATURA ATUAL", value=f"{temperatura} °C")
    st.markdown('</div>', unsafe_allow_html=True)

with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    texto_status = "OPERANDO" if status_exibido == "ON" else "EM PAUSA"
    st.metric(label="STATUS DO PROCESSO", value=texto_status)
    st.markdown('</div>', unsafe_allow_html=True)

with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(label="CONEXÃO", value="ESTÁVEL")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("### 🛠️ Painel de Comando")
col_btn1, col_btn2 = st.columns(2)

# Lógica de LEDs e Textos
if status_exibido == "ON":
    cor_txt_on, cor_txt_off = "#00FF00", "#555"
    led_on, led_off = "led-verde", "led-cinza"
    msg_on, msg_off = "SISTEMA EM OPERAÇÃO", "STANDBY"
else:
    cor_txt_on, cor_txt_off = "#555", "#FF0000"
    led_on, led_off = "led-cinza", "led-vermelho"
    msg_on, msg_off = "STANDBY", "PROCESSO INTERROMPIDO"

with col_btn1:
    st.markdown(f'<span class="led-indicador {led_on}"></span> <b style="color:{cor_txt_on}">{msg_on}</b>', unsafe_allow_html=True)
    if st.button("🚀 INICIAR CICLO"):
        enviar_comando("ON")
        st.rerun()

with col_btn2:
    st.markdown(f'<span class="led-indicador {led_off}"></span> <b style="color:{cor_txt_off}">{msg_off}</b>', unsafe_allow_html=True)
    if st.button("🛑 PAUSAR CICLO"):
        enviar_comando("OFF")
        st.rerun()

# Rodapé profissional
st.write("---")
st.caption("© 2026 ASB Automação Industrial - Todos os direitos reservados.")

# --- ATUALIZAÇÃO ---
st.session_state.status_local = None
time.sleep(2)
st.rerun()
