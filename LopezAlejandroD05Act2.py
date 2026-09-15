from collections import deque
from mimetypes import init
import time
import os
import sys
import select
import termios
import tty
import random

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

class KBHit:
    def __init__(self):
        self._activo = True
    def __enter__(self):
        # Obtiene el identificador del archivo de entrada estándar (teclado)
        self.fd = sys.stdin.fileno()
        # Guarda la configuración actual de la terminal
        self.old_settings = termios.tcgetattr(self.fd)
        # Cambia la terminal a modo 'cbreak' (lee teclas al instante sin esperar Enter)
        tty.setcbreak(self.fd)
        return self

    def __exit__(self, tipo, valor, traza):
        # Restaura la configuración original de la terminal al salir del 'with'
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def kbhit(self):
        # Comprueba si hay datos en la entrada estándar sin bloquear la ejecución
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return dr != []

    def isActivo (self):
        return self._activo
    
    def getch(self):
        # Lee un solo carácter de la entrada
        return sys.stdin.read(1)
    def continuar(self):
        print ("Continuar")
        self._activo = True
    def error(self):
        print ("Error")
        
    def pausa(self):
        print ("Sistema pausado presione C para continuar")
        self._activo = False

    def interrupcion(self):
        print ("Interrupcion I/O")

#La clase Proceso sirve para definir la estructura del proceso
class Proceso: 
    def __init__(self, id, numeroLote, operacion, priV, segV, tme):
        self.operacion = operacion
        self.priV = priV
        self.segV = segV
        self.id = id
        self.tme = tme
        self.numero_lote = numeroLote
        self.tiempo_restante = tme

#Esta clase se compone por procesos
class Lote: 
    def __init__(self, numeroLote):
        self.numeroLote = numeroLote
        self.procesos = deque()

    def agregarProceso(self, proceso):
        self.procesos.append(proceso)

    def isEmpty(self):
        return len(self.procesos) == 0

    def isFull(self):
        return len(self.procesos) >= 5

#Estructura del procesos para impirmir en terminados 
class ProcesoTerminado:
    def __init__(self, id, operacion, resultado, num_lote):
        self.id = id
        self.operacion = operacion
        self.resultado = resultado
        self.num_lote = num_lote

#Sirve para definir las operaciones posibles y resolverlas 
class Operacion: 
    MAX_OPERACION = 5

    def ejecutar (self, operacion, primerV, segundoV):
        if operacion == 1:
            return f"{primerV} + {segundoV}", primerV + segundoV
        elif operacion == 2:
            return f"{primerV} - {segundoV}", primerV - segundoV
        elif operacion == 3:
            return f"{primerV} * {segundoV}", primerV * segundoV
        elif operacion == 4:
            return f"{primerV} / {segundoV}", primerV / segundoV
        elif operacion == 5:
            return f"{primerV} % {segundoV}", primerV % segundoV
        return "", 0
    def isValid (self, operacion, segundoV):
        if (operacion == 4 or operacion == 5) and segundoV == 0: 
            return False, "Error: Con división y residuo el segundo numero no puede ser 0."
        return True, ""
    
    def menu (self, i): 
            print(f"\nProceso {i + 1}:")
            print("Ingresa el número de las operaciones del proceso y sus valores")
            print("1.- Suma")
            print("2.- Resta")
            print("3.- Multiplicación")
            print("4.- División")
            print("5.- Residuo\n")

#Este sirve para generar datos randons para los procesos
class GenerarDatos:

    def __init__(self):
        self.id = 0

    def getId(self): 
        self.id += 1
        return self.id 

    @staticmethod
    def getNumerosPruba ():
        return random.randint(1, 100)

    @staticmethod
    def getTiempo():
        return random.randint(5, 20)

    @staticmethod
    def getOperacion():
        return random.randint(1, 5)
    
#Clase para validar que los inputs sean dentro de los lindeaminetos
class PedirDatos:
    def pedirEntero (self, mensaje, minimo=None, maximo=None):
        while True:
            try:
                valor = int(input(mensaje))
                if minimo is not None and valor < minimo:
                    print(f"Error: El valor debe ser mayor o igual a {minimo}.")
                    continue
                if maximo is not None and valor > maximo:
                    print(f"Error: El valor debe ser menor o igual a {maximo}.")
                    continue
                return valor
            except ValueError:
                print("Error: Debes ingresar un número entero.")

    def pedirFlotante (self, mensaje):
        while True:
            try:
                valor = float(input(mensaje))
                return valor
            except ValueError:
                print("Error: Debes ingresar un número.")

    def pedirCadena (self, mensaje):
        while True:
            valor = input(mensaje).strip()
            if valor:
                return valor
            print("Error: La cadena no puede estar vacía.")

    def isValidId (self, ids):
        while True:
            input_id = input("Ingresa el id de la operacion: ")
            if input_id.strip() == "":
                print("Error: El id no puede estar vacío.")
                continue
            if input_id in ids: 
                print("Error: Este id ya fue usado, ingresa otro.")
                continue
            return input_id

