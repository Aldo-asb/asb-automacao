import streamlit as st
import requests
import time

st.set_page_config(page_title="ASB Automação")
URL_FB = "https://projeto-asb-comercial-default-rtdb.firebaseio.com/"

def enviar_comando(estado):
    # Envia o comando padrão: LED:ON ou LED:OFF
    requests.put(f"{URL_FB}controle/led.json", json=f"LED:{estado}")

def buscar_dados():
    try:
        temp = requests.get(f"{URL_FB}sensor/valor.json").json()
        status_raw = requests.get(f"{URL_FB}controle/led.json").json()
        status = status_raw.replace("LED:", "") if status_raw else "OFF"
        return temp, status
    except:
        return "--", "OFF"

st.title("🏗️ ASB AUTOMAÇÃO")
temp, status = buscar_dados()

st.metric("Temperatura", f"{temp} °C")
st.write(f"Status: **{status}**")

col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 INICIAR"):
        enviar_comando("ON")
        st.rerun()

with col2:
    if st.button("🔴 PAUSAR"):
        enviar_comando("OFF")
        st.rerun()

time.sleep(3)
st.rerun()
