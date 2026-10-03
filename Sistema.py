import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio

class Abrir_csv:
    def __init__(self, nombre_archivo):
        
        try:
            df = pd.read_csv(nombre_archivo)
        except FileNotFoundError:
            raise FileNotFoundError(f'Error, archivo {nombre_archivo} no encontrado.')
        
        self.__nombre = nombre_archivo
        self.__df = df.set_index("time_ms")

    def ver_nombre(self):
        return self.__nombre

    def ver_dataframe(self):
        return self.__df.copy()

    def ver_canales(self):
        canales = []
        for c in self.__df.columns:
            if c != "subject" and c != "condition":
                canales.append(c)
        return canales

    def ver_condiciones(self):
        condiciones = []
        for c in sorted(self.__df["condition"].unique()):
            condiciones.append(int(c))
        return condiciones

# Método __str__
    def __str__(self):
            self.__df.info()
            dimensiones = self.__df.shape
            tipos_columnas = self.__df.dtypes.to_string()
            describe_texto = self.__df.describe().to_string()

            info = f"""
            - Archivo CSV: {self.__nombre}
            - Información general (Resumen alternativo de info):
            - Dimensiones: {dimensiones[0]} filas y {dimensiones[1]} columnas.
            - Tipos de datos por columna:{tipos_columnas}
            - Resumen estadístico (describe):{describe_texto}"""
    return info