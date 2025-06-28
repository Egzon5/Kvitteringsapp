import streamlit as st
from PIL import Image
import pytesseract
import json
import re
import os
import datetime
import pandas as pd

# Opsætning
st.set_page_config(page_title="KvitteringsApp", layout="centered")
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

DATAFIL = "alle_kvitteringer.json"

# --- Hjælpefunktioner ---
def load_data():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r") as f:
            return json.load(f)
    return []

def save_data(postering):
    data = load_data()
    data.append(postering)
    with open(DATAFIL, "w") as f:
        json.dump(data, f, indent=2)

def extract_data_from_image(img):
    text = pytesseract.image_to_string(img, lang="dan")
    belob_match = re.search(r"TOTAL.?[:\s]*([0-9]+[.,][0-9]{2})", text.upper())
    belob = belob_match.group(1).replace(",", ".") if belob_match else None

    dato_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
    dato = dato_match.group(0) if dato_match else None

    varelinjer = []
    for linje in text.splitlines():
        match = re.search(r"(.+?)\s+([0-9]+[.,][0-9]{2})$", linje)
        if match:
            navn = match.group(1).strip().upper()
            pris = float(match.group(2).replace(",", "."))
            kategori = gæt_kategori(navn)
            varelinjer.append({"vare": navn, "pris": pris, "kategori": kategori})

    return {
        "dato": dato,
        "belob": float(belob) if belob else None,
        "varer": varelinjer
    }

def gæt_kategori(navn):
    if "PIZZA" in navn or "BURGER" in navn or "SNACK" in navn:
        return "mad"
    elif "COLA" in navn or "VAND" in navn or "ØL" in navn:
        return "drikke"
    elif "TAPE" in navn or "LABELS" in navn or "PEN" in navn:
        return "kontor"
    else:
        return "andet"

# --- UI ---

st.title("📸 KvitteringsApp med Upload, Kategorier og Grafik")

# 🔼 1. Upload og scanning
st.header("1️⃣ Upload kvittering")

uploaded_file = st.file_uploader("Upload billede (JPG eller PNG)", type=["jpg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Din kvittering", use_container_width=True)
    


    if st.button("🔍 Scan og gem kvittering"):
        result = extract_data_from_image(image)
        save_data(result)
        st.success("✅ Kvittering gemt!")
        st.write(result)

# 📊 2. Graf og oversigt
st.header("2️⃣ Overblik over dine køb")
data = load_data()

if data:
    df = pd.DataFrame(data)
    df = df.dropna(subset=["dato", "belob"])
    df["måned"] = df["dato"].apply(lambda d: "-".join(d.split("-")[1:3]))  # fx "03-2025"

    st.subheader("📈 Forbrug pr. måned")
    måned_total = df.groupby("måned")["belob"].sum()
    st.bar_chart(måned_total)

    st.subheader("📋 Alle køb (seneste først)")
    st.dataframe(df.sort_values("dato", ascending=False))

    # 🏷️ 3. Vis kategorier
    st.subheader("🏷️ Varetyper og kategorier")
    vare_data = []
    for post in data:
        for v in post.get("varer", []):
            vare_data.append(v)
    if vare_data:
        vare_df = pd.DataFrame(vare_data)
        st.dataframe(vare_df)
        kategori_total = vare_df.groupby("kategori")["pris"].sum()
        st.subheader("📊 Forbrug fordelt på kategorier")
        st.bar_chart(kategori_total)
else:
    st.info("Ingen kvitteringer endnu. Upload din første ovenfor 👆")
