import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ASB Automação Industrial", layout="centered")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- ESTILIZAÇÃO PROFISSIONAL (CSS) ---
st.markdown("""
    <style>
    /* Fundo Preto e Texto Branco */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Estilo dos Botões */
    div.stButton > button:first-child {
        height: 4em;
        width: 100%;
        border-radius: 15px;
        border: 2px solid #333;
        background-color: #1A1C24;
        color: white;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }

    /* Indicador de LED (Bolinha) */
    .led-on {
        height: 15px;
        width: 15px;
        background-color: #00FF00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00FF00;
        margin-right: 10px;
    }
    .led-off {
        height: 15px;
        width: 15px;
        background-color: #FF0000;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #FF0000;
        margin-right: 10px;
    }
    .led-idle {
        height: 15px;
        width: 15px;
        background-color: #444;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
    }

    /* Métrica de Temperatura */
    [data-testid="stMetricValue"] {
        color: #00D4FF !important;
        font-size: 48px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def enviar_comando(estado):
    requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")
    requests.put(f"{URL_FB}controle/status_atual.json", json=estado)

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status = requests.get(f"{URL_FB}controle/status_atual.json").json()
        return (temp if temp else "0.00"), (status if status else "OFF")
    except:
        return "--", "OFF"

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center; color: white;'>🏗️ ASB AUTOMAÇÃO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>SISTEMA DE MONITORAMENTO INDUSTRIAL</p>", unsafe_allow_html=True)

temp_atual, status_atual = buscar_dados()

# Display de Temperatura
st.write("")
col_temp = st.columns(1)[0]
with col_temp:
    st.metric(label="TEMPERATURA DO PROCESSO", value=f"{temp_atual} °C")

st.write("---")

# Painel de Controle com LEDs
col1, col2 = st.columns(2)

with col1:
    # Se estiver ligado, mostra o LED verde aceso dentro do botão (simulado com markdown/emoji)
    label_on = "🟢 LIGAR" if status_atual == "ON" else "⚪ LIGAR"
    if st.button(label_on, use_container_width=True):
        enviar_comando("ON")
        st.rerun()
    
    # Bolinha indicadora abaixo do botão
    if status_atual == "ON":
        st.markdown("<div style='text-align:center'><span class='led-on'></span><b style='color:#00FF00'>SISTEMA ATIVO</b></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center'><span class='led-idle'></span></div>", unsafe_allow_html=True)

with col2:
    label_off = "🔴 DESLIGAR" if status_atual == "OFF" else "⚪ DESLIGAR"
    if st.button(label_off, use_container_width=True):
        enviar_comando("OFF")
        st.rerun()
    
    # Bolinha indicadora abaixo do botão
    if status_atual == "OFF":
        st.markdown("<div style='text-align:center'><span class='led-off'></span><b style='color:#FF0000'>SISTEMA PARADO</b></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center'><span class='led-idle'></span></div>", unsafe_allow_html=True)

# Rodapé
st.write("")
st.markdown("<p style='text-align: center; font-size: 12px; color: #555;'>v2.0 - ASB Automação Industrial &copy; 2026</p>", unsafe_allow_html=True)

# Atualização automática
time.sleep(3)
st.rerun()
