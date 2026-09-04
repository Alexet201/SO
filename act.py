from collections import deque
import random
import time
import os

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def ingresoDatos():
    colaProcesos = deque()
    ids = set ()

    while True:
        userName = input("Nombre del usuario: ")
        if userName.strip():
            break
        print("El nombre no puede estar vacío. Por favor, ingresa un nombre válido.")

    while True:
        try:
            nProces = int(input("¿Cuántos procesos quieres ejecutar?: "))
            if nProces > 0:
                break
            print("Ingresa un numero mayor a 0.")
        except ValueError:
            print("Debes ingresar un número entero.")
    

    
    i = 0
    while i < nProces:

        limpiarPantalla()
        
        print("\nIngresa el número de las operaciones del proceso y sus valores")
        print("1.- Suma")
        print("2.- Resta")
        print("3.- Multiplicación")
        print("4.- División")
        print("5.- Residuo\n")
            
        print(f"Datos de la operación {i + 1}")
        band = True
        
        while band: 
            operacion_str = input("Operación (1-5): ")
            primerV_str   = input("Primer valor: ")
            segundoV_str  = input("Segundo valor: ")

            # Validar que los 3 inputs sean numeros enteros 
            if  not (
                    operacion_str.isdigit() 
                    and primerV_str.isdigit() 
                    and segundoV_str.isdigit()
                ):

                print("Error: Todos los campos deben ser números enteros.\n")
                continue  

            # Convertimos a enteros para poder evaluar
            operacion = int(operacion_str)
            primerV   = int(primerV_str)
            segundoV  = int(segundoV_str)

            # Validaciones de rango y división entre cero
            if operacion < 1 or operacion > 5:
                print("Error: La operación debe de ser del 1 al 5.\n")
            elif (operacion == 4 or operacion == 5) and segundoV == 0: 
                print("Error: Con división y residuo el segundo numero no puede ser 0.\n")
            else:
                band = False 
 
        while True:
            id = input ("Ingresa el id de la operacion: ")
            if id in ids: 
                print ("Este id ya fue usado, ingresa otro")
            else: 
                ids.add(id)
                break
        tmp = random.randint(1, 4)
        print(f"El tiempo estimado es {tmp} s")        
        colaProcesos.append((operacion, primerV, segundoV, id, tmp))
        i += 1


    return userName, colaProcesos

def procesarDatos (userName, colaProcesos): 
    contador_global = 0
    terminados = []
    num_lote = 0

    # Iteramos sobre la cola
    while colaProcesos:
        num_lote += 1

        # Cargar el lote actual de 5 procesos
        lote_trabajando = deque()
        for _ in range(5):
            if colaProcesos:
                lote_trabajando.append(colaProcesos.popleft())

        # Calcular lotes pendientes
        lotes_pendientes = (len(colaProcesos) + 4) // 5

        # Procesar los lotes 
        while lote_trabajando:
            # Extraer proceso en actual
            operacion, primerV, segundoV, id_proc, tme = (
                lote_trabajando.popleft()
            )

            # Resolver la operacion 
            if operacion == 1:
                ope_str = f"{primerV} + {segundoV}"
                res = primerV + segundoV
            elif operacion == 2:
                ope_str = f"{primerV} - {segundoV}w"
                res = primerV - segundoV
            elif operacion == 3:
                ope_str = f"{primerV} * {segundoV}"
                res = primerV * segundoV
            elif operacion == 4:
                ope_str = f"{primerV} / {segundoV}"
                res = primerV / segundoV
            elif operacion == 5:
                ope_str = f"{primerV} % {segundoV}"
                res = primerV % segundoV

            # Cronometro (segundero)
            for tt in range(1, tme + 1):
                limpiarPantalla ()
                tr = tme - tt
                contador_global += 1

                print("\n----------------------------------------")
                print(f"No. Lotes Pendientes: {lotes_pendientes}\n")

                print("Lote Trabajando:")
                print("ID   TME")
                for p in lote_trabajando:
                    print(f"{p[3]}    {p[4]}")

                print("\nProceso en Ejecución:")
                print(f"Nombre: {userName}")
                print(f"Ope:    {ope_str}")
                print(f"ID:     {id_proc}")
                print(f"TME:    {tme}")
                print(f"TT:     {tt}")
                print(f"TR:     {tr}")

                print("\nTerminados:")
                print(f"{'ID':<6} {'Operación':<12} {'Resultado':<10} {'N.L.':<5}")
                print("-" * 38)
                for t in terminados:
                    print(f"{t[0]:<6} {t[1]:<12} {t[2]:<10} {t[3]:<5}")

                print(f"\nContador: {contador_global}")
                time.sleep(1)

            # Al finalizar el proceso actual se guarda en terminados
            terminados.append((id_proc, ope_str, res, num_lote))

    # resultados finales 
    limpiarPantalla ()
    print("\n----------------------------------------")
    print("Terminados:")
    print(f"{'ID':<6} {'Operación':<12} {'Resultado':<10} {'N.L.':<5}")
    for t in terminados:
        print(f"{t[0]:<6} {t[1]:<12} {t[2]:<10} {t[3]:<5}")
    print(f"\nContador Total: {contador_global} s")
    

if __name__ == "__main__":
    userName, colaProcesos = ingresoDatos()
    procesarDatos (userName, colaProcesos)
    print("Presiona Enter para finalizar el programa...")
    input()