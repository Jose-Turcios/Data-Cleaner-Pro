import pandas as pd
import numpy as np
import streamlit as st
import warnings
from typing import Dict
warnings.filterwarnings('ignore')

class DataCleaner:
    def __init__(self, brand: str, mongo_dataframes: Dict[str, pd.DataFrame]):
        """
        Inicializa el DataCleaner con la marca y los DataFrames de MongoDB.
        
        Args:
            brand: Código de la marca (CH, CL, SK, NE, etc.)
            mongo_dataframes: Diccionario con los DataFrames de MongoDB (colecciones por marca)
        """
        self.brand = brand.upper()
        self.mongo_dataframes = mongo_dataframes
        self.brand_configs = {
            "CH": {
                "name": "Cole Haan",
                "columns": ["ItemName", "ItemCode", "Empresa", "U_Estilo", "U_Genero", "U_Categoria", 
                           "U_Segmento", "U_Descripcion", "U_Descrip_Color", "U_Segmentacion_SK", "U_Zone", "U_Talla"]
            },
            "CL": {
                "name": "Columbia", 
                "columns": ["ItemName", "ItemCode", "Empresa", "u_estilo", "u_descripcion", 
                           "u_descrip_color", "u_cod_color", "u_genero"]
            },
            "SK": {
                "name": "Skechers", 
                "columns": ["ItemName", "ItemCode", "Empresa", "createdate", "updatedate", 
                           "U_Estilo", "U_Genero", "U_Division", "U_Suela", "U_Temporalidad", 
                           "U_Segmentacion_SK", "U_Descripcion", "U_Descrip_Color", "BarCode"]
            },
            "NE": {
                "name": "New Era",
                "columns": ["ItemCode", "Empresa", "ItemName", "U_Talla", "U_Estilo", "U_Silueta", 
                            "U_Team", "U_Descrip_Color", "U_Segmento", "U_Liga", "U_Coleccion_NE", 
                            "U_Genero", "U_Descripcion", "U_Temporalidad"]
            },
            "BI": {
                "name": "Birkenstock",
                "columns": ["ItemName", "ItemCode", "Empresa", "U_Estilo", "U_Genero", "U_Categoria"]
            },
            "PB": {
                "name": "Psycho Bunny",
                "columns": ["ItemName", "ItemCode", "Empresa", "U_Estilo", "U_Genero", "U_Categoria"]
            },
            "AD": {
                "name": "Adolfo",
                "columns": ["ItemName", "ItemCode", "Empresa", "U_Estilo", "U_Genero", "U_Categoria"]
            }
        }
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia los datos según la marca especificada usando los DataFrames de MongoDB"""
        if self.brand not in self.brand_configs:
            raise ValueError(f"Marca no soportada: {self.brand}")
        
        # Copia del DataFrame original
        cleaned_df = df.copy()
        
        # Validar columnas requeridas
        required_cols = ["ItemName", "ItemCode", "Empresa"]
        missing_cols = [col for col in required_cols if col not in cleaned_df.columns]
        if missing_cols:
            raise ValueError(f"Columnas faltantes: {missing_cols}")
        
        # Aplicar limpieza específica por marca
        if self.brand == "CH":
            cleaned_df = self._clean_cole_haan(cleaned_df)
        elif self.brand == "CL":
            cleaned_df = self._clean_columbia(cleaned_df)
        elif self.brand == "SK":
            cleaned_df = self._clean_skechers(cleaned_df)
        elif self.brand == "NE":
            cleaned_df = self._clean_new_era(cleaned_df)
        elif self.brand in ["BI", "PB", "AD"]:
            cleaned_df = self._clean_generic_brand(cleaned_df)
        
        return cleaned_df
    
    def _get_reference_dataframe(self, brand: str) -> pd.DataFrame:
        """Obtiene el DataFrame de referencia para la marca desde los DataFrames de MongoDB"""
        brand_name = self.brand_configs.get(brand, {}).get("name", "")
        if not brand_name:
            return pd.DataFrame()
        
        # Buscar el DataFrame correspondiente en los datos de MongoDB
        for df_name, df in self.mongo_dataframes.items():
            if brand_name.lower() in df_name.lower():
                return df.copy()
        
        return pd.DataFrame()
    
    def _clean_cole_haan(self, df: pd.DataFrame) -> pd.DataFrame:
        """Proceso de limpieza para Cole Haan usando DataFrames de MongoDB"""
        cleaned_df = df.copy()
        
        # Obtener DataFrame de referencia de MongoDB
        df_reference = self._get_reference_dataframe("CH")
        if df_reference.empty:
            st.warning("No se encontró el DataFrame de referencia para Cole Haan")
            return cleaned_df
        
        # Procesamiento similar al original pero usando df_reference en lugar de los archivos L
        # Extraer U_Estilo de ItemName
        cleaned_df['U_Estilo'] = cleaned_df['ItemName'].str.split('/').str[0]
        cleaned_df['U_Descripcion'] = cleaned_df['ItemName'].str.split('/').str[1]
        
        # Asignar U_Genero y U_Categoria basado en el primer carácter
        conditions = [
            cleaned_df['U_Estilo'].str.startswith('F'),
            cleaned_df['U_Estilo'].str.startswith('W'),
            cleaned_df['U_Estilo'].str.startswith('C'),
            cleaned_df['U_Estilo'].str.startswith('U')
        ]
        choices = ['MACC', 'WFW', 'MFW', 'WACC']
        cleaned_df['U_Genero'] = np.select(conditions, choices, default='')
        cleaned_df['U_Categoria'] = cleaned_df['U_Genero']
        
        # Asignar U_Segmento según reglas
        cleaned_df['U_Segmento'] = np.where(
            cleaned_df['U_Genero'].isin(['WFW', 'MFW']),
            'FOOTWEAR',
            np.where(cleaned_df['U_Genero'].isin(['MACC', 'WACC']), 'ACCESSORIES', '')
        )
        
        # Hacer merge con el DataFrame de referencia
        if not df_reference.empty:
            # Seleccionar solo las columnas necesarias del DataFrame de referencia
            ref_columns = ['U_Estilo', 'U_Segmentacion_SK', 'U_Zone', 'U_Descrip_Color']
            ref_columns = [col for col in ref_columns if col in df_reference.columns]
            
            df_reference = df_reference[ref_columns].drop_duplicates('U_Estilo')
            
            # Realizar el merge
            df_resultado = pd.merge(
                cleaned_df.drop(columns=[ 'U_Segmentacion_SK', 'U_Zone', 'U_Descrip_Color'], 
                errors='ignore'),
                df_reference,
                on='U_Estilo',
                how='left'
            )
        else:
            df_resultado = cleaned_df.copy()
        
        # Reordenar columnas
        column_order = [
            'ItemName', 'ItemCode', 'Empresa', 'U_Estilo', 'U_Genero', 'U_Categoria',
            'U_Segmento', 'U_Descripcion', 'U_Descrip_Color', 'U_Segmentacion_SK', 'U_Zone'
        ]
        df_resultado = df_resultado.reindex(columns=[col for col in column_order if col in df_resultado.columns])
        
        # Agregar U_Talla si no existe
        if 'U_Talla' not in df_resultado.columns:
            df_resultado['U_Talla'] = df_resultado['ItemName'].str.split('/').str[2]
        
        return df_resultado
    
    def _clean_columbia(self, df: pd.DataFrame) -> pd.DataFrame:
        """Proceso de limpieza para Columbia usando DataFrames de MongoDB"""
        cleaned_df = df.copy()
        
        # Obtener DataFrame de referencia de MongoDB
        df_reference = self._get_reference_dataframe("CL")
        if not df_reference.empty:
            # Si hay datos de referencia, podemos usarlos para completar información faltante
            pass  # Columbia no usa mucho datos de referencia en su proceso original
        
        # Proceso literal del CL.PY (líneas 7-31)
        # 1. Extraer información de ItemName
        cleaned_df['u_estilo'] = cleaned_df['ItemName'].str.split('/').str[0]
        cleaned_df['u_descripcion'] = cleaned_df['ItemName'].str.split('/').str[1]
        cleaned_df['u_descrip_color'] = cleaned_df['ItemName'].str.split('/').str[3]
        
        # Manejar casos donde u_descrip_color es NaN y convertir a string
        cleaned_df['u_descrip_color'] = cleaned_df['u_descrip_color'].fillna('').astype(str)
        cleaned_df['u_cod_color'] = cleaned_df['u_descrip_color'].str.split('-').str[1]
        
        # Definir condiciones y valores
        # Asegurar que ItemCode es string
        cleaned_df['ItemCode'] = cleaned_df['ItemCode'].astype(str)
        
        conditions = [
            cleaned_df['ItemCode'].str.startswith('3'),               # MENS
            cleaned_df['ItemCode'].str.startswith(('804', '805')),    # UNISEX
            cleaned_df['ItemCode'].str.startswith('4'),               # WOMENS
            cleaned_df['ItemCode'].str.startswith('5'),               # YOUTH BOYS
            cleaned_df['ItemCode'].str.startswith('6'),               # YOUTH GIRLS
            cleaned_df['ItemCode'].str.startswith('802')              # YOUTH UNISEX
        ]
        
        choices = ['MENS', 'UNISEX', 'WOMENS', 'YOUTH BOYS', 'YOUTH GIRLS', 'YOUTH UNISEX']
        
        # Aplicar condiciones
        cleaned_df['u_genero'] = np.select(conditions, choices, default='')
        
        return cleaned_df
    
    def _clean_skechers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Proceso de limpieza para Skechers usando DataFrames de MongoDB"""
        # El DF de entrada es como sk.csv
        df_null_sk = df.copy()
        
        # Obtener DataFrames de referencia de MongoDB
        df_sk = self._get_reference_dataframe("SK")
        
        if df_sk.empty:
            st.warning("No se encontró el DataFrame de referencia para Skechers")
            return df_null_sk
        
        # Inicializar columnas que podrían no existir en el DataFrame de entrada
        required_columns = ['U_Estilo', 'U_Genero', 'U_Suela', 'U_Descrip_Color', 
                           'U_Segmentacion_SK', 'U_Division', 'U_Temporalidad', 'U_Descripcion']
        for col in required_columns:
            if col not in df_null_sk.columns:
                df_null_sk[col] = np.nan
        
        # 1. Extraer u_estilo de ItemName
        df_null_sk['U_Estilo'] = df_null_sk['ItemName'].str.split('/').str[0]
        
        # 2. Condiciones de validación
        tiene_slash = df_null_sk['ItemName'].str.contains('/')
        formato_correcto = (
            df_null_sk['U_Estilo'].str.len() >= 2
        ) & (
            df_null_sk['U_Estilo'].str[0].str.isalnum()
        )
        
        # 3. Condición final: válido si cumple ambas
        cond_valido = tiene_slash & formato_correcto
        
        # 4. Separar válidos e inválidos
        df_valido = df_null_sk[cond_valido].copy()
        df_invalido = df_null_sk[~cond_valido].copy()
        
        # 5. Limpiar u_estilo en los inválidos
        df_invalido['U_Estilo'] = np.nan
        
        # 6. Procesar válidos - extraer descripción
        df_valido['U_Descripcion'] = df_valido['ItemName'].str.split('/').str[1]
        
        # Eliminar "Americana" seguido de número
        df_valido['U_Descripcion'] = df_valido['U_Descripcion'].str.replace(
            r'(?i)americana\s*\d+(?:\.\d+)?', '', regex=True
        )
        
        # 7. Usar solo las columnas disponibles en MongoDB para completar datos
        available_mongo_columns = list(df_sk.columns)
        
        # Preparar DataFrame de referencia usando U_Estilo como clave
        if 'U_Estilo' in available_mongo_columns:
            df_reference = df_sk[['U_Estilo'] + [col for col in ['U_Genero', 'U_Suela', 'U_Division', 'U_Temporalidad'] 
                                                 if col in available_mongo_columns]].copy()
            
            # Limpiar duplicados por U_Estilo
            df_reference = df_reference.drop_duplicates('U_Estilo')
            
            # Asegurar tipos compatibles
            df_reference['U_Estilo'] = df_reference['U_Estilo'].astype(str)
            df_valido['U_Estilo'] = df_valido['U_Estilo'].astype(str)
            df_invalido['U_Estilo'] = df_invalido['U_Estilo'].astype(str)
            
            # Merge para válidos - usar U_Estilo como clave
            df_valido = pd.merge(
                df_valido,
                df_reference,
                on='U_Estilo',
                how='left',
                suffixes=('', '_ref')
            )
            
            # Completar columnas faltantes para válidos
            for col in ['U_Genero', 'U_Suela', 'U_Division', 'U_Temporalidad']:
                col_ref = f'{col}_ref'
                if col_ref in df_valido.columns:
                    # Usar datos de MongoDB para completar valores faltantes
                    df_valido[col] = df_valido[col].fillna(df_valido[col_ref])
                    df_valido.drop(columns=[col_ref], inplace=True)
            
            # Merge para inválidos - también intentar completar por U_Estilo
            df_invalido = pd.merge(
                df_invalido,
                df_reference,
                on='U_Estilo',
                how='left',
                suffixes=('', '_ref')
            )
            
            # Completar columnas faltantes para inválidos
            for col in ['U_Genero', 'U_Suela', 'U_Division', 'U_Temporalidad']:
                col_ref = f'{col}_ref'
                if col_ref in df_invalido.columns:
                    # Usar datos de MongoDB para completar valores faltantes
                    df_invalido[col] = df_invalido[col].fillna(df_invalido[col_ref])
                    df_invalido.drop(columns=[col_ref], inplace=True)
        
        # 8. Concatenar válidos e inválidos
        df_final = pd.concat([df_valido, df_invalido], ignore_index=True)
        
        # 9. Mostrar estadísticas de limpieza
        total_rows = len(df_final)
        completed_rows = len(df_final[df_final['U_Genero'].notna() | df_final['U_Suela'].notna() | 
                                     df_final['U_Division'].notna() | df_final['U_Temporalidad'].notna()])
        
        st.success(f"Skechers: Se completaron {completed_rows} de {total_rows} filas con datos de MongoDB")
        
        return df_final
    
    def _clean_new_era(self, df: pd.DataFrame) -> pd.DataFrame:
        """Proceso de limpieza para New Era usando DataFrames de MongoDB"""
        # El DF de entrada es como DataNull.csv
        df_null = df.copy()
        
        # Obtener DataFrame de referencia de MongoDB
        df_reference = self._get_reference_dataframe("NE")
        if df_reference.empty:
            st.warning("No se encontró el DataFrame de referencia para New Era")
            return df_null
        
        # Inicializar columnas que podrían no existir en el DataFrame de entrada
        required_columns = ['U_Estilo', 'U_Silueta', 'U_Team', 'U_Descrip_Color', 'U_Segmento',
                           'U_Liga', 'U_Coleccion_NE', 'U_Genero', 'U_Descripcion', 'U_Temporalidad', 'U_Talla']
        for col in required_columns:
            if col not in df_null.columns:
                df_null[col] = np.nan
        
        # Procesar DataFrame principal
        df_null['U_Estilo'] = df_null['ItemName'].str.split('/').str[0]
        df_null['U_Descripcion'] = (
            df_null['ItemName']
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .str.split('/')
            .str[1]
            .str.strip()
        )
        df_null['U_Talla'] = df_null['ItemName'].str.split('/').str[2]
        
        # Completar datos desde el DataFrame de referencia
        columnas_completar = ['U_Estilo', 'U_Silueta', 'U_Team', 'U_Descrip_Color', 'U_Segmento',
                             'U_Liga', 'U_Coleccion_NE', 'U_Genero', 'U_Descripcion', 'U_Temporalidad']
        columnas_extra = ['ItemCode', 'Empresa', 'ItemName', 'U_Talla']
        
        df_reference = df_reference[columnas_completar]
        df_null = df_null.reindex(columns=columnas_completar + columnas_extra)
        
        df_reference['U_Estilo'] = df_reference['U_Estilo'].astype(str)
        df_null['U_Estilo'] = df_null['U_Estilo'].astype(str)
        
        df_reference = df_reference.drop_duplicates('U_Estilo').reset_index(drop=True)
        
        temp_df = df_null[columnas_extra + ['U_Estilo']].merge(
            df_reference, 
            on='U_Estilo', 
            how='left',
            suffixes=('', '_ref')
        )
        
        for col in columnas_completar[1:]:
            mask = df_null[col].isnull()
            if col in temp_df.columns:
                df_null.loc[mask, col] = temp_df.loc[mask, col]
        
        # Aplicar team_licenses
        team_licenses = {
            'LOS ANGELES DODGERS': 'MLB', 'NEW YORK YANKEES': 'MLB', 'PITTSBURGH PIRATES': 'MLB',
            'SAN FRANCISCO GIANTS': 'MLB', 'SEATTLE MARINERS': 'MLB', 'TAMPA BAY RAYS': 'MLB',
            'NEW ERA BRANDED': 'NEW ERA BRANDED', 'NO APLICA': 'NO APLICA', 'NEW ENGLAND PATRIOTS': 'NFL',
            'HOUSTON TEXANS': 'NFL', 'BALTIMORE RAVENS': 'NFL', 'TORONTO BLUE JAYS': 'MLB',
            'HOUSTON ASTROS': 'MLB', 'GREEN BAY PACKERS': 'NFL', 'BOSTON RED SOX': 'MLB',
            'BALTIMORE ORIOLES': 'MLB', 'ST. LOUIS CARDINALS': 'MLB', 'SEATTLE SEAHAWKS': 'NFL',
            'DALLAS COWBOYS': 'NFL', 'PITTSBURGH STEELERS': 'NFL', 'MIAMI DOLPHINS': 'NFL',
            'STARWARS': 'ENTERTAINMENT', 'DALLAS MAVERICKS': 'NBA', 'LOS ANGELES LAKERS': 'NBA',
            'NEW ORLEANS SAINTS': 'NFL', 'JACKSONVILLE JAGUARS': 'NFL', 'CLEVELAND BROWNS': 'NFL',
            'NEW YORK KNICKS': 'NBA', 'SAN ANTONIO SPURS': 'NBA', 'WASHINGTON NATIONALS': 'MLB',
            'OAKLAND ATHLETICS': 'MLB', 'DETROIT TIGERS': 'MLB', 'ANAHEIM ANGELS': 'MLB',
            'NASCAR': 'MOTORSPORT', 'NEW YORK METS': 'MLB', 'PHILADELPHIA PHILLIES': 'MLB',
            'CHICAGO WHITE SOX': 'MLB', 'SAN DIEGO PADRES': 'MLB', 'CLEVELAND INDIANS': 'MLB',
            'DENVER BRONCOS': 'NFL', 'BUFFALO BILLS': 'NFL', 'ATLANTA FALCONS': 'NFL',
            'CHICAGO BEARS': 'NFL', 'BROOKLYN NETS': 'NBA', 'CHICAGO BULLS': 'NBA',
            'SAN FRANCISCO 49ERS': 'NFL', 'INDIANAPOLIS COLTS': 'NFL', 'ARIZONA CARDINALS': 'NFL',
            'OAKLAND RAIDERS': 'NFL', 'LOS ANGELES RAMS': 'NFL', 'TAMPA BAY BUCCANEERS': 'NFL',
            'GOLDEN STATE WARRIORS': 'NBA', 'BOSTON CELTICS': 'NBA', 'CHICAGO CUBS': 'MLB'
        }
        
        # Aplicar team_licenses
        registros_en_blanco = df_null[df_null['U_Liga'].isna() | (df_null['U_Liga'] == '')]
        
        for index, row in registros_en_blanco.iterrows():
            equipo = row['U_Team']
            if equipo in team_licenses:
                df_null.at[index, 'U_Liga'] = team_licenses[equipo]
        
        return df_null
    
    def _clean_generic_brand(self, df: pd.DataFrame) -> pd.DataFrame:
        """Proceso de limpieza genérico para marcas sin proceso específico (Birkenstock, Psycho Bunny, Adolfo)"""
        cleaned_df = df.copy()
        
        # Obtener DataFrame de referencia de MongoDB
        df_reference = self._get_reference_dataframe(self.brand)
        
        # Extraer información básica del ItemName
        cleaned_df['U_Estilo'] = cleaned_df['ItemName'].str.split('/').str[0]
        cleaned_df['U_Descripcion'] = cleaned_df['ItemName'].str.split('/').str[1]
        
        # Si hay datos de referencia, completar información faltante
        if not df_reference.empty:
            # Seleccionar solo las columnas necesarias del DataFrame de referencia
            ref_columns = ['U_Estilo', 'U_Genero', 'U_Categoria']
            ref_columns = [col for col in ref_columns if col in df_reference.columns]
            
            df_reference = df_reference[ref_columns].drop_duplicates('U_Estilo')
            
            # Realizar el merge para completar información
            cleaned_df = pd.merge(
                cleaned_df,
                df_reference,
                on='U_Estilo',
                how='left',
                suffixes=('', '_ref')
            )
            
            # Completar columnas faltantes
            if 'U_Genero_ref' in cleaned_df.columns:
                cleaned_df['U_Genero'] = cleaned_df['U_Genero'].fillna(cleaned_df['U_Genero_ref'])
                cleaned_df.drop('U_Genero_ref', axis=1, inplace=True)
            
            if 'U_Categoria_ref' in cleaned_df.columns:
                cleaned_df['U_Categoria'] = cleaned_df['U_Categoria'].fillna(cleaned_df['U_Categoria_ref'])
                cleaned_df.drop('U_Categoria_ref', axis=1, inplace=True)
        
        return cleaned_df