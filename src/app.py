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

# Agregar el directorio padre al path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Importar configuración de autenticación
    from config.database_config import LOGIN_CONFIG
except ImportError:
    # Fallback si no se puede importar
    LOGIN_CONFIG = {
        "password": os.getenv("LOGIN_PASSWORD"),
        "title": "Data Cleaner Pro", 
        "subtitle": "Sistema de Procesamiento de Limpieza de Datos"
    }

def show_login_screen():
    st.set_page_config(
        page_title="Data Cleaner Pro - Login",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        
        .login-container {
            background: #ffffff;
            padding: 3rem 4rem;
            max-width: 500px;
            margin: 0 auto;
            text-align: center;
        }
        
        
        .login-title {
            color: #1a1a1a;
            font-size: 3.5rem;
            font-weight: 700;
            margin: 0 auto 2.5rem auto;
            letter-spacing: -0.02em;
            text-align: center;
            width: 100%;
            white-space: nowrap;
            display: block;
        }
        
        
        .stTextInput > div > div > input {
            background: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 2px;
            padding: 0.75rem 1rem;
            font-size: 0.875rem;
            font-weight: 400;
            transition: border-color 0.2s ease;
            width: 100%;
            color: #333333;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #555555;
            outline: 0;
            box-shadow: 0 0 0 1px #555555;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #999999;
        }
        
        .stButton > button {
            background: #333333;
            color: white;
            border: none;
            border-radius: 2px;
            padding: 0.75rem 1.5rem;
            font-size: 0.875rem;
            font-weight: 500;
            width: 100%;
            transition: background-color 0.2s ease;
            margin-top: 0.75rem;
        }
        
        .stButton > button:hover {
            background: #222222;
        }
        
        .login-footer {
            margin-top: 1.5rem;
            color: #999999;
            font-size: 0.75rem;
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
    
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="login-container">
        <h1 class="login-title">🤖 {LOGIN_CONFIG['title']}</h1>
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
                st.success("✅ ¡Acceso concedido!")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
    
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
    
    # Buscar patrones L+número+marca (ej: L1CH, L2SK, L3NE, L4CL)
    l_pattern = re.search(r'L\d+([A-Z]{2})', filename_upper)
    if l_pattern:
        return l_pattern.group(1)
    
    # Buscar patrones directos (ej: ejemplo_CH.csv)
    for marca in ['CH', 'CL', 'NE', 'SK']:
        if marca in filename_upper:
            return marca
    
    return None

# Verificar autenticación antes de mostrar la aplicación principal
check_authentication()

# Configuración de la página
st.set_page_config(
    page_title="Data Cleaner Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para diseño profesional
st.markdown("""
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #64748b;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    /* Tipografía */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg-secondary);
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    .main-header h1 {
        color: white;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Cards */
    .metric-card {
        background: var(--bg-primary);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: var(--bg-primary);
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar-content {
        padding: 1rem;
    }
    
    /* Botones */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed var(--border-color);
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background: var(--bg-primary);
        transition: all 0.2s ease;
    }
    
    .upload-area:hover {
        border-color: var(--primary-color);
        background: #fafbff;
    }
    
    /* Status badges */
    .status-success {
        background: #d1fae5;
        color: var(--success-color);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .status-warning {
        background: #fef3c7;
        color: var(--warning-color);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .status-error {
        background: #fee2e2;
        color: var(--error-color);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Tablas */
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* Separadores */
    hr {
        border: none;
        height: 1px;
        background: var(--border-color);
        margin: 2rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box-success {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box-warning {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Ocular elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Header principal con diseño moderno
st.markdown("""
<div class="main-header">
    <h1>⚡ Data Cleaner Pro</h1>
    <p>Procesamiento inteligente de datos con integración MongoDB</p>
</div>
""", unsafe_allow_html=True)

# Ticker horizontal estático
try:
    mongo_dataframes = load_mongo_dataframes()
    if mongo_dataframes:
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Crear columnas para mostrar datos horizontalmente
        cols = st.columns([1] + [2] * len(mongo_dataframes) + [1])
        
        with cols[0]:
            st.markdown("""
            <div style="background: #f8f9fa; border: 1px solid #e9ecef; padding: 0.5rem; border-radius: 6px; text-align: center;">
                <span style="color: #6c757d; font-weight: 600; font-size: 0.8rem;">🔴 LIVE</span>
            </div>
            """, unsafe_allow_html=True)
        
        for i, (collection_name, df) in enumerate(mongo_dataframes.items()):
            with cols[i + 1]:
                total_records = df.shape[0]
                total_fields = df.shape[1]
                
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #dee2e6; padding: 0.5rem; border-radius: 6px; text-align: center; border-left: 3px solid #6c757d;">
                    <div style="color: #212529; font-weight: 600; font-size: 0.8rem;">{collection_name}</div>
                    <div style="color: #6c757d; font-size: 0.7rem;">{total_records:,} records</div>
                    <div style="color: #6c757d; font-size: 0.7rem;">{total_fields} fields</div>
                </div>
                """, unsafe_allow_html=True)
        
        with cols[-1]:
            st.markdown(f"""
            <div style="background: #f8f9fa; border: 1px solid #e9ecef; padding: 0.5rem; border-radius: 6px; text-align: center;">
                <span style="color: #6c757d; font-size: 0.7rem;">{current_time}</span>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("📡 Connecting to database...")
except:
    st.error("❌ Database connection error")

# Sidebar con diseño mejorado
with st.sidebar:
    
    # Menú de acciones
    action = st.selectbox(
        "⚙️ Configuración",
        ["Seleccionar acción...", "🔄 Actualizar Base de Datos", "🚪 Cerrar Sesión"],
        key="action_menu",
        help="Selecciona una acción para ejecutar"
    )
    
    # Ejecutar acción seleccionada
    if action == "🚪 Cerrar Sesión":
        st.session_state['authenticated'] = False
        st.rerun()
    elif action == "🔄 Actualizar Base de Datos":
        with st.spinner("Actualizando base de datos..."):
            st.cache_data.clear()
            load_mongo_dataframes.clear()
        st.success("✅ Base de datos actualizada")
    
    st.markdown("---")
    
    
    # Selector de marca con diseño mejorado
    st.markdown("#### 🏷️ Marca")
    brand = st.selectbox(
        "Seleccionar marca:",
        ["CH", "CL", "SK", "NE"],
        help="Elige la marca a procesar",
        label_visibility="collapsed"
    )
    
    # Información compacta de la marca
    brand_info = {
        "CH": {"name": "Cole Haan", "icon": "👞", "color": "#8B4513"},
        "CL": {"name": "Columbia", "icon": "🧥", "color": "#1E40AF"},
        "SK": {"name": "Skechers", "icon": "👟", "color": "#DC2626"},
        "NE": {"name": "New Era", "icon": "🧢", "color": "#059669"}
    }
    
    info = brand_info[brand]
    st.markdown(f"""
    <div style="background: {info['color']}15; border: 1px solid {info['color']}30; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">{info['icon']}</span>
            <span style="font-weight: 600; color: {info['color']};">{info['name']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Descargar formatos por marca
    st.markdown("#### 📥 Descargar Formatos")
    st.markdown("Descarga el formato de ejemplo para cada marca:")
    
    # Definir rutas de archivos de ejemplo
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Directorio raíz del proyecto
    example_files = {
        "CH": os.path.join(base_dir, "data", "ejemplo_CH.csv"),
        "CL": os.path.join(base_dir, "data", "ejemplo_CL.csv"),
        "SK": os.path.join(base_dir, "data", "ejemplo_SK.csv"),
        "NE": os.path.join(base_dir, "data", "ejemplo_NE.csv")
    }
    
    # Crear botones de descarga para cada marca
    for marca, file_path in example_files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                brand_name = brand_info[marca]["name"]
                icon = brand_info[marca]["icon"]
                
                st.download_button(
                    label=f"{icon} {marca} - {brand_name}",
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
    
    
    
    # Footer del sidebar
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.75rem;">
        <strong>Data Cleaner Pro</strong><br>
        v2.0 • MongoDB Integration
    </div>
    """, unsafe_allow_html=True)

# Área principal con tabs
tab1, tab2 = st.tabs(["🧹 Limpieza de Datos", "📋 Plantillas"])

with tab1:
    st.markdown("### 📁 Cargar Archivo")
    
    # Upload area con diseño personalizado
    upload_container = st.container()
    with upload_container:
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo",
            type=['csv', 'xlsx', 'xls'],
            help="Arrastra y suelta o haz clic para seleccionar",
            label_visibility="collapsed"
        )
    
    # Procesar archivo subido
    if uploaded_file is not None:
        # Detección automática de marca
        detected_brand = detect_brand_from_filename(uploaded_file.name)
        
        # Container para info del archivo
        file_info_container = st.container()
        with file_info_container:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**📄 {uploaded_file.name}**")
                pattern_type = "Patrón L+número" if re.search(r'L\d+', uploaded_file.name.upper()) else "Patrón directo"
                st.caption(f"Tipo: {pattern_type}")
            
            with col2:
                if detected_brand and detected_brand != brand:
                    st.markdown(f'<span class="status-warning">Detectado: {detected_brand}</span>', unsafe_allow_html=True)
                    if st.button("🔄 Usar detectado", key="use_detected"):
                        st.session_state['auto_brand'] = detected_brand
                        st.rerun()
                else:
                    st.markdown(f'<span class="status-success">Marca: {brand}</span>', unsafe_allow_html=True)
            
            with col3:
                # Usar marca detectada si está disponible
                if 'auto_brand' in st.session_state:
                    brand = st.session_state['auto_brand']
        
        # Continuar con el resto del procesamiento de archivos
        try:
            file_handler = FileHandler()
            df = file_handler.read_file(uploaded_file)
            
            # Métricas del archivo en cards
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
                    file_size = uploaded_file.size / 1024  # KB
                    size_text = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{size_text}</div>
                        <div class="metric-label">Tamaño</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    # Verificar columnas necesarias
                    required_columns = ["ItemName", "ItemCode", "Empresa"]
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    status = "✓ Válido" if not missing_columns else "✗ Incompleto"
                    status_class = "status-success" if not missing_columns else "status-error"
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Estado</div>
                        <span class="{status_class}">{status}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Mostrar errores si los hay
            if missing_columns:
                st.error(f"❌ Columnas faltantes: {', '.join(missing_columns)}")
            
            # Vista previa de datos
            st.markdown("### 👁️ Vista Previa")
            with st.expander("Mostrar datos", expanded=True):
                st.dataframe(df.head(10), use_container_width=True, height=300)
            
            # Botón de procesamiento
            if not missing_columns:
                process_container = st.container()
                with process_container:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button(
                            "⚡ Procesar Datos", 
                            type="primary", 
                            use_container_width=True,
                            help="Iniciar proceso de limpieza con datos MongoDB"
                        ):
                            with st.spinner("🔄 Procesando datos..."):
                                try:
                                    # Cargar DataFrames de MongoDB
                                    mongo_dataframes = load_mongo_dataframes()
                                    
                                    if not mongo_dataframes:
                                        st.error("❌ Error al conectar con MongoDB")
                                        st.stop()
                                    
                                    # Inicializar el limpiador
                                    cleaner = DataCleaner(brand, mongo_dataframes)
                                    
                                    # Procesar los datos
                                    cleaned_df = cleaner.clean_data(df)
                                    
                                    # Guardar en session state
                                    st.session_state['cleaned_data'] = cleaned_df
                                    st.session_state['original_filename'] = uploaded_file.name
                                    st.session_state['processing_brand'] = brand
                                    
                                    st.success("✅ ¡Procesamiento completado!")
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                                    with st.expander("Ver detalles del error"):
                                        st.exception(e)
        
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")

    else:
        # Placeholder cuando no hay archivo
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #64748b;">
            <h3>📁 Selecciona un archivo para comenzar</h3>
            <p>Soportamos archivos CSV y Excel con detección automática de marca</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📋 Plantilla")
    
    # Upload area con diseño personalizado
    upload_container = st.container()
    with upload_container:
        uploaded_file_template = st.file_uploader(
            "Selecciona tu archivo",
            type=['csv', 'xlsx', 'xls'],
            help="Arrastra y suelta o haz clic para seleccionar",
            key="template_uploader",
            label_visibility="collapsed"
        )
    
    # Procesar archivo subido
    if uploaded_file_template is not None:
        try:
            file_handler = FileHandler()
            df = file_handler.read_file(uploaded_file_template)
            
            # Métricas del archivo en cards
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
                    file_size = uploaded_file_template.size / 1024  # KB
                    size_text = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{size_text}</div>
                        <div class="metric-label">Tamaño</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Vista previa de datos
            st.markdown("### 👁️ Vista Previa")
            with st.expander("Mostrar datos", expanded=True):
                st.dataframe(df.head(10), use_container_width=True, height=300)
            
            # Proceso de transformación de DataFrame
            st.markdown("---")
            st.markdown("### 🔄 Crear Nueva Plantilla")
            
            # Verificar si existen las columnas necesarias
            if 'Empresa' in df.columns and 'ItemCode' in df.columns:
                # Buscar columnas que empiecen con 'U' o 'u' (case insensitive) excluyendo columnas específicas
                excluded_columns = ['U_Sellitem', 'Update', 'U_Style','u_sellitem', 'update', 'u_style']
                u_columns = [col for col in df.columns if col.upper().startswith('U') and col not in excluded_columns]
                
                if u_columns:
                    st.markdown(f"**Columnas encontradas que empiezan con 'U':** {len(u_columns)}")
                    st.write(u_columns)
                    
                    # Botón para procesar
                    if st.button("⚡ Crear Plantilla Excel", type="primary", use_container_width=True):
                        with st.spinner("🔄 Transformando datos..."):
                            try:
                                # Crear el nuevo DataFrame
                                new_rows = []
                                
                                for index, row in df.iterrows():
                                    empresa = row['Empresa']
                                    itemcode = row['ItemCode']
                                    
                                    # Para cada columna que empiece con 'U'
                                    for u_col in u_columns:
                                        valor = row[u_col]
                                        
                                        # Solo incluir si el valor NO es nulo
                                        if pd.notna(valor):
                                            new_row = {
                                                'Pais': '',  # Siempre vacía
                                                'DB': empresa,
                                                'COLUMNA': u_col,
                                                'Codigo_SAP': itemcode,
                                                'VALOR': valor
                                            }
                                            new_rows.append(new_row)
                                
                                # Crear el nuevo DataFrame
                                new_df = pd.DataFrame(new_rows)
                                
                                # Formatear la columna "COLUMNA": U mayúscula y primera letra después de cada _ mayúscula
                                def format_column_name(col_name):
                                    if '_' not in col_name:
                                        return col_name.upper()
                                    else:
                                        parts = col_name.split('_')
                                        formatted_parts = [parts[0].upper()]  # Primera parte siempre mayúscula
                                        for part in parts[1:]:
                                            formatted_parts.append(part.capitalize())  # Primera letra mayúscula, resto minúsculas
                                        return '_'.join(formatted_parts)
                                
                                new_df['COLUMNA'] = new_df['COLUMNA'].apply(format_column_name)
                                
                                # Ordenar por columna "COLUMNA" de forma descendente
                                new_df = new_df.sort_values('COLUMNA', ascending=False)
                                
                                # Guardar en session state
                                st.session_state['transformed_df'] = new_df
                                st.session_state['original_template_filename'] = uploaded_file_template.name
                                
                                st.success("✅ ¡Plantilla creada exitosamente!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error al crear plantilla: {str(e)}")
                                st.exception(e)
                else:
                    st.warning("⚠️ No se encontraron columnas que empiecen con 'U'")
            else:
                missing_cols = []
                if 'Empresa' not in df.columns:
                    missing_cols.append('Empresa')
                if 'ItemCode' not in df.columns:
                    missing_cols.append('ItemCode')
                st.error(f"❌ Columnas faltantes: {', '.join(missing_cols)}")
            
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")
    else:
        # Placeholder cuando no hay archivo
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #64748b;">
            <h3>📁 Selecciona un archivo para comenzar</h3>
            <p>Soportamos archivos CSV y Excel para crear plantillas</p>
        </div>
        """, unsafe_allow_html=True)

# Mostrar resultados de la plantilla transformada
if 'transformed_df' in st.session_state:
    st.markdown("---")
    
    # Header de resultados de plantilla
    template_results_header = st.container()
    with template_results_header:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📊 Plantilla Transformada")
            original_filename = st.session_state.get('original_template_filename', 'archivo.csv')
            st.caption(f"Generada desde: **{original_filename}**")
        
        with col2:
            # Botón de descarga de Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"plantilla_transformada_{timestamp}.xlsx"
            
            # Crear archivo Excel en memoria
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state['transformed_df'].to_excel(writer, sheet_name='Plantilla', index=False)
            
            st.download_button(
                label="📥 Descargar Excel",
                data=output.getvalue(),
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
    
    transformed_df = st.session_state['transformed_df']
    
    # Métricas de la plantilla transformada
    metrics_container = st.container()
    with metrics_container:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(transformed_df):,}</div>
                <div class="metric-label">📊 Total Filas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            unique_db = transformed_df['DB'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{unique_db}</div>
                <div class="metric-label">🏢 Empresas Únicas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unique_columns = transformed_df['COLUMNA'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{unique_columns}</div>
                <div class="metric-label">📋 Columnas 'U'</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            unique_items = transformed_df['Codigo_SAP'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{unique_items}</div>
                <div class="metric-label">🔢 Códigos SAP</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Vista previa de la plantilla transformada
    st.markdown("### 👁️ Vista Previa de la Plantilla")
    with st.expander("Mostrar plantilla transformada", expanded=True):
        st.dataframe(transformed_df.head(20), use_container_width=True, height=400)
    
    # Información adicional
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

# Espaciado y separador
st.markdown("<br>", unsafe_allow_html=True)

# Mostrar resultados con diseño mejorado
if 'cleaned_data' in st.session_state:
    st.markdown("---")
    
    # Header de resultados
    results_header = st.container()
    with results_header:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🎯 Resultados del Procesamiento")
            brand_used = st.session_state.get('processing_brand', 'N/A')
            st.caption(f"Procesado como: **{brand_used}** • {st.session_state.get('original_filename', 'archivo.csv')}")
        
        with col2:
            # Botón de descarga principal
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{brand_used.lower()}_cleaned_{timestamp}.csv"
            csv_data = st.session_state['cleaned_data'].to_csv(index=False, sep=';')
            
            st.download_button(
                label="💾 Descargar",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                type="primary",
                use_container_width=True
            )
    
    cleaned_df = st.session_state['cleaned_data']
    
    # Métricas principales en cards
    metrics_container = st.container()
    with metrics_container:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(cleaned_df):,}</div>
                <div class="metric-label">📊 Total Filas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(cleaned_df.columns)}</div>
                <div class="metric-label">📋 Columnas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            null_rows = cleaned_df.isnull().sum().sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #dc2626;">{null_rows:,}</div>
                <div class="metric-label">❌ Celdas Incompletas</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            complete_rows = cleaned_df.notnull().sum().sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #12a14b;">{complete_rows:,}</div>
                <div class="metric-label">✅ Celdas Completas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            completeness = (complete_rows - null_rows) / complete_rows * 100 if complete_rows > 0 else 0
            color = "#059669" if completeness > 80 else "#d97706" if completeness > 60 else "#dc2626"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">{completeness:.1f}%</div>
                <div class="metric-label">✅ Completitud</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabs para diferentes vistas
    tab1, tab2 = st.tabs(["📋 Datos Procesados", "📈 Análisis de Calidad"])
    
    with tab1:
        st.markdown("#### Vista de Datos")
        st.dataframe(cleaned_df, use_container_width=True, height=400)
        
        # Información adicional
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Primeras columnas:**")
            st.write(list(cleaned_df.columns[:5]))
        with col2:
            st.markdown("**Últimas columnas:**")
            st.write(list(cleaned_df.columns[-5:]))
    
    with tab2:
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
            null_df = null_df[null_df['Nulos'] > 0]  # Solo mostrar columnas con nulos
            
            if len(null_df) > 0:
                st.dataframe(null_df, use_container_width=True, height=300)
            else:
                st.success("🎉 ¡No hay valores nulos en ninguna columna!")
        
        with col2:
            st.markdown("**Estadísticas de Tipos de Datos**")
            dtypes_count = cleaned_df.dtypes.value_counts()
            dtypes_df = pd.DataFrame({
                'Tipo': dtypes_count.index.astype(str),
                'Cantidad': dtypes_count.values
            })
            st.dataframe(dtypes_df, use_container_width=True, height=300)
        
        # Resumen de calidad
        st.markdown("#### 📊 Resumen de Calidad")
        total_cells = len(cleaned_df) * len(cleaned_df.columns)
        null_cells = cleaned_df.isnull().sum().sum()
        quality_score = ((total_cells - null_cells) / total_cells * 100) if total_cells > 0 else 0
        
        if quality_score >= 95:
            quality_status = "🟢 Excelente"
            quality_color = "#059669"
        elif quality_score >= 80:
            quality_status = "🟡 Buena"
            quality_color = "#d97706"
        else:
            quality_status = "🔴 Requiere atención"
            quality_color = "#dc2626"
        
        st.markdown(f"""
        <div style="background: {quality_color}15; border: 1px solid {quality_color}30; border-radius: 8px; padding: 1.5rem; margin: 1rem 0;">
            <h4 style="color: {quality_color}; margin: 0;">Puntuación de Calidad: {quality_score:.1f}%</h4>
            <p style="margin: 0.5rem 0 0 0; color: #64748b;">Estado: {quality_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    

# Footer moderno
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">⚡ Data Cleaner Pro</div>
    <div style="font-size: 0.9rem;">Procesamiento inteligente de datos • Integración MongoDB • v2.0</div>
</div>
""", unsafe_allow_html=True)
