import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ASB Automação Industrial", layout="wide", page_icon="⚙️")

# URL do seu Firebase (ajustada para o seu projeto)
URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- ESTILO CSS PARA OS BOTÕES E LEDS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
    }
    .led-indicador {
        height: 15px;
        width: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        border: 1px solid #333;
    }
    .led-verde { background-color: #00FF00; box-shadow: 0 0 10px #00FF00; }
    .led-cinza { background-color: #555; }
    </style>
    """, unsafe_allow_status_html=True)

# --- FUNÇÕES DE CONTROLE ---
def enviar_comando(estado):
    requests.put(f"{URL_FB}controle.json", json={"led": estado})

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_led = requests.get(f"{URL_FB}controle/led.json").json()
        return temp, status_led
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("🏗️ ASB AUTOMAÇÃO INDUSTRIAL")
st.subheader("Supervisório de Monitoramento Térmico")

# Busca dados atuais
temperatura, status_atual = buscar_dados()

# --- ÁREA DE INDICADORES (KPIs) ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Temperatura do Sensor", value=f"{temperatura} °C")

with col2:
    status_texto = "OPERANDO" if status_atual == "ON" else "EM PAUSA"
    st.metric(label="Status do Sistema", value=status_texto)

st.divider()

# --- ÁREA DE COMANDO COM LEDS NOS BOTÕES ---
st.write("### Painel de Controle")
c1, c2 = st.columns(2)

# Lógica dos LEDs (Bolinhas)
led_on = '<span class="led-indicador led-verde"></span>' if status_atual == "ON" else '<span class="led-indicador led-cinza"></span>'
led_off = '<span class="led-indicador led-verde"></span>' if status_atual == "OFF" else '<span class="led-indicador led-cinza"></span>'

with c1:
    # Botão de Início
    st.markdown(f"**{led_on} SISTEMA ATIVO**", unsafe_allow_html=True)
    if st.button("INICIAR OPERAÇÃO (ON)"):
        enviar_comando("ON")
        st.rerun()

with c2:
    # Botão de Pausa
    st.markdown(f"**{led_off} SISTEMA EM PAUSA**", unsafe_allow_html=True)
    if st.button("PAUSAR OPERAÇÃO (OFF)"):
        enviar_comando("OFF")
        st.rerun()

# --- ATUALIZAÇÃO AUTOMÁTICA ---
time.sleep(2)
st.rerun()
