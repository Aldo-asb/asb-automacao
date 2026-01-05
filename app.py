import streamlit as st
import requests
import time

st.set_page_config(page_title="ASB Automação Industrial", layout="centered")

URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

# Estilo para os botões
st.markdown("""
    <style>
    div.stButton > button:first-child { height: 3em; font-size: 18px; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

def enviar_comando(estado):
    requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")
    # Salva o último estado para a interface não se perder
    requests.put(f"{URL_FB}controle/status_atual.json", json=estado)

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status = requests.get(f"{URL_FB}controle/status_atual.json").json()
        return (temp if temp else "--"), (status if status else "OFF")
    except:
        return "--", "OFF"

st.title("🏗️ ASB AUTOMAÇÃO")

temp_atual, status_atual = buscar_dados()

# Interface mais limpa
st.metric(label="TEMPERATURA DO PROCESSO", value=f"{temp_atual} °C")
st.subheader(f"Sistema está: {status_atual}")

st.write("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 LIGAR", use_container_width=True, type="primary"):
        enviar_comando("ON")
        st.rerun()

with col2:
    if st.button("🔴 DESLIGAR", use_container_width=True):
        enviar_comando("OFF")
        st.rerun()

time.sleep(2)
st.rerun()
