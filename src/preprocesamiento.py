import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder


class PreprocesamientoDatos:
    
    def __init__(self, df):
        self.df = df.copy()
        self.scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
        self.label_encoders = {}
    
    def informacion_general(self):
        info = {
            'dimensiones': self.df.shape,
            'columnas': self.df.columns.tolist(),
            'tipos_datos': self.df.dtypes.to_dict(),
            'valores_nulos': self.df.isnull().sum().to_dict(),
            'duplicados': self.df.duplicated().sum()
        }
        return info
    
    def manejar_valores_nulos(self, estrategia='mean', columnas=None):
        if columnas is None:
            columnas = self.df.select_dtypes(include=[np.number]).columns
        
        for col in columnas:
            if col in self.df.columns:
                if estrategia == 'mean':
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif estrategia == 'median':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif estrategia == 'most_frequent':
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                elif estrategia == 'drop':
                    self.df.dropna(subset=[col], inplace=True)
        
        return self.df
    
    def eliminar_duplicados(self):
        antes = len(self.df)
        self.df.drop_duplicates(inplace=True)
        despues = len(self.df)
        print(f"Duplicados eliminados: {antes - despues}")
        return self.df
    
    def normalizar(self, columnas=None, metodo='standard'):
        if columnas is None:
            columnas = self.df.select_dtypes(include=[np.number]).columns
        
        if metodo == 'standard':
            self.df[columnas] = self.scaler.fit_transform(self.df[columnas])
        elif metodo == 'minmax':
            self.df[columnas] = self.minmax_scaler.fit_transform(self.df[columnas])
        
        return self.df
    
    def codificar_categoricas(self, columnas=None, metodo='label'):
        if columnas is None:
            columnas = self.df.select_dtypes(include=['object']).columns
        
        if metodo == 'label':
            for col in columnas:
                if col in self.df.columns:
                    le = LabelEncoder()
                    self.df[col] = le.fit_transform(self.df[col].astype(str))
                    self.label_encoders[col] = le
        elif metodo == 'onehot':
            self.df = pd.get_dummies(self.df, columns=columnas)
        
        return self.df
    
    def preprocesamiento_completo(self):
        print("Iniciando preprocesamiento completo...")
        
        print("\n1. Información inicial del dataset:")
        info = self.informacion_general()
        print(f"   Dimensiones: {info['dimensiones']}")
        print(f"   Valores nulos: {sum(info['valores_nulos'].values())}")
        print(f"   Duplicados: {info['duplicados']}")
        
        print("\n2. Eliminando duplicados...")
        self.eliminar_duplicados()
        
        print("\n3. Manejando valores nulos...")
        self.manejar_valores_nulos(estrategia='mean')
        
        print("\n4. Codificando variables categóricas...")
        self.codificar_categoricas(metodo='label')
        
        print("\n5. Normalizando datos...")
        self.normalizar(metodo='standard')
        
        print("\nPreprocesamiento completado exitosamente!")
        print(f"Nuevas dimensiones: {self.df.shape}")
        
        return self.df


def probar_preprocesamiento():
    data = {
        'edad': [25, 30, 35, 30, 25, 40, 35, None, 30, 25],
        'ingresos': [50000, 60000, 75000, 60000, 50000, 80000, 75000, 55000, 60000, 50000],
        'genero': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
        'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona', 
                   'Madrid', 'Valencia', 'Barcelona', 'Madrid', 'Valencia'],
        'puntuacion': [8.5, 7.0, 9.0, 7.5, 8.0, 9.5, 7.0, 8.5, 7.5, 8.0]
    }
    
    df = pd.DataFrame(data)
    
    # Agregamos un duplicado de la primera fila
    df = pd.concat([df, df.iloc[0:1]], ignore_index=True)
    
    print("Dataset original:")
    print(df)
    print("\n" + "="*50 + "\n")
    
    preprocesador = PreprocesamientoDatos(df)
    df_procesado = preprocesador.preprocesamiento_completo()
    
    print("\nDataset procesado:")
    print(df_procesado)
    
    return df_procesado


if __name__ == "__main__":
    probar_preprocesamiento()