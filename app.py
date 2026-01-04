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
        height: 20px;
        width: 20px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
        border: 2px solid #333;
    }
    .led-verde { 
        background-color: #00FF00; 
        box-shadow: 0 0 12px #00FF00; 
    }
    .led-vermelho { 
        background-color: #FF0000; 
        box-shadow: 0 0 12px #FF0000; 
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
        temp_data = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_data = requests.get(f"{URL_FB}controle/led.json").json()
        
        temp = temp_data if temp_data is not None else "---"
        status = status_data if status_data is not None else "OFF"
        return temp, status
    except:
        return "---", "OFF"

# --- INTERFACE ---
st.title("🏗️ ASB AUTOMAÇÃO INDUSTRIAL")
st.subheader("Supervisório de Monitoramento Térmico")

temperatura, status_atual = buscar_dados()

# --- ÁREA DE INDICADORES (KPIs) ---
col_metric1, col_metric2 = st.columns(2)

with col_metric1:
    st.metric(label="Temperatura Atual", value=f"{temperatura} °C")

with col_metric2:
    if status_atual == "ON":
        status_texto = "SISTEMA OPERANDO"
    elif status_atual == "OFF":
        status_texto = "SISTEMA EM PAUSA"
    else:
        status_texto = "DESLIGADO"
    st.metric(label="Status do Painel", value=status_texto)

st.divider()

# --- ÁREA DE COMANDO COM LÓGICA DE CORES ---
st.write("### Painel de Controle de Operação")
c1, c2 = st.columns(2)

# Lógica das Bolinhas de LED (Feedback Visual)
if status_atual == "ON":
    # Início ativo (Verde), Pausa inativa (Cinza)
    led_on_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-verde"></span><span class="texto-botao" style="color:#00FF00;">OPERANDO</span></div>'
    led_off_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-cinza"></span><span class="texto-botao">AGUARDANDO</span></div>'
elif status_atual == "OFF":
    # Início inativo (Cinza), Pausa ativa (Vermelho)
    led_on_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-cinza"></span><span class="texto-botao">AGUARDANDO</span></div>'
    led_off_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-vermelho"></span><span class="texto-botao" style="color:#FF0000;">PAUSADO</span></div>'
else:
    # Tudo desligado (Cinza)
    led_on_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-cinza"></span><span class="texto-botao">OFF</span></div>'
    led_off_html = f'<div style="margin-bottom:10px;"><span class="led-indicador led-cinza"></span><span class="texto-botao">OFF</span></div>'

with c1:
    st.markdown(led_on_html, unsafe_allow_html=True)
    if st.button("INICIAR OPERAÇÃO"):
        enviar_comando("ON")
        st.rerun()

with c2:
    st.markdown(led_off_html, unsafe_allow_html=True)
    if st.button("PAUSAR OPERAÇÃO"):
        enviar_comando("OFF")
        st.rerun()

# --- ATUALIZAÇÃO AUTOMÁTICA ---
time.sleep(2)
st.rerun()
