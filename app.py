import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ASB AUTOMAÇÃO", layout="wide")

# --- URL DO SEU GOOGLE FIREBASE ---
URL_BASE = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"
if not URL_BASE.endswith('/'): URL_BASE += '/'

# --- ESTILO PROFISSIONAL (CSS CUSTOMIZADO) ---
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp { background-color: #0E1117; }
    
    /* Estilo do Card de Temperatura */
    .temp-card {
        background-color: #161B22;
        border: 2px solid #30363D;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    .temp-valor {
        color: #00FF00;
        font-size: 70px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    
    .temp-label {
        color: #8B949E;
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Botões Industriais */
    div.stButton > button {
        height: 80px;
        font-size: 25px !important;
        font-weight: bold;
        border-radius: 10px;
        text-transform: uppercase;
    }
    
    /* Botão LIGAR (Verde) */
    .stBtnLigar > div > button {
        background-color: #238636 !important;
        color: white !important;
        border: none;
    }
    
    /* Botão DESLIGAR (Vermelho) */
    .stBtnDesligar > div > button {
        background-color: #DA3633 !important;
        color: white !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: white;'>ASB AUTOMAÇÃO INDUSTRIAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8B949E;'>SISTEMA DE MONITORAMENTO REMOTO IOT</p>", unsafe_allow_html=True)
st.divider()

# --- BUSCA DE DADOS ---
try:
    res = requests.get(f"{URL_BASE}sensor.json").json()
    temp_valor = res.get("valor") or res.get("temperatura") or "00.0"
except:
    temp_valor = "ERR"

# --- LAYOUT PRINCIPAL ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # Card de Temperatura Profissional
    st.markdown(f"""
        <div class="temp-card">
            <div class="temp-label">Temperatura do Processo</div>
            <div class="temp-valor">{temp_valor}°C</div>
            <div style='color: #58A6FF;'>● MONITORANDO EM TEMPO REAL</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<p style='color: white; font-weight: bold;'>CONTROLE DE ATUADORES</p>", unsafe_allow_html=True)
    
    # Botão Ligar
    st.markdown('<div class="stBtnLigar">', unsafe_allow_html=True)
    if st.button("▶ INICIAR OPERAÇÃO (ON)", key="btn_on", use_container_width=True):
        requests.put(f"{URL_BASE}controle.json", json={"led": "ON"})
        st.toast("Comando ON enviado!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("") # Espaço

    # Botão Desligar
    st.markdown('<div class="stBtnDesligar">', unsafe_allow_html=True)
    if st.button("⏹ PARADA DE EMERGÊNCIA (OFF)", key="btn_off", use_container_width=True):
        requests.put(f"{URL_BASE}controle.json", json={"led": "OFF"})
        st.toast("Comando OFF enviado!")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
# Barra de status no rodapé
st.markdown(f"<p style='text-align: right; color: #8B949E;'>Sincronizado com Firebase: {time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# Auto-refresh simples (Opcional: atualiza a cada 5 segundos se quiser)
# time.sleep(5)
# st.rerun()