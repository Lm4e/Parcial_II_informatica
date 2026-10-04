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
       
    def graficar_condiciones(self, condicion, canal, canal_x, canal_y, ruta_salida):
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

        # Guardado de la gráfica
        plt.savefig(ruta_salida)
        return plt.show()
    
    # Diferencia interhemisferica (consulta)
    def diferencia_interhemisferica(self, canal_izq, canal_der):
        for c in (canal_izq, canal_der):
            if c not in self.ver_canales():
                raise ValueError(f"Error, el canal {c} no existe en el archivo")

        if canal_izq == canal_der:
            raise ValueError("Error, debe elegir dos canales diferentes")

        nombre_columna = f"{canal_izq}-{canal_der}"
        self.__df[nombre_columna] = self.__df.loc[:, canal_izq].sub(self.__df.loc[:, canal_der])
        return self.__df.loc[:, nombre_columna]

    # Aplicación del método __str__
    def __str__(self):
        linea = "=" * 50
        print(f'\n{linea}')
        print(f'Información del archivo {self.__nombre}')
        print(linea)
        self.__df.info()

        return f'\n{linea}\nResumen del archivo\n{linea}\n{self.__df.describe()}\n'

# Clase para ver archivos .mat
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
        self.__fs = 250                              

        if len(self.__matriz.shape) != 3: 
            raise ValueError("Error, la variable elegida no es una matriz 3D")
        self.__info = f"""Archivo mat: {self.__nombre}
Variables (nombre, dimensiones, tipo):
{self.__contenido}""" 

    def __str__(self):
        return self.__info

    def suma(self, c1, c2, c3, c4):
        return c1 + c2 + c3 + c4

    def resta(self, c1, c2, c3, c4):
        return c1 - c2 - c3 - c4

    def multiplicacion(self, c1, c2, c3, c4):
        return c1 * c2 * c3 * c4

    def operar_canales(self, funcion, canales, punto_inicial, punto_final, ruta_salida):

        # Definir qué operación es, y en qué unidad queda el resultado
        if funcion == self.suma:
            operacion = "suma"
            unidad = "µV"
        elif funcion == self.resta:
            operacion = "resta"
            unidad = "µV"
        elif funcion == self.multiplicacion:
            operacion = "multiplicación"
            unidad = "µV^2"                    
        else:
            raise ValueError("Error, la función debe ser suma, resta o multiplicación")
        
        total_canales = self.__matriz.shape[0]
        muestras = self.__matriz.shape[1]
        ensayos = self.__matriz.shape[2]

        if len(canales) != 4:
            raise ValueError("Error, debe elegir 4 canales")
        
        for c in canales:  # que cada canal exista en la matriz
                if c < 0 or c >= total_canales:
                    raise ValueError(f"Error, el canal {c} no existe (hay {total_canales} canales)")
        
        # Tiempo 
        tiempo = np.arange(punto_inicial, punto_final) / self.__fs 
        
        # Reshape para pasar la matriz de 3D a 2D
        
        matriz2d = self.__matriz.reshape(total_canales, muestras * ensayos)

        # Los 4 canales en el rango elegido
        c1 = matriz2d[canales[0], punto_inicial:punto_final]
        c2 = matriz2d[canales[1], punto_inicial:punto_final]
        c3 = matriz2d[canales[2], punto_inicial:punto_final]
        c4 = matriz2d[canales[3], punto_inicial:punto_final]

        resultado = funcion(c1, c2, c3, c4) # Operación con los 4 canales

        plt.figure(figsize=(11, 8))
        
    # subplot 1: los 4 canales

        plt.subplot(2, 1, 1)   
        plt.plot(tiempo, c1, label=f"Canal {canales[0]}")
        plt.plot(tiempo, c2, label=f"Canal {canales[1]}")
        plt.plot(tiempo, c3, label=f"Canal {canales[2]}")
        plt.plot(tiempo, c4, label=f"Canal {canales[3]}")
        plt.title("Canales seleccionados")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud (µV)")
        plt.legend()

    # subplot 2: el resultado

        plt.subplot(2, 1, 2)  
        plt.plot(tiempo, resultado, color="red", label=operacion)
        plt.title(f"Resultado de la {operacion} de los 4 canales")
        plt.xlabel("Tiempo (s)")
        plt.ylabel(f"Amplitud ({unidad})")
        plt.legend()

        plt.tight_layout()
        plt.savefig(ruta_salida) # guardar antes de mostrar
        plt.show()

    def promedio_std(self, eje1, eje2, ruta_salida):
 
        # Validación de los ejes
        if eje1 not in (0, 1, 2) or eje2 not in (0, 1, 2):
            raise ValueError("Error, los ejes deben ser 0, 1 o 2")
        if eje1 == eje2:
            raise ValueError("Error, debe elegir dos ejes diferentes")
 
        # Promedio a lo largo del primer eje  elegido y desviación a lo largo del segundo
        promedio = np.mean(self.__matriz, axis=eje1) # Queda una matriz 2D
        desviacion = np.std(self.__matriz, axis=eje2) # Queda otra matriz 2D
 
        # Forma final de cada resultado
        print(f"Forma del promedio (eje {eje1}): {promedio.shape}")
        print(f"Forma de la desviación (eje {eje2}): {desviacion.shape}")
 
        # Creación de dataframe y uso de ravel() para convertir las matrices en un vector
        tabla = pd.DataFrame({"Promedio": pd.Series(promedio.ravel()),
                              "Desviación estándar": pd.Series(desviacion.ravel())})
 
        # Creación de la boxplot
        plt.figure(figsize=(7, 6))
        ax = plt.axes()
        tabla.boxplot(ax=ax)
        plt.title(f"Promedio (eje {eje1}) y desviación estándar (eje {eje2})")
        plt.xlabel("Estadístico")
        plt.ylabel("Amplitud (µV)")
        plt.savefig(ruta_salida)
        plt.show()