#Captura de los lotes 
class CapturarProcesos: 
    
    def recolectarValores (): 
        colaLotes = deque()
        ids_usados = set ()
        generador = GenerarDatos()
        total_procesos = PedirDatos().pedirEntero("¿Cuántos procesos quieres ejecutar?: ", minimo=1)
        lote_actual = None

        for i in range(total_procesos):

            numeroLote = (i // 5) + 1
            if i % 5 == 0:
                lote_actual = Lote(numeroLote)
                colaLotes.append(lote_actual)

            limpiarPantalla()
            
            while True: 
                operacion = GenerarDatos().getOperacion()
                primerV   = GenerarDatos().getNumerosPruba()
                segundoV  = GenerarDatos().getNumerosPruba()
                tme       = GenerarDatos().getTiempo()

                # Validar operación y segundo valor
                es_valido, mensaje_error = Operacion().isValid(operacion, segundoV)
                if not es_valido:
                    print(mensaje_error)
                    continue

                id = generador.getId()
                ids_usados.add(id)

                proceso = Proceso(id, numeroLote, operacion, primerV, segundoV, tme)
                lote_actual.agregarProceso(proceso)
                break

        return colaLotes

#Procesamiento de los lotes, despues de la captura
class ProcesardorLotes:
    def __init__(self, colaLotes):
        self.colaLotes = colaLotes
        self.contadorGlobal = 0
        self.terminados = []

    def procesarTeclado (self, kb):
        if not kb.kbhit():
            return None

        caracter = kb.getch().lower()
        if kb.isActivo():
            if caracter == 'w':
                kb.error()
                return 'ERROR'
            elif caracter == 'p':
                kb.pausa()
                return 'PAUSA'
            elif caracter == 'e':
                kb.interrupcion()
                return 'INTERRUPCION'
        elif caracter == 'c':
            kb.continuar()
            return 'CONTINUAR'

        return None 

    def esperarUnSegundo(self, kb):
        
        paso = 0.05
        tiempo_acumulado = 0.0

        while tiempo_acumulado < 1.0:
            accion = self.procesarTeclado(kb)

            # Si el sistema está pausado, se detiene hasta presionar 'c'
            while not kb.isActivo():
                time.sleep(paso)
                self.procesarTeclado(kb)

            # Manejo de acciones inmediatas
            if accion in ('ERROR', 'INTERRUPCION'):
                return accion

            time.sleep(paso)
            tiempo_acumulado += paso

        return 'OK'

    def imprimirPantalla(self, loteActual, procesosLote, proc, opeStr, tt):
        lotesPendientes = len(self.colaLotes)

        limpiarPantalla()
        print("\n----------------------------------------")
        print(f"No. Lotes Pendientes: {lotesPendientes}\n")

        print(f"Lote Trabajando (Lote #{loteActual.numeroLote}):")
        print("ID   TME")
        for p in procesosLote:
            print(f"{p.id:<4} {p.tme:<5}")

        print("\nProceso en Ejecución:")
        print(f"Ope:    {opeStr}")
        print(f"ID:     {proc.id}")
        print(f"TME:    {proc.tme}")
        print(f"TT:     {tt}")
        print(f"TR:     {proc.tiempo_restante}")

        print("\nTerminados:")
        print(f"{'ID':<6} {'Operación':<12} {'Resultado':<10} {'N.L.':<5}")
        print("-" * 45)
        for t in self.terminados:
            res_str = f"{t.resultado:.2f}" if isinstance(t.resultado, (float, int)) else str(t.resultado)

            print(f"{t.id:<6} {t.operacion:<12} {res_str:<10} {t.num_lote:<5}")

        print(f"\nContador Global: {self.contadorGlobal} s")
    
    def ejecutar(self):
        operador = Operacion()

        with KBHit() as kb: 
            while self.colaLotes:
                loteActual = self.colaLotes.popleft()
                procesosLote = loteActual.procesos
                while procesosLote:
                    proc = procesosLote.popleft()
                    opeStr, res = operador.ejecutar(proc.operacion, proc.priV, proc.segV)

                    is_interrupcion = False
                    while proc.tiempo_restante > 0:
                        tt = proc.tme - proc.tiempo_restante
                                            
                        self.imprimirPantalla(loteActual, procesosLote, proc, opeStr, tt)

                        estado = self.esperarUnSegundo(kb)

                        if estado == 'ERROR':
                            res = 'ERROR'
                            break
                        elif estado == 'INTERRUPCION':
                            is_interrupcion = True
                            break

                        self.contadorGlobal  += 1
                        proc.tiempo_restante -= 1
                    if is_interrupcion:
                        loteActual.agregarProceso(proc)
                        continue

                    proc_terminado = ProcesoTerminado(proc.id, opeStr, res, proc.numero_lote)
                    self.terminados.append(proc_terminado)

        # Impresión final
        limpiarPantalla()
        print("\n")
        print("-" * 45)
        print("Procesos Terminados:")
        print(f"{'ID':<6} {'Operación':<12} {'Resultado':<10} {'N.L.':<5}")
        print("-" * 45)
        for t in self.terminados:
            res_str = f"{t.resultado:.2f}" if isinstance(t.resultado, (float, int)) else str(t.resultado)
            print(f"{t.id:<6} {t.operacion:<12} {res_str:<10} {t.num_lote:<5}")
            
        print(f"\nContador Total: {self.contadorGlobal} s")


if __name__ == "__main__":
    colaLotes = CapturarProcesos.recolectarValores()
    app = ProcesardorLotes(colaLotes)
    app.ejecutar()

    print("\nPresiona Enter para finalizar el programa...")
    input()
  