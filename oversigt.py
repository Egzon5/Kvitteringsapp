import json

# Åbn filen med kvitteringer
filnavn = "alle_kvitteringer.json"

try:
    with open(filnavn, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Filen alle_kvitteringer.json blev ikke fundet.")
    exit()

# 1. Vis alle kvitteringer
print("📃 Alle kvitteringer:")
for kvit in data:
    print(f"- {kvit['dato']} | {kvit['belob']} kr")

# 2. Beregn totalforbrug
total = sum(k['belob'] for k in data if k['belob'] is not None)
print(f"\n💸 Totalforbrug: {total:.2f} kr")

# 3. Filtrér på måned (brugeren vælger)
valg = input("\n📆 Indtast måned og år (fx 03-2025): ")

print(f"\n🗓️ Kvitteringer for {valg}:")
for kvit in data:
    if kvit["dato"] != "IKKE FUNDET" and valg in kvit["dato"]:
        print(f"- {kvit['dato']} | {kvit['belob']} kr")
