import streamlit as st
import pandas as pd
import numpy as np
import os
import tempfile
import re
import sys
from datetime import datetime
from utils.data_cleaner import DataCleaner
from utils.file_handler import FileHandler
from mongo_extractor import crear_dataframes_de_todas_las_colecciones

# Configuración de autenticación usando secrets.toml
LOGIN_CONFIG = {
    "password": st.secrets.get("LOGIN_PASSWORD"),
    "title": st.secrets.get("APP_TITLE", "Data Cleaner Pro"),
    "subtitle": st.secrets.get("APP_SUBTITLE", "Sistema de Procesamiento de Limpieza de Datos")
}

def show_login_screen():
    st.set_page_config(
        page_title="Data Cleaner Pro - Login",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        .stApp {
            background: linear-gradient(145deg, #f5f5f5 0%, #e8e8e8 100%);
            font-family: 'Inter', sans-serif;
        }

        .login-container {
            background: #ffffff;
            padding: 3rem 4rem;
            max-width: 500px;
            margin: 0 auto;
            text-align: center;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
        }

        .login-title {
            color: #2c3e50;
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0 auto 2rem auto;
            letter-spacing: -0.02em;
            text-align: center;
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stTextInput > div > div > input {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.875rem 1rem;
            font-size: 0.95rem;
            font-weight: 400;
            transition: all 0.2s ease;
            width: 100%;
            color: #2d3748;
        }

        .stTextInput > div > div > input:focus {
            outline: none;
            border-color: #4a5568;
            box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1);
            background: #ffffff;
        }

        .stTextInput > div > div > input::placeholder {
            color: #a0aec0;
        }

        .stButton > button {
            background: #4a5568;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.875rem 2rem;
            font-size: 0.95rem;
            font-weight: 500;
            width: 100%;
            transition: all 0.2s ease;
            margin-top: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .stButton > button:hover {
            background: #2d3748;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        .login-footer {
            margin-top: 2rem;
            color: #718096;
            font-size: 0.8rem;
            font-weight: 400;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        header {visibility: hidden;}

        .stTextInput > label {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="login-container">
        <h1 class="login-title">{LOGIN_CONFIG['title']}</h1>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="Ingresa tu contraseña",
            label_visibility="collapsed",
            key="login_password"
        )

        if st.button("Ingresar", type="primary", use_container_width=True):
            if password == LOGIN_CONFIG['password']:
                st.session_state['authenticated'] = True
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

    st.markdown("""
        <div class="login-footer">
            <p>Data Cleaner Pro v2.0</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def check_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        show_login_screen()
        st.stop()

@st.cache_data
def load_mongo_dataframes():
    """Carga los DataFrames de MongoDB con cache"""
    try:
        dataframes = crear_dataframes_de_todas_las_colecciones()
        if dataframes:
            return dataframes
        else:
            return {}
    except Exception as e:
        st.error(f"Error cargando DataFrames de MongoDB: {e}")
        return {}

def detect_brand_from_filename(filename):
    """Detecta la marca desde el nombre del archivo"""
    filename_upper = filename.upper()

    l_pattern = re.search(r'L\d+([A-Z]{2})', filename_upper)
    if l_pattern:
        return l_pattern.group(1)

    for marca in ['CH', 'CL', 'NE', 'SK', 'FB']:
        if marca in filename_upper:
            return marca

    return None

check_authentication()

st.set_page_config(
    page_title="Data Cleaner Pro",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Global con diseño 3D Neutro Profesional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-dark: #2d3748;
        --primary-mid: #4a5568;
        --primary-light: #718096;
        --accent: #5a67d8;
        --bg-light: #f7fafc;
        --bg-card: #ffffff;
        --shadow-dark: rgba(0, 0, 0, 0.08);
        --shadow-light: rgba(255, 255, 255, 0.8);
        --border-subtle: #e2e8f0;
    }

    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e7f1 100%);
    }

    /* Header Principal - Responsive y centrado */
    .main-header {
        background: #ffffff;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        width: 100%;
        box-sizing: border-box;
    }

    .main-header h1 {
        color: var(--primary-dark);
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        text-align: center;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .main-header p {
        color: var(--primary-light);
        font-size: 1rem;
        text-align: center;
        margin: 0.75rem 0 0 0;
        font-weight: 400;
    }

    /* Cards elegantes */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-color: #cbd5e0;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin: 0;
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--primary-light);
        font-weight: 600;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Sidebar 3D */
    .stSidebar {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.6);
    }

    .stSidebar .sidebar-content {
        padding: 1.5rem;
    }

    /* Botones elegantes y planos */
    .stButton > button {
        background: #4a5568;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-transform: none;
        letter-spacing: 0.01em;
        font-size: 0.9rem;
    }

    .stButton > button:hover {
        background: #2d3748;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #ffffff;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }

    /* Upload Area */
    .upload-area {
        background: #f7fafc;
        border: 2px dashed #cbd5e0;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        transition: all 0.2s ease;
    }

    .upload-area:hover {
        border-color: #4a5568;
        background: #edf2f7;
    }

    /* Badges de Estado */
    .status-success, .status-warning, .status-error {
        padding: 0.375rem 0.875rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
        text-transform: none;
        letter-spacing: 0.01em;
        border: 1px solid transparent;
    }

    .status-success {
        background: #f0fff4;
        color: #22543d;
        border-color: #9ae6b4;
    }

    .status-warning {
        background: #fffff0;
        color: #744210;
        border-color: #f6e05e;
    }

    .status-error {
        background: #fff5f5;
        color: #742a2a;
        border-color: #fc8181;
    }

    /* Tablas */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }

    /* Info Boxes */
    .info-box, .info-box-success, .info-box-warning {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid transparent;
    }

    .info-box {
        background: #ebf8ff;
        color: #2c5282;
        border-color: #bee3f8;
    }

    .info-box-success {
        background: #f0fff4;
        color: #22543d;
        border-color: #c6f6d5;
    }

    .info-box-warning {
        background: #fffff0;
        color: #744210;
        border-color: #fefcbf;
    }

    /* Separadores */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #cbd5e0 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Ticker/Stats Bar - Plano y limpio */
    .stat-box {
        background: #ffffff;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #4a5568;
        box-shadow: none;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #f7fafc;
        border-radius: 8px 8px 0 0;
        padding: 0.875rem 1.25rem;
        font-weight: 500;
        color: #718096;
        border: none;
        border-bottom: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #2d3748;
        border-bottom-color: #4a5568;
        font-weight: 600;
    }

    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Brand Card */
    .brand-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        border-left: 3px solid #4a5568;
    }

    /* Footer */
    .footer-3d {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
    }

    /* Spinner y Loading */
    .stSpinner > div {
        border-color: #4a5568 !important;
    }

    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid transparent;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc !important;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        font-weight: 500;
        color: #2d3748;
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: #4a5568;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }

    .stDownloadButton > button:hover {
        background: #2d3748;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Header principal - centrado y con ancho máximo fijo
st.markdown("""
<div style="max-width: 1200px; margin: 0 auto; width: 100%;">
    <div class="main-header">
        <h1>Data Cleaner Pro</h1>
        <p>Procesamiento inteligente de datos con integración MongoDB</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Ticker horizontal estático - Contenedor centrado con ancho máximo
try:
    mongo_dataframes = load_mongo_dataframes()
    if mongo_dataframes:
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")

        # Contenedor principal centrado con ancho máximo
        st.markdown('<div style="max-width: 1200px; margin: 0 auto; width: 100%;">', unsafe_allow_html=True)

        # Usar columns con gap específico para mejor espaciado
        n_collections = len(mongo_dataframes)
        # Crear columnas: LIVE + colecciones + tiempo, todas del mismo tamaño proporcional
        col_weights = [1] + [2] * n_collections + [1]
        cols = st.columns(col_weights, gap="small")

        with cols[0]:
            st.markdown("""
            <div style="background: #ffffff; 
                        border-radius: 6px; 
                        padding: 0.75rem; 
                        text-align: center;
                        border: 1px solid #e2e8f0;
                        border-left: 3px solid #4a5568;
                        height: 100%;
                        min-height: 60px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;">
                <span style="color: #4a5568; font-weight: 700; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase;">LIVE</span>
            </div>
            """, unsafe_allow_html=True)

        for i, (collection_name, df) in enumerate(mongo_dataframes.items()):
            with cols[i + 1]:
                total_records = df.shape[0]
                total_fields = df.shape[1]

                st.markdown(f"""
                <div style="background: #ffffff; 
                            border-radius: 6px; 
                            padding: 0.75rem 0.5rem; 
                            text-align: center;
                            border: 1px solid #e2e8f0;
                            border-left: 3px solid #718096;
                            height: 100%;
                            min-height: 60px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;">
                    <div style="color: #2d3748; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.02em; line-height: 1.2; margin-bottom: 0.25rem;">{collection_name}</div>
                    <div style="color: #718096; font-size: 0.7rem; font-weight: 400; line-height: 1.3;">{total_records:,} registros</div>
                    <div style="color: #a0aec0; font-size: 0.65rem; line-height: 1.2;">{total_fields} campos</div>
                </div>
                """, unsafe_allow_html=True)

        with cols[-1]:
            st.markdown(f"""
            <div style="background: #f7fafc; 
                        border-radius: 6px; 
                        padding: 0.75rem; 
                        text-align: center;
                        border: 1px solid #e2e8f0;
                        height: 100%;
                        min-height: 60px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;">
                <span style="color: #718096; font-size: 0.7rem; font-weight: 500; font-family: monospace;">{current_time}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Conectando a base de datos...")
except:
    st.error("Error de conexión a base de datos")

# Sidebar con diseño mejorado
with st.sidebar:

    action = st.selectbox(
        "Configuración",
        ["Seleccionar acción...", "Actualizar Base de Datos", "Cerrar Sesión"],
        key="action_menu",
        help="Selecciona una acción para ejecutar"
    )

    if action == "Cerrar Sesión":
        st.session_state['authenticated'] = False
        st.rerun()
    elif action == "Actualizar Base de Datos":
        with st.spinner("Actualizando base de datos..."):
            st.cache_data.clear()
            load_mongo_dataframes.clear()
        st.success("Base de datos actualizada")

    st.markdown("---")

    st.markdown("#### Marca")
    brand = st.selectbox(
        "Seleccionar marca:",
        ["CH", "CL", "SK", "NE", "FB", "PB"],
        help="Elige la marca a procesar",
        label_visibility="collapsed"
    )

    brand_info = {
        "CH": {"name": "Cole Haan", "color": "#4a5568"},
        "CL": {"name": "Columbia", "color": "#2d3748"},
        "SK": {"name": "Skechers", "color": "#1a202c"},
        "NE": {"name": "New Era", "color": "#4a5568"},
        "FB": {"name": "Fabletics", "color": "#2d3748"},
        "PB": {"name": "Psycho Bunny", "color": "#1a202c"}
    }

    info = brand_info[brand]
    st.markdown(f"""
    <div class="brand-card" style="border-left-color: {info['color']};">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-weight: 700; color: {info['color']}; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em;">{brand}</span>
            <span style="color: #718096; font-size: 0.9rem; font-weight: 500;">{info['name']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### Descargar Formatos")
    st.markdown("Descarga el formato de ejemplo para cada marca:")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    example_files = {
        "CH": os.path.join(base_dir, "data", "ejemplo_CH.csv"),
        "CL": os.path.join(base_dir, "data", "ejemplo_CL.csv"),
        "SK": os.path.join(base_dir, "data", "ejemplo_SK.csv"),
        "NE": os.path.join(base_dir, "data", "ejemplo_NE.csv"),
        "FB": os.path.join(base_dir, "data", "ejemplo_FB.csv")
    }

    for marca, file_path in example_files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                brand_name = brand_info[marca]["name"]

                st.download_button(
                    label=f"{marca} - {brand_name}",
                    data=file_content,
                    file_name=f"formato_{marca.lower()}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"download_{marca}"
                )
            except Exception as e:
                st.error(f"Error al cargar formato {marca}: {e}")
        else:
            st.warning(f"Formato {marca} no disponible")

    st.markdown("---")

    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #718096; font-size: 0.75rem;">
        <strong style="color: #4a5568; font-size: 0.85rem;">Data Cleaner Pro</strong><br>
        v2.0 • MongoDB Integration
    </div>
    """, unsafe_allow_html=True)

# Área principal con tabs - Contenedor centrado
st.markdown('<div style="max-width: 1200px; margin: 0 auto; width: 100%;">', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Limpieza de Datos", "Plantillas"])

with tab1:
    st.markdown("### Cargar Archivo")

    upload_container = st.container()
    with upload_container:
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo",
            type=['csv', 'xlsx', 'xls'],
            help="Arrastra y suelta o haz clic para seleccionar",
            label_visibility="collapsed"
        )

    if uploaded_file is not None:
        detected_brand = detect_brand_from_filename(uploaded_file.name)

        file_info_container = st.container()
        with file_info_container:
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**{uploaded_file.name}**")
                pattern_type = "Patrón L+número" if re.search(r'L\d+', uploaded_file.name.upper()) else "Patrón directo"
                st.caption(f"Tipo: {pattern_type}")

            with col2:
                if detected_brand and detected_brand != brand:
                    st.markdown(f'<span class="status-warning">Detectado: {detected_brand}</span>', unsafe_allow_html=True)
                    if st.button("Usar detectado", key="use_detected"):
                        st.session_state['auto_brand'] = detected_brand
                        st.rerun()
                else:
                    st.markdown(f'<span class="status-success">Marca: {brand}</span>', unsafe_allow_html=True)

            with col3:
                if 'auto_brand' in st.session_state:
                    brand = st.session_state['auto_brand']

        try:
            file_handler = FileHandler()
            df = file_handler.read_file(uploaded_file)

            metrics_container = st.container()
            with metrics_container:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df):,}</div>
                        <div class="metric-label">Filas</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df.columns)}</div>
                        <div class="metric-label">Columnas</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    file_size = uploaded_file.size / 1024
                    size_text = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{size_text}</div>
                        <div class="metric-label">Tamaño</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    required_columns = ["ItemName", "ItemCode", "Empresa"]
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    status = "Válido" if not missing_columns else "Incompleto"
                    status_class = "status-success" if not missing_columns else "status-error"

                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Estado</div>
                        <span class="{status_class}">{status}</span>
                    </div>
                    """, unsafe_allow_html=True)

            if missing_columns:
                st.error(f"Columnas faltantes: {', '.join(missing_columns)}")

            st.markdown("### Vista Previa")
            with st.expander("Mostrar datos", expanded=True):
                st.dataframe(df.head(10), use_container_width=True, height=300)

            if not missing_columns:
                process_container = st.container()
                with process_container:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button(
                            "Procesar Datos", 
                            type="primary", 
                            use_container_width=True,
                            help="Iniciar proceso de limpieza con datos MongoDB"
                        ):
                            with st.spinner("Procesando datos..."):
                                try:
                                    mongo_dataframes = load_mongo_dataframes()

                                    if not mongo_dataframes:
                                        st.error("Error al conectar con MongoDB")
                                        st.stop()

                                    cleaner = DataCleaner(brand, mongo_dataframes)
                                    cleaned_df = cleaner.clean_data(df)

                                    st.session_state['cleaned_data'] = cleaned_df
                                    st.session_state['original_filename'] = uploaded_file.name
                                    st.session_state['processing_brand'] = brand

                                    st.success("Procesamiento completado")
                                    st.rerun()

                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                                    with st.expander("Ver detalles del error"):
                                        st.exception(e)

        except Exception as e:
            st.error(f"Error al cargar archivo: {str(e)}")

    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #718096;">
            <h3 style="color: #4a5568; font-weight: 600; margin-bottom: 0.5rem;">Selecciona un archivo para comenzar</h3>
            <p style="font-size: 0.9rem;">Soportamos archivos CSV y Excel con detección automática de marca</p>
        </div>
        """, unsafe_allow_html=True)
    # Resultados de limpieza en tab1
    if 'cleaned_data' in st.session_state:
        st.markdown("---")

        results_header = st.container()
        with results_header:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("### Resultados del Procesamiento")
                brand_used = st.session_state.get('processing_brand', 'N/A')
                st.caption(f"Procesado como: **{brand_used}** • {st.session_state.get('original_filename', 'archivo.csv')}")

            with col2:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{brand_used.lower()}_cleaned_{timestamp}.csv"
                csv_data = st.session_state['cleaned_data'].to_csv(index=False, sep=';')

                st.download_button(
                    label="Descargar",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    type="primary",
                    use_container_width=True
                )

        cleaned_df = st.session_state['cleaned_data']

        metrics_container = st.container()
        with metrics_container:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(cleaned_df):,}</div>
                    <div class="metric-label">Total Filas</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(cleaned_df.columns)}</div>
                    <div class="metric-label">Columnas</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                null_rows = cleaned_df.isnull().sum().sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="background: linear-gradient(135deg, #c53030 0%, #9b2c2c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{null_rows:,}</div>
                    <div class="metric-label">Celdas Incompletas</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                complete_rows = cleaned_df.notnull().sum().sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="background: linear-gradient(135deg, #2f855a 0%, #276749 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{complete_rows:,}</div>
                    <div class="metric-label">Celdas Completas</div>
                </div>
                """, unsafe_allow_html=True)

            with col5:
                completeness = (complete_rows - null_rows) / complete_rows * 100 if complete_rows > 0 else 0
                color = "#2f855a" if completeness > 80 else "#d69e2e" if completeness > 60 else "#c53030"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: {color};">{completeness:.1f}%</div>
                    <div class="metric-label">Completitud</div>
                </div>
                """, unsafe_allow_html=True)

        results_tab1, results_tab2 = st.tabs(["Datos Procesados", "Análisis de Calidad"])

        with results_tab1:
            st.markdown("#### Vista de Datos")
            st.dataframe(cleaned_df, use_container_width=True, height=400)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Primeras columnas:**")
                st.write(list(cleaned_df.columns[:5]))
            with col2:
                st.markdown("**Últimas columnas:**")
                st.write(list(cleaned_df.columns[-5:]))

        with results_tab2:
            st.markdown("#### Análisis de Calidad de Datos")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Valores Nulos por Columna**")
                null_counts = cleaned_df.isnull().sum()
                null_df = pd.DataFrame({
                    'Columna': null_counts.index,
                    'Nulos': null_counts.values,
                    'Porcentaje': (null_counts.values / len(cleaned_df) * 100).round(1)
                })
                null_df = null_df[null_df['Nulos'] > 0]

                if len(null_df) > 0:
                    st.dataframe(null_df, use_container_width=True, height=300)
                else:
                    st.success("No hay valores nulos en ninguna columna")

            with col2:
                st.markdown("**Estadísticas de Tipos de Datos**")
                dtypes_count = cleaned_df.dtypes.value_counts()
                dtypes_df = pd.DataFrame({
                    'Tipo': dtypes_count.index.astype(str),
                    'Cantidad': dtypes_count.values
                })
                st.dataframe(dtypes_df, use_container_width=True, height=300)

            st.markdown("#### Resumen de Calidad")
            total_cells = len(cleaned_df) * len(cleaned_df.columns)
            null_cells = cleaned_df.isnull().sum().sum()
            quality_score = ((total_cells - null_cells) / total_cells * 100) if total_cells > 0 else 0

            if quality_score >= 95:
                quality_status = "Excelente"
                quality_color = "#2f855a"
            elif quality_score >= 80:
                quality_status = "Buena"
                quality_color = "#d69e2e"
            else:
                quality_status = "Requiere atención"
                quality_color = "#c53030"

            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%); 
                        border-radius: 16px; 
                        padding: 1.5rem; 
                        margin: 1rem 0;
                        box-shadow: 6px 6px 12px #e0e0e0, -6px -6px 12px #ffffff;
                        border-left: 4px solid {quality_color};">
                <h4 style="color: {quality_color}; margin: 0; font-size: 1.25rem;">Puntuación de Calidad: {quality_score:.1f}%</h4>
                <p style="margin: 0.5rem 0 0 0; color: #718096; font-weight: 500;">Estado: {quality_status}</p>
            </div>
            """, unsafe_allow_html=True)



with tab2:
    st.markdown("### Plantilla")

    upload_container = st.container()
    with upload_container:
        uploaded_file_template = st.file_uploader(
            "Selecciona tu archivo",
            type=['csv', 'xlsx', 'xls'],
            help="Arrastra y suelta o haz clic para seleccionar",
            key="template_uploader",
            label_visibility="collapsed"
        )

    if uploaded_file_template is not None:
        try:
            file_handler = FileHandler()
            df = file_handler.read_file(uploaded_file_template)

            metrics_container = st.container()
            with metrics_container:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df):,}</div>
                        <div class="metric-label">Filas</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df.columns)}</div>
                        <div class="metric-label">Columnas</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    file_size = uploaded_file_template.size / 1024
                    size_text = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{size_text}</div>
                        <div class="metric-label">Tamaño</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("### Vista Previa")
            with st.expander("Mostrar datos", expanded=True):
                st.dataframe(df.head(10), use_container_width=True, height=300)

            st.markdown("---")
            st.markdown("### Crear Nueva Plantilla")

            if 'Empresa' in df.columns and 'ItemCode' in df.columns:
                excluded_columns = ['U_Sellitem', 'Update', 'U_Style','u_sellitem', 'update', 'u_style']
                u_columns = [col for col in df.columns if col.upper().startswith('U') and col not in excluded_columns]

                if u_columns:
                    st.markdown(f"**Columnas encontradas que empiezan con 'U':** {len(u_columns)}")
                    st.write(u_columns)

                    if st.button("Crear Plantilla Excel", type="primary", use_container_width=True):
                        with st.spinner("Transformando datos..."):
                            try:
                                new_rows = []

                                for index, row in df.iterrows():
                                    empresa = row['Empresa']
                                    itemcode = row['ItemCode']

                                    for u_col in u_columns:
                                        valor = row[u_col]

                                        if pd.notna(valor):
                                            new_row = {
                                                'Pais': '',
                                                'DB': empresa,
                                                'COLUMNA': u_col,
                                                'Codigo_SAP': itemcode,
                                                'VALOR': valor
                                            }
                                            new_rows.append(new_row)

                                new_df = pd.DataFrame(new_rows)

                                def format_column_name(col_name):
                                    if '_' not in col_name:
                                        return col_name.upper()
                                    else:
                                        parts = col_name.split('_')
                                        formatted_parts = [parts[0].upper()]
                                        for part in parts[1:]:
                                            formatted_parts.append(part.capitalize())
                                        return '_'.join(formatted_parts)

                                new_df['COLUMNA'] = new_df['COLUMNA'].apply(format_column_name)
                                new_df = new_df.sort_values('COLUMNA', ascending=False)

                                st.session_state['transformed_df'] = new_df
                                st.session_state['original_template_filename'] = uploaded_file_template.name

                                st.success("Plantilla creada exitosamente")
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error al crear plantilla: {str(e)}")
                                st.exception(e)
                else:
                    st.warning("No se encontraron columnas que empiecen con 'U'")
            else:
                missing_cols = []
                if 'Empresa' not in df.columns:
                    missing_cols.append('Empresa')
                if 'ItemCode' not in df.columns:
                    missing_cols.append('ItemCode')
                st.error(f"Columnas faltantes: {', '.join(missing_cols)}")

        except Exception as e:
            st.error(f"Error al cargar archivo: {str(e)}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #718096;">
            <h3 style="color: #4a5568; font-weight: 600; margin-bottom: 0.5rem;">Selecciona un archivo para comenzar</h3>
            <p style="font-size: 0.9rem;">Soportamos archivos CSV y Excel para crear plantillas</p>
        </div>
        """, unsafe_allow_html=True)

    if 'transformed_df' in st.session_state:
        st.markdown("---")

        template_results_header = st.container()
        with template_results_header:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("### Plantilla Transformada")
                original_filename = st.session_state.get('original_template_filename', 'archivo.csv')
                st.caption(f"Generada desde: **{original_filename}**")

            with col2:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"plantilla_transformada_{timestamp}.xlsx"

                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    st.session_state['transformed_df'].to_excel(writer, sheet_name='Plantilla', index=False)

                st.download_button(
                    label="Descargar Excel",
                    data=output.getvalue(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )

        transformed_df = st.session_state['transformed_df']

        metrics_container = st.container()
        with metrics_container:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(transformed_df):,}</div>
                    <div class="metric-label">Total Filas</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                unique_db = transformed_df['DB'].nunique()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_db}</div>
                    <div class="metric-label">Empresas Únicas</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                unique_columns = transformed_df['COLUMNA'].nunique()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_columns}</div>
                    <div class="metric-label">Columnas 'U'</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                unique_items = transformed_df['Codigo_SAP'].nunique()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_items}</div>
                    <div class="metric-label">Códigos SAP</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### Vista Previa de la Plantilla")
        with st.expander("Mostrar plantilla transformada", expanded=True):
            st.dataframe(transformed_df.head(20), use_container_width=True, height=400)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Estructura de la Plantilla:**")
            st.write("• **Pais**: Columna vacía")
            st.write("• **DB**: Contenido de la columna 'Empresa'")
            st.write("• **COLUMNA**: Nombres de columnas que empiezan con 'U'")
            st.write("• **Codigo_SAP**: Código del item")
            st.write("• **VALOR**: Valores de las columnas 'U'")

        with col2:
            st.markdown("**Resumen de Transformación:**")
            st.write(f"• Total de registros: {len(transformed_df):,}")
            st.write(f"• Empresas procesadas: {unique_db}")
            st.write(f"• Columnas 'U' encontradas: {unique_columns}")
            st.write(f"• Códigos SAP únicos: {unique_items}")

st.markdown("<br>", unsafe_allow_html=True)

# Cerrar contenedor principal
st.markdown('</div>', unsafe_allow_html=True)

# Footer moderno
st.markdown('<div style="max-width: 1200px; margin: 0 auto; width: 100%;">', unsafe_allow_html=True)
st.markdown("""
<div class="footer-3d">
    <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; color: #2d3748; letter-spacing: 0.02em;">Data Cleaner Pro</div>
    <div style="font-size: 0.85rem; color: #718096;">Procesamiento inteligente de datos • Integración MongoDB • v2.0</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)