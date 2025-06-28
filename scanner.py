from PIL import Image
import pytesseract
import re
import json
import os

# Fortæl hvor tesseract ligger
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Åbn billedet
img = Image.open("/Users/egzon/Desktop/kvittering.jpg")

# Læs teksten
text = pytesseract.image_to_string(img, lang="dan")

# Vis hele teksten (valgfrit)
print("🔍 Hele kvitteringsteksten:")
print(text)

# Find beløb
belob_match = re.search(r"TOTAL.?[:\s]*([0-9]+[.,][0-9]{2})", text.upper())
belob = belob_match.group(1).replace(",", ".") if belob_match else "IKKE FUNDET"

# Find dato
dato_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
dato = dato_match.group(0) if dato_match else "IKKE FUNDET"

# Vis resultat
print("\n✅ Fundet information:")
print(f"Dato: {dato}")
print(f"Beløb: {belob} kr")

# Klar data som dictionary
ny_postering = {
    "dato": dato,
    "belob": float(belob) if belob != "IKKE FUNDET" else None
}

# Filnavn
filnavn = "alle_kvitteringer.json"

# Hvis filen findes, læs den – ellers start med tom liste
if os.path.exists(filnavn):
    with open(filnavn, "r") as f:
        data = json.load(f)
else:
    data = []

# Tilføj ny postering
data.append(ny_postering)

# Gem hele listen tilbage i filen
with open(filnavn, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n💾 Gemte kvitteringer i '{filnavn}'")
