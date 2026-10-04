import Sistema as sis

# Creación del menú y sub-menús
def main():
    archivos_csv = {}
    archivos_mat = {}

    while True:
        op = input("""\nBienvenido al sistema de análisis de EEG, ingrese la opción deseada:
            1. Archivos CSV (pacientes con esquizofrenia).
            2. Archivos MAT.
            3. Salir.
            Coloque aquí su opción: """)

        if op == "1":
            menu2 = input("""\nIngrese la opción deseada:
            1. Cargar archivo CSV.
            2. Ver información de un archivo CSV.
            3. Graficar por condición (stem, histograma y scatter).
            4. Diferencia interhemisférica entre dos canales.
            0. Volver al menú principal.
            Coloque aquí su opción: """)

            if menu2 == "0":
                continue

            elif menu2 == "1":
                nombre_archivo = input("Ingrese el nombre del archivo CSV (ej nombre.csv): ")
                try:
                    archivo = sis.Abrir_csv(nombre_archivo)
                    archivos_csv[archivo.ver_nombre()] = archivo
                    print(f"Archivo {archivo.ver_nombre()} cargado exitosamente.")

                except (FileNotFoundError, ValueError, KeyError) as error:
                    print(error)

            elif menu2 in ("2", "3", "4"):
                nombre = input("Ingrese el nombre del archivo CSV cargado (ej n.csv): ")
                if nombre not in archivos_csv:
                    print(f"No se encontró un archivo CSV cargado con el nombre {nombre}.")

                archivo = archivos_csv[nombre]

                if menu2 == "2":
                    print(archivo)

                elif menu2 == "3":
                    print(f"Condiciones disponibles: {archivo.ver_condiciones()}")
                    try:
                        condicion = int(input("Ingrese la condición: "))
                    except ValueError:
                        print("Error, la condición debe ser un número entero.")
                        continue
                    print(f"Canales disponibles: {archivo.ver_canales()}")
                    canal = input("Ingrese el canal para el stem y el histograma: ")
                    canal_x = input("Ingrese el canal del eje x para el scatter: ")
                    canal_y = input("Ingrese el canal del eje y para el scatter: ")
                    nombre_salida = input("Ingrese el nombre para guardar el gráfico (ejemplo: grafico.png): ")

                    try:
                        archivo.graficar_condiciones(condicion, canal, canal_x, canal_y, nombre_salida)
                        print(f"\nGráfico guardado como {nombre_salida}")
                    except ValueError as error:
                        print(error)

                else:
                    print(f"Canales disponibles: {archivo.ver_canales()}")
                    canal_izq = input("Ingrese el canal del hemisferio izquierdo (ejemplo: C3): ")
                    canal_der = input("Ingrese el canal del hemisferio derecho (ejemplo: C4): ")

                    try:
                        diferencia = archivo.diferencia_interhemisferica(canal_izq, canal_der)
                        print(f"\nNueva columna creada: {canal_izq}-{canal_der} (en µV). Primeros valores:")
                        print(diferencia.iloc[:10])
                    except ValueError as error:
                        print(error)

            else:
                print("Opción inválida. Por favor, intente de nuevo.")