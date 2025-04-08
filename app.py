import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Coffee Water Builder", layout="centered")

# --- Style for Mobile ---
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; color: #333; font-family: 'Segoe UI', sans-serif; }
        .block-container { padding: 1rem; }
        h1, h2, h3 { color: #5a2a83; }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Coffee Water Builder – Mobile Optimized")

# --- Concentrate Strengths ---
drop_strengths = {
    "MgSO₄": 8,     # mg/drop
    "CaCl₂": 8,
    "NaHCO₃": 8,
    "KHCO₃": 8,
}

NAHCO3_NA_PER_MG = 0.274
KHCO3_K_PER_MG = 0.393

mineral_notes = {
    "MgSO₄": "Adds brightness, clarity, and fruity acidity.",
    "CaCl₂": "Adds body, balance, and smooth mouthfeel.",
    "NaHCO₃": "Buffers acidity + adds sodium for sweetness/body.",
    "KHCO₃": "Buffers acidity + adds potassium (clean, juicy finish).",
}

recipes = {
    "Rao/Perger (Prodigal)": {"GH": 90, "KH": 42},
    "Simple & Sweet": {"GH": 90, "KH": 40},
    "Light & Bright": {"GH": 60, "KH": 25},
    "Holy Water": {"GH": 62, "KH": 23},
    "La Cabra": {"GH": 60, "KH": 40},
    "Mr. Vo": {"GH": 20, "KH": 15},
    "Wendelboe": {"GH": 38, "KH": 28},
    "Black & White": {"GH": 118, "KH": 32},
    "Coffee Collective": {"GH": 14, "KH": 9},
}

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Customize Your Water")
recipe_names = list(recipes.keys()) + ["Custom"]
selected_recipe = st.sidebar.selectbox("Select a recipe:", recipe_names)
water_volume = st.sidebar.slider("Water Volume (mL)", 250, 1000, 300, step=50)

if selected_recipe == "Custom":
    gh = st.sidebar.number_input("Target GH", 0, 200, 40)
    kh = st.sidebar.number_input("Target KH", 0, 100, 20)
else:
    gh = recipes[selected_recipe]["GH"]
    kh = recipes[selected_recipe]["KH"]

kh_na_ratio = st.sidebar.slider("KH split: NaHCO₃ vs KHCO₃", 0, 100, 50, step=5)

# --- Calculations ---
mg_target = gh * 0.75
ca_target = gh * 0.25
scale = water_volume / 250
mg_mg = mg_target * scale
ca_mg = ca_target * scale
kh_mg = kh * scale

def balanced_rounding(mg_a, mg_b, name_a, name_b):
    per_drop_a = drop_strengths[name_a]
    per_drop_b = drop_strengths[name_b]
    raw_a = mg_a / per_drop_a
    raw_b = mg_b / per_drop_b
    if raw_a >= raw_b:
        rounded_a = math.ceil(raw_a)
        rounded_b = math.floor(raw_b)
    else:
        rounded_a = math.floor(raw_a)
        rounded_b = math.ceil(raw_b)
    return {
        name_a: {"drops": rounded_a, "raw": raw_a, "target_mg": mg_a},
        name_b: {"drops": rounded_b, "raw": raw_b, "target_mg": mg_b},
    }

drops = balanced_rounding(mg_mg, ca_mg, "MgSO₄", "CaCl₂")

kh_na_part = kh_mg * (kh_na_ratio / 100)
kh_k_part = kh_mg - kh_na_part

# NaHCO₃
nahco3_raw = kh_na_part / drop_strengths["NaHCO₃"]
na_contribution = kh_na_part * NAHCO3_NA_PER_MG
drops["NaHCO₃"] = {
    "drops": round(nahco3_raw),
    "raw": nahco3_raw,
    "target_mg": kh_na_part
}

# KHCO₃
khco3_raw = kh_k_part / drop_strengths["KHCO₃"]
k_contribution = kh_k_part * KHCO3_K_PER_MG
drops["KHCO₃"] = {
    "drops": round(khco3_raw),
    "raw": khco3_raw,
    "target_mg": kh_k_part
}

# --- Output Table ---
st.subheader(f"💧 Add these drops to {water_volume} mL of water:")
df = pd.DataFrame([{ 
    "Mineral": k,
    "Drops": v["drops"],
    "Target (mg)": round(v["target_mg"], 1),
    "Strength (mg/drop)": drop_strengths[k],
    "Raw": round(v["raw"], 2),
    "Function": mineral_notes[k]
} for k, v in drops.items()])
st.dataframe(df, use_container_width=True, height=310)

# --- Sodium/Potassium Info ---
st.markdown(f"🧂 **Sodium from NaHCO₃**: `{round(na_contribution, 2)} mg`")
st.markdown(f"🍌 **Potassium from KHCO₃**: `{round(k_contribution, 2)} mg`")

# --- GH vs KH Chart ---
st.subheader("📊 GH vs KH Composition")
fig, ax = plt.subplots(figsize=(5, 3))
ax.scatter([kh], [gh], s=100, color="#5a2a83")
ax.set_xlim(0, 100)
ax.set_ylim(0, 160)
ax.set_xlabel("KH (Alkalinity, ppm)")
ax.set_ylabel("GH (Hardness, ppm)")
ax.grid(True)
st.pyplot(fig, use_container_width=True)

# --- Mineral Info ---
st.subheader("🧠 Mineral Functions")
for m, note in mineral_notes.items():
    st.markdown(f"**{m}**: {note}")
