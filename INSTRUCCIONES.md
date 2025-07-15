# 🚀 Instrucciones de Instalación y Ejecución

## Prerrequisitos

1. **Python 3.8 o superior** debe estar instalado
2. **pip** debe estar disponible
3. **git** (opcional, para clonar el repositorio)

## Instalación Paso a Paso

### 1. Descargar el Proyecto
```bash
# Si tienes git instalado:
git clone <url-del-repositorio>
cd streamlit_data_cleaner

# O simplemente descarga y extrae el ZIP
```

### 2. Instalar Dependencias del Sistema (Ubuntu/Debian)
```bash
# Instalar python3-venv si no está instalado
sudo apt update
sudo apt install python3.12-venv python3-pip

# Instalar dependencias adicionales para Excel
sudo apt install python3-dev
```

### 3. Crear Entorno Virtual
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

#### Opción 1: Script Automático (Recomendado)
```bash
# Hacer el script ejecutable
chmod +x start.sh

# Ejecutar
./start.sh
```

#### Opción 2: Ejecución Manual
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar Streamlit
cd src
streamlit run app.py
```

#### Opción 3: Usando VS Code
1. Abrir el proyecto en VS Code
2. Presionar `Ctrl+Shift+P`
3. Buscar "Tasks: Run Task"
4. Seleccionar "Ejecutar Streamlit App"

## Uso de la Aplicación

### 1. Acceder a la Aplicación
Una vez ejecutada, la aplicación se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

### 2. Pasos para Limpiar Datos
1. **Selecciona la marca** en la barra lateral (CH, CL, SK, NE)
2. **Arrastra y suelta** tu archivo CSV o Excel
3. **Revisa la vista previa** de los datos
4. **Haz clic en "Limpiar Datos"**
5. **Descarga el archivo limpio**

### 3. Formato de Datos de Entrada
Tu archivo debe tener estas columnas mínimas:
- `ItemName`: Formato `ESTILO/DESCRIPCION/TALLA/COLOR`
- `ItemCode`: Código del producto
- `Empresa`: Nombre de la empresa

### 4. Archivos de Ejemplo
En la carpeta `data/` encontrarás archivos de ejemplo para cada marca:
- `ejemplo_CH.csv` - Datos de Champion
- `ejemplo_CL.csv` - Datos de Converse
- `ejemplo_SK.csv` - Datos de Skechers
- `ejemplo_NE.csv` - Datos de New Era

## Solución de Problemas

### Error: "externally-managed-environment"
```bash
# Usar entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "python3-venv not found"
```bash
# Instalar en Ubuntu/Debian
sudo apt install python3.12-venv
```

### Error: "streamlit command not found"
```bash
# Asegurarse de activar el entorno virtual
source venv/bin/activate
pip install streamlit
```

### Puerto 8501 en uso
```bash
# Usar puerto diferente
streamlit run app.py --server.port 8502
```

## Estructura del Proyecto

```
streamlit_data_cleaner/
├── src/
│   ├── app.py              # Aplicación principal
│   ├── config.py           # Configuración
│   └── utils/
│       ├── data_cleaner.py # Lógica de limpieza
│       └── file_handler.py # Manejo de archivos
├── data/
│   ├── ejemplo_*.csv       # Archivos de ejemplo
│   ├── uploads/            # Archivos subidos
│   └── processed/          # Archivos procesados
├── venv/                   # Entorno virtual
├── requirements.txt        # Dependencias
├── start.sh               # Script de inicio
└── README.md              # Documentación
```

## Marcas Soportadas

- **CH (Champion)**: Procesamiento completo con categorización
- **CL (Converse)**: Limpieza básica y clasificación por género
- **SK (Skechers)**: Validación avanzada y procesamiento
- **NE (New Era)**: Limpieza especializada para productos deportivos

## Características

- ✅ Interfaz web intuitiva
- ✅ Soporte para CSV y Excel
- ✅ Validación de datos
- ✅ Limpieza automática por marca
- ✅ Descarga de resultados
- ✅ Análisis de calidad de datos
- ✅ Archivos de ejemplo incluidos

## Soporte

Si encuentras problemas:
1. Verifica que Python 3.8+ esté instalado
2. Asegúrate de usar el entorno virtual
3. Revisa que todas las dependencias estén instaladas
4. Consulta los archivos de ejemplo para el formato correcto

---

¡Disfruta limpiando tus datos! 🧹✨
