import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ======================
# Proprietà materiali
# ======================
materiali = {
    "Acciaio inox": {"densita": 8000, "c": 500, "k": 16},
    "Ghisa": {"densita": 7200, "c": 460, "k": 50},
    "Alluminio": {"densita": 2700, "c": 900, "k": 235},
    "Rame": {"densita": 8900, "c": 385, "k": 400},
    "Personalizzato": {"densita": None, "c": None, "k": None}
}

st.title("🔬 Simulatore Avanzato Riscaldamento Piastra")

# ======================
# Input utente
# ======================
materiale = st.selectbox("Materiale della piastra", list(materiali.keys()))

if materiale == "Personalizzato":
    densita = st.number_input("Densità (kg/m³)", value=7800.0)
    c = st.number_input("Calore specifico (J/kg·K)", value=500.0)
    k = st.number_input("Conduttività termica (W/m·K)", value=50.0)
else:
    densita = materiali[materiale]["densita"]
    c = materiali[materiale]["c"]
    k = materiali[materiale]["k"]

diametro = st.slider("Diametro piastra (cm)", 10, 100, 40)
spessore = st.slider("Spessore piastra (cm)", 0.5, 5.0, 1.0)
potenza = st.slider("Potenza fornello (kW)", 0.5, 10.0, 4.0)
tempo = st.slider("Tempo esposizione (minuti)", 1, 60, 20)
efficienza = st.slider("Efficienza trasferimento calore (%)", 10, 80, 45)

# ======================
# Calcoli principali
# ======================
r = diametro / 2 / 100   # m
A = np.pi * r**2         # m²
V = spessore / 100 * A   # m³
m = densita * V          # kg

E_tot = potenza * 1000 * tempo * 60  # J
E_eff = E_tot * (efficienza / 100)

# Temperatura media
deltaT = E_eff / (m * c)
T_finale_media = 25 + deltaT

# Temperatura massima (stimata 1,3x media per effetto diretto fiamma)
T_finale_max = T_finale_media * 1.3

# Gradiente nello spessore (semplificato)
# ΔT_spessore ~ flusso * spessore / k
q = (E_eff / (tempo * 60)) / A  # W/m²
deltaT_spessore = q * (spessore/100) / k
T_superficie_inf = T_finale_max
T_superficie_sup = T_superficie_inf - deltaT_spessore*100  # lato opposto più freddo

# ======================
# Output numerico
# ======================
st.subheader("📊 Risultati")
st.write(f"**Temperatura media stimata:** {T_finale_media:.1f} °C")
st.write(f"**Temperatura massima (zona fiamma):** {T_finale_max:.1f} °C")
st.write(f"**Gradiente termico attraverso lo spessore:** ~{deltaT_spessore:.1f} °C/cm")
st.write(f"**Temperatura lato inferiore:** {T_superficie_inf:.1f} °C")
st.write(f"**Temperatura lato superiore:** {T_superficie_sup:.1f} °C")

# ======================
# Grafici
# ======================
time_array = np.linspace(0, tempo*60, 200)
temp_media = 25 + deltaT * (time_array / (tempo*60))
temp_max = temp_media * 1.3

fig, ax = plt.subplots()
ax.plot(time_array/60, temp_media, label="Temperatura media")
ax.plot(time_array/60, temp_max, '--', label="Temperatura massima zona fiamma")
ax.set_xlabel("Tempo (minuti)")
ax.set_ylabel("Temperatura (°C)")
ax.set_title("Evoluzione temperatura nel tempo")
ax.legend()
st.pyplot(fig)

# Gradiente nello spessore
fig2, ax2 = plt.subplots()
ax2.bar(["Lato fiamma (inferiore)", "Lato opposto (superiore)"],
        [T_superficie_inf, T_superficie_sup],
        color=["red", "blue"])
ax2.set_ylabel("Temperatura (°C)")
ax2.set_title("Gradiente termico attraverso lo spessore")
st.pyplot(fig2)
