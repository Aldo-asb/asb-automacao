import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ASB Automação Industrial", layout="wide", page_icon="⚙️")

# URL do seu Firebase
URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# --- ESTILO CSS PARA OS BOTÕES E LEDS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 10px;
    }
    .led-indicador {
        height: 18px;
        width: 18px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
        border: 2px solid #333;
    }
    .led-verde { 
        background-color: #00FF00; 
        box-shadow: 0 0 10px #00FF00; 
    }
    .led-cinza { 
        background-color: #444; 
    }
    .texto-botao {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE CONTROLE ---
def enviar_comando(estado):
    try:
        requests.put(f"{URL_FB}controle.json", json={"led": estado})
    except:
        st.error("Erro ao conectar com o Firebase")

def buscar_dados():
    try:
        # Busca temperatura e status do LED
        temp_data = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_data = requests.get(f"{URL_FB}controle/led.json").json()
        
        # Garante que sempre teremos um valor exibível
        temp = temp_data if temp_data is not None else "---"
        status = status_data if status_data is not None else "OFF"
        return temp, status
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("🏗️ ASB AUTOMAÇÃO INDUSTRIAL")
st.subheader("Supervisório de Monitoramento Térmico")

# Busca dados atuais
temperatura, status_atual = buscar_dados()

# --- ÁREA DE INDICADORES (KPIs) ---
col_metric1, col_metric2 = st.columns(2)

with col_metric1:
    st.metric(label="Temperatura Atual", value=f"{temperatura} °C")

with col_metric2:
    status_texto = "OPERANDO" if status_atual == "ON" else "EM PAUSA"
    st.metric(label="Status do Sistema", value=status_texto)

st.divider()

# --- ÁREA DE COMANDO COM LEDS INDICADORES ---
st.write("### Painel de Controle de Operação")
c1, c2 = st.columns(2)

# Lógica das Bolinhas de LED
if status_atual == "ON":
    led_on_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-verde"></span><span class="texto-botao">SISTEMA ATIVO</span></div>'
    led_off_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-cinza"></span><span class="texto-botao">DESATIVADO</span></div>'
else:
    led_on_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-cinza"></span><span class="texto-botao">DESATIVADO</span></div>'
    led_off_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-verde"></span><span class="texto-botao">SISTEMA EM PAUSA</span></div>'

with c1:
    st.markdown(led_on_html, unsafe_allow_html=True)
    if st.button("INICIAR OPERAÇÃO (ON)"):
        enviar_comando("ON")
        st.rerun()

with c2:
    st.markdown(led_off_html, unsafe_allow_html=True)
    if st.button("PAUSAR OPERAÇÃO (OFF)"):
        enviar_comando("OFF")
        st.rerun()

# --- ATUALIZAÇÃO AUTOMÁTICA ---
# Delay menor para parecer mais tempo real (2 segundos)
time.sleep(2)
st.rerun()
