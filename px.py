import sys
import select
import termios
import tty
import time

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
        print ("Pausa")
        self._activo = False

    def interrupcion(self):
        print ("Interrupcion I/O")

# Ejemplo de uso con Gestor de Contexto ('with'):

with KBHit() as kb:
    while True:
        if kb.kbhit():
            caracter = kb.getch()
            if kb.isActivo():

                if caracter.lower() == 'w':
                    kb.error()
                elif caracter.lower() == 'p':
                    kb.pausa()
                elif caracter.lower() == 'e':
                    kb.interrupcion()
                elif caracter.lower() == 'c':
                    kb.continuar()
                
            elif caracter.lower() == 'c':
                kb.continuar()

        time.sleep(0.05)