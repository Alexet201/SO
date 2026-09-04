#include <iostream>
#include "linux_conio.h"
#include <cctype>    
#include <chrono>    
#include <thread>    

bool activo = true;

void continuar() {
    std::cout << "Continuar\n";
    activo = true;
}

void error() { 
    std::cout << "Error\n"; 
}

void pausa() {
    std::cout << "Pausa\n";
    activo = false;
}

void interrupcion() { 
    std::cout << "Interrupcion I/O\n"; 
}

int main() {
#ifndef _WIN32
    setup_signal_interceptor();
    enable_conio_mode(); // Requerido por tu implementación para que _kbhit() funcione
#endif

    while (true) {
        if (_kbhit()) {
            char caracter = std::tolower(_getch());

            if (activo) {
                if (caracter == 'w') error();
                else if (caracter == 'p') pausa();
                else if (caracter == 'e') interrupcion();
                else if (caracter == 'c') continuar();
            } else if (caracter == 'c') {
                continuar();
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

#ifndef _WIN32
    disable_conio_mode();
#endif

    return 0;
}