import streamlit as st
import pandas as pd
import os
import io
from utils import criar_audios, gerar_links_audios, criar_baralho_anki, limpar_arquivos_temporarios

# Page configuration
st.set_page_config(
    page_title="Anki Deck Generator - English Study Tracker",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS matching English Study Tracker
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    }
    
    /* Purple gradient background like tracker */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px;
    }
    
    /* Header navbar estilo do tracker */
    .navbar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    
    .navbar-brand {
        display: flex;
        align-items: center;
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .navbar-menu {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .navbar-item {
        background: rgba(255,255,255,0.15);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .navbar-item:hover {
        background: rgba(255,255,255,0.25);
    }
    
    .navbar-item.active {
        background: white;
        color: #667eea;
    }
    
    /* White cards tracker style */
    .tracker-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .tracker-card h2 {
        color: #5a67d8;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
    }
    
    .tracker-card h2::before {
        content: '';
        display: inline-block;
        width: 4px;
        height: 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin-right: 0.75rem;
        border-radius: 2px;
    }
    
    /* Tracker style metrics (3 cards with icons) */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #718096;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Tracker style buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        width: 100%;
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader estilo clean */
    .stFileUploader {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        border: 2px dashed #e2e8f0;
    }
    
    /* Dataframe estilo tracker */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Success/Info boxes */
    .success-box {
        background: #c6f6d5;
        color: #22543d;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #38a169;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .info-box {
        background: #bee3f8;
        color: #2c5282;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3182ce;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Audio preview boxes */
    .audio-preview {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    /* Step indicator */
    .step-indicator {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: #edf2f7;
        border-radius: 8px;
    }
    
    .step-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 1rem;
        font-size: 1rem;
    }
    
    .step-text {
        color: #4a5568;
        font-weight: 600;
    }
    
    /* REMOVE sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Settings inline card */
    .settings-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e9ecff;
        margin: 1rem 0;
    }
    
    .settings-row {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Navbar com menu no topo
st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">
            🎴 Anki Deck Generator
        </div>
        <div class="navbar-menu">
            <span style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-right: 1rem;">English Study Tracker</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'audio_dir' not in st.session_state:
    st.session_state.audio_dir = None
if 'audios_gerados' not in st.session_state:
    st.session_state.audios_gerados = False
if 'excel_path' not in st.session_state:
    st.session_state.excel_path = None
if 'last_upload_id' not in st.session_state:
    st.session_state.last_upload_id = None

# Inline settings (replaces sidebar)
st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
st.markdown("<h2>⚙️ Deck Settings</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    deck_name = st.text_input("📦 Deck Name", "English Words", key="deck_name_input")

with col2:
    audio_speed = st.slider("⚡ Audio Speed", 0.5, 2.0, 1.0, 0.1, key="audio_speed_slider", help="1.0 = normal speed")

st.info("🎤 Using Google Text-to-Speech (English voice)")

deck_id = 2059400110
model_id = 1607392319

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# STEP 1: File Upload
# ============================================================================
st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
st.markdown("<h2>📁 Upload Excel File</h2>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag your Excel file here or click to select",
    type=['xlsx', 'xls'],
    help="Format: Word | Translation | Phonetic | Context",
    key="file_uploader"
)

# If no file is uploaded, clear everything
if not uploaded_file:
    if st.session_state.df is not None:
        st.session_state.df = None
        st.session_state.audio_dir = None
        st.session_state.audios_gerados = False
        st.session_state.excel_path = None
        st.session_state.last_upload_id = None
        st.rerun()

if uploaded_file:
    # Check if it's a new file OR if state needs reset
    current_upload_id = f"{uploaded_file.name}_{uploaded_file.size}"
    
    if current_upload_id != st.session_state.last_upload_id:
        # Reset all state for new file
        st.session_state.audios_gerados = False
        st.session_state.audio_dir = None
        
        # Read Excel directly from uploaded file buffer
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"⚠️ Error reading Excel file: {str(e)}")
            st.stop()
        
        # Automatically identify columns
        if len(df.columns) >= 4:
            df_renamed = df.iloc[:, [0, 1, 2, 3]].copy()
            df_renamed.columns = ['Word', 'Translation', 'Phonetic', 'Context']
        elif len(df.columns) == 3:
            df_renamed = df.iloc[:, [0, 1, 2]].copy()
            df_renamed.columns = ['Word', 'Translation', 'Context']
        else:
            df_renamed = df.iloc[:, [0, 1]].copy()
            df_renamed.columns = ['Word', 'Context']
        
        st.session_state.df = df_renamed
        st.session_state.excel_path = uploaded_file.name  # Store just the name
        st.session_state.last_upload_id = current_upload_id
        st.rerun()  # Force UI refresh to clear audio preview
    
    # Always show data when file is loaded (even if it's the same file)
    if st.session_state.df is not None:
        
        # Show metrics in tracker style
        st.markdown("""
            <div class="metrics-row">
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Total Words</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">📝</div>
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Columns Detected</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">✅</div>
                    <div class="metric-value">Ready</div>
                    <div class="metric-label">Status</div>
                </div>
            </div>
        """.format(len(st.session_state.df), len(st.session_state.df.columns)), unsafe_allow_html=True)
        
        # Data preview - show all rows
        st.markdown("#### 👀 Data Preview")
        st.dataframe(st.session_state.df, use_container_width=True, height=400)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# STEP 2: Generate Audio Automatically
# ============================================================================
if st.session_state.df is not None and not st.session_state.audios_gerados:
    st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
    st.markdown("<h2>🎵 Generate Audio</h2>", unsafe_allow_html=True)
    
    st.info("💡 Click the button below to generate audio files automatically.")
    
    if st.button("🚀 Generate Audio & Process", type="primary", use_container_width=True):
        with st.spinner("🎤 Creating audio files... This may take a few minutes..."):
            # Create audio files
            audio_folder_name = f"Audios_{deck_name.replace(' ', '_')}"
            audio_dir = criar_audios(
                st.session_state.df,
                audio_folder_name,
                speed=audio_speed
            )
            
            # Generate links
            df_com_audios = gerar_links_audios(
                st.session_state.df,
                audio_dir,
                st.session_state.excel_path,
                deck_name
            )
            
            st.session_state.df = df_com_audios
            st.session_state.audio_dir = audio_dir
            st.session_state.audios_gerados = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# STEP 3: Audio Preview
# ============================================================================
if st.session_state.audios_gerados and st.session_state.audio_dir:
    st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
    st.markdown("<h2>🎧 Audio Preview</h2>", unsafe_allow_html=True)
    
    st.success(f"✅ {len(st.session_state.df)} audio files created successfully!")
    
    # Show 3 examples
    st.markdown("#### 🔊 Audio Samples")
    for i in range(min(3, len(st.session_state.df))):
        with st.expander(f"🎵 {i+1}. {st.session_state.df.iloc[i]['Word']}"):
            col1, col2 = st.columns(2)
            
            audio_path_word = os.path.join(st.session_state.audio_dir, f"word_{i+1}.mp3")
            audio_path_context = os.path.join(st.session_state.audio_dir, f"context_{i+1}.mp3")
            
            with col1:
                st.markdown("**📝 Word**")
                if os.path.exists(audio_path_word):
                    st.audio(audio_path_word)
            
            with col2:
                st.markdown("**💬 Context**")
                if os.path.exists(audio_path_context):
                    st.audio(audio_path_context)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # STEP 4: Download Options
    # ============================================================================
    st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
    st.markdown("<h2>📥 Download Options</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Excel with Audio Links")
        st.info("Download the Excel file with audio file references added.")
        
        # Create Excel file in memory
        excel_buffer = io.BytesIO()
        st.session_state.df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download Excel",
            data=excel_buffer,
            file_name=f"{deck_name}_with_audio.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        st.markdown("#### 🎴 Anki Deck (.apkg)")
        st.info("Generate and download the complete Anki deck with all audio files.")
        
        if st.button("📦 Generate .apkg", type="primary", use_container_width=True):
            with st.spinner("📦 Creating deck..."):
                apkg_path, cartas_novas, total_cartas = criar_baralho_anki(
                    st.session_state.df,
                    st.session_state.audio_dir,
                    deck_name,
                    deck_id,
                    model_id
                )
                
                limpar_arquivos_temporarios()
                
                st.success(f"✅ Deck created with {total_cartas} cards!")
                
                # Download button
                with open(apkg_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download .apkg Deck",
                        data=f,
                        file_name=f"{deck_name}.apkg",
                        mime="application/octet-stream",
                        use_container_width=True,
                        key="download_apkg"
                    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>💡 <b>Tip:</b> Keep your Excel files organized with 4 columns: Word, Translation, Phonetic, Context</p>
    </div>
""", unsafe_allow_html=True)
