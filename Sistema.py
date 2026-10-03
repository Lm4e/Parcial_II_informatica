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
        self.__condiciones =[]
        for c in self.__df.loc[:, "condition"]:
            if int(c) not in self.__condiciones:
                self.__condiciones.append(int(c))

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
        return list(self.__condiciones)
       
    def graficar_condiciones(self, condicion, canal, canal_x, canal_y):
        if condicion not in self.__condiciones:
            raise ValueError("Error, la condición elegida no existe en el archivo")

        for c in (canal, canal_x, canal_y):
            if c not in self.ver_canales():
                raise ValueError(f"Error, el canal {c} no existe en el archivo")

        datos = self.__df.loc[self.__df.loc[:, "condition"] == condicion]
        amplitud = datos.loc[:, canal]

        plt.figure(figsize=(12, 10))
        plt.subplot(2, 1, 1)
        plt.bar(datos.index, amplitud)
        plt.plot([0, 0], [min(amplitud), max(amplitud)], color="red")
        plt.title(f"Stem del canal {canal} - Condición {condicion} (línea roja: t = 0 ms)")
        plt.xlabel("Tiempo (ms)")
        plt.ylabel("Amplitud (µV)")

        # Gráfica histograma
        ax_hist = plt.subplot(2, 2, 3)
        amplitud.plot(kind="hist", bins=30, edgecolor="black", ax=ax_hist,
                      title=f"Histograma del canal {canal} - Condición {condicion}",
                      xlabel="Amplitud (µV)", ylabel="Frecuencia (número de muestras)")

        # Gráfica scatter
        ax_scatter = plt.subplot(2, 2, 4)
        datos.plot(kind="scatter", x=canal_x, y=canal_y, s=5, ax=ax_scatter,
                   title=f"Scatter {canal_x} vs {canal_y}",
                   xlabel=f"Canal {canal_x} (µV)", ylabel=f"Canal {canal_y} (µV)")
        return plt.show()
    
    # Diferencia interhemisferica
    def diferencia_interhemisferica(self, canal_izq, canal_der):
        for c in (canal_izq, canal_der):
            if c not in self.ver_canales():
                raise ValueError(f"Error, el canal {c} no existe en el archivo")

        if canal_izq == canal_der:
            raise ValueError("Error, debe elegir dos canales diferentes")

        nombre_columna = f"{canal_izq}-{canal_der}"
        self.__df[nombre_columna] = self.__df.loc[:, canal_izq].sub(self.__df.loc[:, canal_der])
        return self.__df.loc[:, nombre_columna]

    # Método __str__
    def __str__(self):
        linea = "=" * 50
        print(f'\n{linea}')
        print(f'Información del archivo {self.__nombre}')
        print(linea)
        self.__df.info()

        return f'\n{linea}\nResumen del archivo\n{linea}\n{self.__df.describe()}\n'

#Clase para ver archivos .mat
class Abrir_mat:

    def __init__(self, nombre_archivo):

        # Intentamos abrir el archivo; si no existe, mostramos el mensaje de error
        try:
            datos = sio.loadmat(nombre_archivo)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error, archivo {nombre_archivo} no encontrado")

        self.__nombre = nombre_archivo
        self.__contenido = sio.whosmat(nombre_archivo) # Lista de tuplas con (variable, dimensiones, tipo)
        self.__variable = self.__contenido[0][0]
        self.__matriz = datos[self.__variable]

