import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Constants (1 drop = 5 ppm per 1L)
PPM_PER_DROP = {
    "Mg": 8,
    "Ca": 5,
    "KHCO3": 8,
    "NaHCO3": 5
}

drop_effects = {
    "Mg": "Enhances brightness, juiciness, perceived acidity",
    "Ca": "Enhances body, weight, richness",
    "KHCO3": "Buffers acidity, adds potassium sweetness",
    "NaHCO3": "Buffers acidity, adds sodium sweetness"
}

presets = {
    "Bright & Juicy": {"GH": 40, "KH": 20, "Mg_pct": 80, "K_pct": 80, "desc": "Perfect for washed African coffees", "icon": "☀️"},
    "Balanced Sweetness": {"GH": 50, "KH": 30, "Mg_pct": 50, "K_pct": 50, "desc": "Ideal for Latin American origins", "icon": "⚖️"},
    "Body & Roundness": {"GH": 60, "KH": 40, "Mg_pct": 30, "K_pct": 30, "desc": "Great for naturals & anaerobic", "icon": "🔵"},
    "High Floral Clarity": {"GH": 35, "KH": 20, "Mg_pct": 90, "K_pct": 90, "desc": "Exceptional for Geisha varieties", "icon": "🌸"}
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
st.set_page_config(
    page_title="Champion Water Builder", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Coffee-Themed Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b16 50%, #1a1a1a 100%);
        color: #f5f5f5;
    }
    
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(139, 69, 19, 0.3);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Card Styling */
    .card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        border: 1px solid #444;
    }
    
    .preset-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        border: 2px solid #444;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .preset-card:hover {
        border-color: #D2691E;
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(210, 105, 30, 0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        border: none;
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 69, 19, 0.4);
        background: linear-gradient(135deg, #A0522D 0%, #FF8C00 100%);
    }
    
    /* Input Styling */
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, #333 0%, #2a2a2a 100%);
        border: 2px solid #444;
        border-radius: 10px;
        color: #f5f5f5;
        font-size: 1rem;
        padding: 0.6rem;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #D2691E;
        box-shadow: 0 0 0 2px rgba(210, 105, 30, 0.2);
    }
    
    /* Slider Styling */
    .stSlider > div > div > div > div {
        background-color: #D2691E;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #8B4513;
    }
    
    /* Recipe Card */
    .recipe-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
        border: 1px solid #D2691E;
    }
    
    .drop-item {
        background: linear-gradient(135deg, #333 0%, #2a2a2a 100%);
        border-radius: 10px;
        padding: 0.875rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #D2691E;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .drop-count {
        font-size: 1.1rem;
        font-weight: 700;
        color: #D2691E;
    }
    
    .drop-effect {
        font-size: 0.85rem;
        color: #ccc;
        margin-top: 0.25rem;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }
        
        .card {
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        
        .recipe-card {
            padding: 1.25rem;
        }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    }
    
    /* Text color overrides */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label {
        color: #f5f5f5 !important;
    }
    
    /* Remove white backgrounds from containers */
    .stApp > div:first-child {
        background: transparent;
    }
    
    div[data-testid="stVerticalBlock"] > div:first-child {
        background: transparent;
    }
    
    /* Metric styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #333 0%, #2a2a2a 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #444;
    }
    
    div[data-testid="metric-container"] > div {
        color: #f5f5f5;
    }
    
    /* Info/Success/Warning boxes */
    .stInfo, .stSuccess, .stWarning {
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 12px;
        border: 1px solid #D2691E;
        color: #f5f5f5;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: linear-gradient(135deg, #333 0%, #2a2a2a 100%);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #333 0%, #2a2a2a 100%);
        border-radius: 10px;
        border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏆 Champion Water Builder</h1>
        <p class="header-subtitle">Craft barista-quality water profiles for exceptional coffee extraction</p>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'selected_preset' not in st.session_state:
    st.session_state.selected_preset = None
if 'recipe_generated' not in st.session_state:
    st.session_state.recipe_generated = False

# Main Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💧 Water Profile Designer")
    
    mode = st.radio(
        "Choose your approach:",
        ["Champion Presets", "Custom Profile"],
        key="mode_selector"
    )
    
    if mode == "Champion Presets":
        st.markdown("#### Select a Profile")
        
        for preset_name, preset_data in presets.items():
            if st.button(
                f"{preset_data['icon']} {preset_name}",
                key=f"preset_{preset_name}",
                help=preset_data['desc']
            ):
                st.session_state.selected_preset = preset_name
                st.rerun()
        
        if st.session_state.selected_preset:
            p = presets[st.session_state.selected_preset]
            gh = p["GH"]
            kh = p["KH"]
            mg_pct = p["Mg_pct"]
            k_pct = p["K_pct"]
            
            st.success(f"✅ **{st.session_state.selected_preset}** selected")
            st.info(f"**GH**: {gh} ppm | **KH**: {kh} ppm")
        else:
            gh = kh = mg_pct = k_pct = 0
    
    else:
        st.markdown("#### Custom Parameters")
        gh = st.number_input("🔷 General Hardness (GH, ppm)", min_value=0, max_value=200, value=50, step=5)
        mg_pct = st.number_input("🧪 Magnesium % of GH", min_value=0, max_value=100, value=70, step=5)
        kh = st.number_input("🔶 Carbonate Hardness (KH, ppm)", min_value=0, max_value=200, value=30, step=5)
        k_pct = st.number_input("🥝 Potassium % of KH", min_value=0, max_value=100, value=60, step=5)
    
    st.markdown("#### Brew Volume")
    volume_ml = st.number_input("📦 Water Volume (mL)", min_value=100, max_value=2000, value=300, step=50)
    
    # Generate Recipe Button
    if st.button("🚀 Generate Water Recipe", type="primary"):
        if (mode == "Champion Presets" and st.session_state.selected_preset) or mode == "Custom Profile":
            st.session_state.recipe_generated = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.recipe_generated and ((mode == "Champion Presets" and st.session_state.selected_preset) or mode == "Custom Profile"):
        result = calculate_drops(gh, kh, mg_pct, k_pct, volume_ml)
        
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        st.markdown("### ☕ Your Water Recipe")
        st.markdown(f"**For {volume_ml} mL of distilled water:**")
        
        # Recipe drops with better formatting
        drops_data = [
            ("Mg", result['Mg'], "🧪", "#D2691E"),
            ("Ca", result['Ca'], "🔘", "#8B4513"),
            ("KHCO3", result['KHCO3'], "🥝", "#CD853F"),
            ("NaHCO3", result['NaHCO3'], "🧂", "#DEB887")
        ]
        
        for mineral, drops, icon, color in drops_data:
            st.markdown(f"""
                <div class="drop-item" style="border-left-color: {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1rem; font-weight: 600; color: #f5f5f5;">{icon} {mineral}</span>
                            <div class="drop-effect">{drop_effects[mineral]}</div>
                        </div>
                        <div class="drop-count">{drops:.1f} drops</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Profile Summary
        st.markdown("#### 📊 Profile Analysis")
        
        col_gh, col_kh = st.columns(2)
        with col_gh:
            st.metric("General Hardness", f"{gh} ppm")
            st.caption(f"Mg: {result['GH_Mg']:.1f} ppm | Ca: {result['GH_Ca']:.1f} ppm")
        
        with col_kh:
            st.metric("Carbonate Hardness", f"{kh} ppm")
            st.caption(f"K: {result['KH_K']:.1f} ppm | Na: {result['KH_Na']:.1f} ppm")
        
        # Water Profile Chart
        st.markdown("#### 📈 Water Profile Visualization")
        
        # Set matplotlib style for dark theme
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        fig.patch.set_facecolor('#1f1f1f')
        
        # GH vs KH scatter plot
        ax1.scatter(kh, gh, s=300, color="#D2691E", alpha=0.8, edgecolors="#8B4513", linewidth=2)
        ax1.set_xlabel("KH (ppm)", fontsize=11, fontweight='600', color='#f5f5f5')
        ax1.set_ylabel("GH (ppm)", fontsize=11, fontweight='600', color='#f5f5f5')
        ax1.set_title("Water Hardness Profile", fontsize=12, fontweight='700', color='#f5f5f5')
        ax1.grid(True, linestyle="--", alpha=0.3, color='#666')
        ax1.set_facecolor('#2a2a2a')
        ax1.tick_params(colors='#f5f5f5')
        
        # Mineral composition pie chart
        minerals = ['Mg', 'Ca', 'K', 'Na']
        values = [result['GH_Mg'], result['GH_Ca'], result['KH_K'], result['KH_Na']]
        colors = ['#D2691E', '#8B4513', '#CD853F', '#DEB887']
        
        wedges, texts, autotexts = ax2.pie(values, labels=minerals, colors=colors, autopct='%1.1f%%', 
                                          startangle=90, pctdistance=0.85, textprops={'color': '#f5f5f5'})
        ax2.set_title("Mineral Composition", fontsize=12, fontweight='700', color='#f5f5f5')
        ax2.set_facecolor('#2a2a2a')
        
        for autotext in autotexts:
            autotext.set_color('#1f1f1f')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        st.pyplot(fig, transparent=False)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pro Tips
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        • **Add drops slowly** and stir gently between additions
        • **Test with TDS meter** to verify mineral content  
        • **Start conservative** - you can always add more
        • **Document results** to build your recipe library
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown('<div class="card" style="text-align: center; padding: 2rem 1.5rem;">', unsafe_allow_html=True)
        st.markdown("### 🎯 Ready to Build?")
        st.markdown("Select a champion preset or create a custom profile, then generate your precision water recipe.")
        
        # Quick preview of presets
        st.markdown("#### 🏆 Champion Profiles")
        for name, data in presets.items():
            st.markdown(f"**{data['icon']} {name}**: {data['desc']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
