import streamlit as st
import matplotlib.pyplot as plt

# Constants (1 drop = 5 ppm per 1L)
PPM_PER_DROP = {
    "Mg": 8,
    "Ca": 5,
    "KHCO3": 8,
    "NaHCO3": 5
}

drop_effects = {
    "Mg": "Enhances Brightness, Juiciness, Perceived Acidity",
    "Ca": "Enhances Body, Weight, Richness",
    "KHCO3": "Buffers Acidity, Adds Potassium Sweetness",
    "NaHCO3": "Buffers Acidity, Adds Sodium Sweetness"
}

presets = {
    "Bright & Juicy (Washed Africans)": {"GH": 40, "KH": 20, "Mg_pct": 80, "K_pct": 80},
    "Balanced Sweetness (Latin Americans)": {"GH": 50, "KH": 30, "Mg_pct": 50, "K_pct": 50},
    "Body & Roundness (Naturals / Anaerobic)": {"GH": 60, "KH": 40, "Mg_pct": 30, "K_pct": 30},
    "High Floral Clarity (Geishas)": {"GH": 35, "KH": 20, "Mg_pct": 90, "K_pct": 90}
}

def calculate_drops(gh, kh, mg_pct, k_pct, volume_ml):
    scale = volume_ml / 1000  # per liter scaling

    mg_ppm = gh * (mg_pct / 100)
    ca_ppm = gh - mg_ppm

    kh_k_ppm = kh * (k_pct / 100)
    kh_na_ppm = kh - kh_k_ppm

    return {
        "Mg": mg_ppm / PPM_PER_DROP["Mg"] * scale,
        "Ca": ca_ppm / PPM_PER_DROP["Ca"] * scale,
        "KHCO3": kh_k_ppm / PPM_PER_DROP["KHCO3"] * scale,
        "NaHCO3": kh_na_ppm / PPM_PER_DROP["NaHCO3"] * scale,
        "GH_Mg": mg_ppm,
        "GH_Ca": ca_ppm,
        "KH_K": kh_k_ppm,
        "KH_Na": kh_na_ppm
    }

# Streamlit App Config
st.set_page_config(page_title="Champion Water Builder", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    h1, h2 {
        color: #f39c12;
    }
    .stButton>button {
        background-color: #f39c12;
        color: white;
        font-weight: bold;
        font-size: 1.1em;
        border-radius: 10px;
        padding: 0.6em 1.2em;
    }
    .stButton>button:hover {
        background-color: #e67e22 !important;
    }
    .stNumberInput>div>div>input {
        font-size: 1.1em;
        padding: 6px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.title("🏆 Champion Coffee Water Builder")
st.caption("Craft your brew water like a world barista champion.")

# Sidebar Setup
st.sidebar.title("💧 Water Design Mode")
mode = st.sidebar.radio("Choose Water Mode", ["Use a Champion Preset", "Custom Build"])

if mode == "Use a Champion Preset":
    preset_name = st.sidebar.selectbox("Choose a Profile", list(presets.keys()))
    p = presets[preset_name]
    gh = p["GH"]
    kh = p["KH"]
    mg_pct = p["Mg_pct"]
    k_pct = p["K_pct"]
    st.sidebar.markdown(f"**GH**: {gh} ppm  \n**KH**: {kh} ppm")
else:
    gh = st.sidebar.number_input("🔷 General Hardness (GH, ppm)", min_value=0, max_value=200, value=50, step=1)
    mg_pct = st.sidebar.number_input("🧪 Magnesium % of GH", min_value=0, max_value=100, value=70, step=1)
    kh = st.sidebar.number_input("🔶 Carbonate Hardness (KH, ppm)", min_value=0, max_value=200, value=30, step=1)
    k_pct = st.sidebar.number_input("🥝 Potassium % of KH (KHCO₃)", min_value=0, max_value=100, value=60, step=1)

volume_ml = st.sidebar.number_input("📦 Total Water Volume (mL)", min_value=100, max_value=5000, value=300, step=100)

# Button to Calculate
if st.sidebar.button("💥 Generate Recipe"):
    result = calculate_drops(gh, kh, mg_pct, k_pct, volume_ml)
    st.balloons()

    st.subheader("☕ Water Recipe")
    st.markdown(f"For **{volume_ml} mL** of distilled water:")

    st.write(f"- **{result['Mg']:.2f} drops Mg** ({round(result['Mg'])} drops) — {drop_effects['Mg']}")
    st.write(f"- **{result['Ca']:.2f} drops Ca** ({round(result['Ca'])} drops) — {drop_effects['Ca']}")
    st.write(f"- **{result['KHCO3']:.2f} drops KHCO₃ (K)** ({round(result['KHCO3'])} drops) — {drop_effects['KHCO3']}")
    st.write(f"- **{result['NaHCO3']:.2f} drops NaHCO₃** ({round(result['NaHCO3'])} drops) — {drop_effects['NaHCO3']}")

    st.markdown("#### 📋 Profile Summary")
    st.info(
        f"**GH:** {gh} ppm  \n"
        f"• Mg: {result['GH_Mg']:.1f} ppm  \n"
        f"• Ca: {result['GH_Ca']:.1f} ppm  \n\n"
        f"**KH:** {kh} ppm  \n"
        f"• From KHCO₃ (K): {result['KH_K']:.1f} ppm  \n"
        f"• From NaHCO₃: {result['KH_Na']:.1f} ppm"
    )

    st.markdown("---")
    st.subheader("📈 Water Map")
    fig, ax = plt.subplots()
    ax.scatter(kh, gh, s=300, color="#f39c12", edgecolors="black")
    ax.set_xlabel("KH (ppm)")
    ax.set_ylabel("GH (ppm)")
    ax.set_title("GH vs KH Profile")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

else:
    st.warning("Adjust your settings and click **Generate Recipe**.")
