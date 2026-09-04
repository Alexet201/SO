#include <iostream>
#include "linux_conio.h"   // Libreria para manejo de conio en Linux
#include <cctype>         //  Para std::tolower
#include <chrono>        // Para std::chrono
#include <thread>       // Para std::this_thread::sleep_for (evitar saturar la CPU)

class KBHit {
    private:
        bool activo;
    public:

        KBHit() : activo(true) {}
        bool isActivo() const { return activo; }
        void continuar() {
            std::cout << "Continuar" << std::endl;
            activo = true;
        }

        void error() { 
            std::cout << "Error" << std::endl; 
        }

        void pausa() {
            std::cout << "Pausa" << std::endl;
            activo = false;
        }

        void interrupcion() { 
            std::cout << "Interrupcion I/O" << std::endl; 
        }
};


int main() {
    KBHit kbhit;
    std::cout << "Presione 'w' para error" << std::endl;
    std::cout << "Presione 'p' para pausa" << std::endl;
    std::cout << "Presione 'e' para interrupcion "<< std::endl;
    std::cout << "Presione 'c' para continuar." << std::endl;
    
    while (true) {
        if (_kbhit()) {
            char caracter = std::tolower(_getch());

            if (kbhit.isActivo()) {
                switch (caracter) {
                    case 'w':   kbhit.error();        break;
                    case 'p':   kbhit.pausa();        break;
                    case 'e':   kbhit.interrupcion(); break;
                    case 'c':   kbhit.continuar();    break;
                    default:    break;       
                }
            } else if (caracter == 'c') {
                kbhit.continuar();
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    return 0;
}