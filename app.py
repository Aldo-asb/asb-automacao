import streamlit as st
import requests
import time

st.set_page_config(page_title="ASB Automação", layout="centered")
URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

def enviar_comando(estado):
    # Envia o comando e limpa o cache do Streamlit para garantir o envio
    requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")

st.title("🏗️ ASB AUTOMAÇÃO")

# Busca temperatura
try:
    temp = requests.get(f"{URL_FB}sensor/valor.json").json()
    st.metric("TEMPERATURA ATUAL", f"{temp} °C")
except:
    st.write("Aguardando sensor...")

st.write("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 LIGAR", use_container_width=True):
        enviar_comando("ON")
        st.success("Comando ON enviado")
        time.sleep(0.5)
        st.rerun()

with col2:
    if st.button("🔴 DESLIGAR", use_container_width=True):
        enviar_comando("OFF")
        st.success("Comando OFF enviado")
        time.sleep(0.5)
        st.rerun()

time.sleep(3)
st.rerun()
