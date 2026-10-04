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
                nombre = input("Ingrese el nombre del archivo CSV cargado (ej nombre.csv): ")
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

        elif op == "2":
            menu3 = input("""\nIngrese la opción deseada:
            1. Cargar archivo MAT.
            2. Ver información (variables) de un archivo MAT.
            3. Operar 4 canales (suma, resta o multiplicación).
            4. Promedio y desviación estándar.
            0. Volver al menú principal.
            Coloque aquí su opción: """)

            if menu3 == "0":
                continue

            elif menu3 == "1":
                nombre_archivo = input("Ingrese el nombre del archivo MAT (ej nombre.mat): ")
                try:
                    archivos_mat[nombre_archivo] = sis.Abrir_mat(nombre_archivo)
                    print(f"Archivo {nombre_archivo} cargado exitosamente.")
    
                except (FileNotFoundError, ValueError) as error:
                    print(error)

            elif menu3 in ("2", "3", "4"):
                nombre = input("Ingrese el nombre del archivo MAT cargado (ej. nombre.mat): ")
                if nombre not in archivos_mat:
                    print(f"No se encontró un archivo MAT cargado con el nombre {nombre}.")
                    continue
                archivo = archivos_mat[nombre]

                if menu3 == "2":
                    print(archivo)

                elif menu3 == "3":
                    print(archivo)   # Muestra las dimensiones (canales, muestras, ensayos)

                    oper = input("""Elija la operación:
            1. Suma.
            2. Resta.
            3. Multiplicación.
            Coloque aquí su opción: """)
                    if oper == "1":
                        funcion = archivo.suma
                    elif oper == "2":
                        funcion = archivo.resta
                    elif oper == "3":
                        funcion = archivo.multiplicacion
                    else:
                        print("Opción inválida. Por favor, intente de nuevo.")
                        continue

                    try:
                        canales = []                     
                        for i in range(4):
                            canales.append(int(input(f"Ingrese el canal {i + 1}: ")))
                        punto_inicial = int(input("Ingrese el punto inicial: "))
                        punto_final = int(input("Ingrese el punto final: "))
                    except ValueError:
                        print("Error, los canales y los puntos deben ser números enteros.")
                        continue

                    nombre_salida = input("Ingrese el nombre para guardar el gráfico (ejemplo: suma.png): ")

                    try:
                        archivo.operar_canales(funcion, canales, punto_inicial, punto_final, nombre_salida)
                        print(f"\nGráfico guardado como {nombre_salida}")
                    except ValueError as error:
                        print(error)
                
                else:
                    print(archivo)
                    try:
                        eje1 = int(input("Ingrese el primer eje (0, 1 o 2): "))
                        eje2 = int(input("Ingrese el segundo eje (0, 1 o 2): "))
                    except ValueError:
                        print("Error, los ejes deben ser números enteros.")
                        continue

                    nombre_salida = input("Ingrese el nombre para guardar el gráfico (ejemplo: promedio.png): ")

                    try:
                        archivo.promedio_std(eje1, eje2, nombre_salida)
                        print(f"\nGráfico guardado como {nombre_salida}")
                    except ValueError as error:
                        print(error)

            else:
                print("Opción inválida. Por favor, intente de nuevo.")

        elif op == "3":
            print("Hasta luego.")
            break

        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()