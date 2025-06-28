import streamlit as st
import json

# Indlæs data
with open("alle_kvitteringer.json", "r") as f:
    data = json.load(f)

# 🟦 Titel og introduktion
st.set_page_config(page_title="Mit ForbrugsOverblik", layout="centered")
st.title("📊 Mit ForbrugsOverblik")
st.caption("Automatisk scanning og opsamling af dine kvitteringer – helt simpelt")

# 📃 Vis alle kvitteringer i en boks
st.subheader("📋 Registrerede kvitteringer")
with st.expander("Se alle kvitteringer"):
    for kvit in data:
        st.write(f"🧾 {kvit['dato']} — {kvit['belob']} kr")

# 💸 Total
total = sum(k['belob'] for k in data if k['belob'] is not None)
st.metric(label="💰 Totalforbrug", value=f"{total:.2f} kr")

# 📅 Brugervalgt filtrering
st.divider()
st.subheader("📆 Filtrer efter måned og år")
valg = st.text_input("Skriv fx: `03-2025` eller `12-2015`")

if valg:
    fundet = [k for k in data if k['dato'] != "IKKE FUNDET" and valg in k['dato']]
    st.markdown(f"### 🗂️ Resultater for `{valg}`:")
    if fundet:
        for k in fundet:
            st.write(f"🧾 {k['dato']} — {k['belob']} kr")
        delsum = sum(k['belob'] for k in fundet)
        st.success(f"📌 I alt brugt i {valg}: **{delsum:.2f} kr**")
    else:
        st.warning("Ingen kvitteringer fundet for den valgte måned.")
else:
    st.info("Indtast en måned for at filtrere dine køb.")

# Footer
st.divider()
st.caption("Bygget af Egzon • Powered by OCR og Python 🚀")
