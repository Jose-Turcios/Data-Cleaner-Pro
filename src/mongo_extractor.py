import pandas as pd
from pymongo import MongoClient
import logging
from datetime import datetime, timedelta
import sys
import os
import streamlit as st

# Configuración de MongoDB usando secrets.toml
try:
    MONGO_CONFIG = {
        "mongouri": st.secrets["MONGO_URI"],
        "db": st.secrets["MONGO_DB_NAME"]
    }
except KeyError as e:
    print(f"Error: Secret no encontrado: {e}")
    MONGO_CONFIG = {
        "mongouri": None,
        "db": None
    }

def extraer_todas_las_colecciones():
    """Extrae todas las colecciones de la base de datos MongoDB"""
    try:
        # Debug: verificar configuración
        if not MONGO_CONFIG["mongouri"]:
            print("ERROR: MONGO_URI no está configurado")
            return []
        
        if not MONGO_CONFIG["db"]:
            print("ERROR: MONGO_DB_NAME no está configurado")
            return []
        
        print(f"Intentando conectar a base de datos: {MONGO_CONFIG['db']}")
        
        client = MongoClient(MONGO_CONFIG["mongouri"])
        
        # Test de conexión
        client.admin.command('ping')
        print("✓ Conexión a MongoDB exitosa")
        
        db = client[MONGO_CONFIG["db"]]
        colecciones = db.list_collection_names()
        
        print(f"Base de datos: {MONGO_CONFIG['db']}")
        print(f"Total de colecciones encontradas: {len(colecciones)}")
        print("\nColecciones:")
        for i, coleccion in enumerate(colecciones, 1):
            print(f"{i}. {coleccion}")
            
        client.close()
        return colecciones
        
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        return []

def extraer_datos_coleccion(nombre_coleccion, limite=None):
    """Extrae datos de una colección específica"""
    try:
        client = MongoClient(MONGO_CONFIG["mongouri"])
        db = client[MONGO_CONFIG["db"]]
        coleccion = db[nombre_coleccion]
        
        if limite:
            datos = list(coleccion.find().limit(limite))
        else:
            datos = list(coleccion.find())
            
        print(f"Colección '{nombre_coleccion}': {len(datos)} documentos extraídos")
        
        client.close()
        return datos
        
    except Exception as e:
        print(f"Error al extraer datos de la colección '{nombre_coleccion}': {e}")
        return []

def crear_dataframe_de_coleccion(nombre_coleccion, limite=None):
    """Crea un DataFrame de pandas desde una colección de MongoDB"""
    try:
        datos = extraer_datos_coleccion(nombre_coleccion, limite)
        if datos:
            df = pd.DataFrame(datos)
            print(f"DataFrame creado para '{nombre_coleccion}': {df.shape[0]} filas, {df.shape[1]} columnas")
            return df
        else:
            print(f"No se pudieron obtener datos de la colección '{nombre_coleccion}'")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error al crear DataFrame para '{nombre_coleccion}': {e}")
        return pd.DataFrame()

def crear_dataframes_de_todas_las_colecciones(limite=None):
    """Crea DataFrames de todas las colecciones en la base de datos"""
    dataframes = {}
    
    try:
        colecciones = extraer_todas_las_colecciones()
        
        for coleccion in colecciones:
            print(f"\nProcesando colección: {coleccion}")
            df = crear_dataframe_de_coleccion(coleccion, limite)
            
            if not df.empty:
                dataframes[coleccion] = df
                print(f"✓ DataFrame '{coleccion}' creado exitosamente")
            else:
                print(f"✗ No se pudo crear DataFrame para '{coleccion}'")
        
        print(f"\n=== RESUMEN ===")
        print(f"Total de colecciones procesadas: {len(colecciones)}")
        print(f"DataFrames creados exitosamente: {len(dataframes)}")
        
        for nombre, df in dataframes.items():
            print(f"- {nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")
            
        return dataframes
        
    except Exception as e:
        print(f"Error al crear DataFrames de todas las colecciones: {e}")
        return {}

if __name__ == "__main__":
    print("=== Extractor de Colecciones MongoDB ===")
    dataframes = crear_dataframes_de_todas_las_colecciones()
    
    if dataframes:
        print(f"\n✓ DataFrames creados exitosamente!")
        for nombre, df in dataframes.items():
            print(f"- {nombre}: {df.shape[0]} filas, {df.shape[1]} columnas")
    else:
        print("No se pudieron crear DataFrames.")

