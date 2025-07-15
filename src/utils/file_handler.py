import pandas as pd
import io
import streamlit as st

class FileHandler:
    """Manejador de archivos para cargar y procesar diferentes formatos"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'xlsx', 'xls']
    
    def read_file(self, uploaded_file):
        """
        Lee un archivo subido y retorna un DataFrame
        
        Args:
            uploaded_file: Archivo subido a través de Streamlit
            
        Returns:
            pd.DataFrame: DataFrame con los datos del archivo
        """
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                return self._read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                return self._read_excel(uploaded_file)
            else:
                raise ValueError(f"Formato de archivo no soportado: {file_extension}")
                
        except Exception as e:
            st.error(f"Error al leer el archivo: {str(e)}")
            raise e
    
    def _read_csv(self, uploaded_file):
        """Lee un archivo CSV con diferentes delimitadores"""
        try:
            # Intentar con punto y coma primero
            df = pd.read_csv(uploaded_file, delimiter=';', encoding='utf-8')
            return df
        except:
            try:
                # Intentar con coma
                uploaded_file.seek(0)  # Resetear el cursor del archivo
                df = pd.read_csv(uploaded_file, delimiter=',', encoding='utf-8')
                return df
            except:
                try:
                    # Intentar con encoding latin-1
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, delimiter=';', encoding='latin-1')
                    return df
                except Exception as e:
                    # Último intento con detección automática
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                    return df
    
    def _read_excel(self, uploaded_file):
        """Lee un archivo Excel"""
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            return df
        except Exception as e:
            st.error(f"Error al leer el archivo Excel: {str(e)}")
            raise e
    
    def save_to_csv(self, df, filename, delimiter=';'):
        """
        Guarda un DataFrame como CSV
        
        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo
            delimiter: Delimitador a usar
            
        Returns:
            str: Contenido del CSV como string
        """
        return df.to_csv(index=False, sep=delimiter, encoding='utf-8')
    
    def validate_required_columns(self, df, required_columns):
        """
        Valida que el DataFrame tenga las columnas requeridas
        
        Args:
            df: DataFrame a validar
            required_columns: Lista de columnas requeridas
            
        Returns:
            tuple: (es_valido, columnas_faltantes)
        """
        missing_columns = [col for col in required_columns if col not in df.columns]
        return len(missing_columns) == 0, missing_columns
    
    def get_file_info(self, df):
        """
        Obtiene información básica del archivo
        
        Args:
            df: DataFrame
            
        Returns:
            dict: Información del archivo
        """
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
