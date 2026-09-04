#pragma once
#include <string>

#ifdef _WIN32
#include <conio.h>
#else
#include <termios.h>
#include <unistd.h>
#include <stdio.h>
#include <cstdlib>
#include <signal.h>
#include <fcntl.h>
#endif

// Configura el interceptor de señales para restaurar la terminal al salir
void setup_signal_interceptor();

// Desactiva el modo conio en Linux
void disable_conio_mode();

// Activa el modo conio en Linux
void enable_conio_mode();

// Versión no bloqueante de getch (Windows y Linux)
int getch_noblock();

#ifndef _WIN32
// Implementación de _getch en Linux
int _getch();

// Implementación de _kbhit en Linux
bool _kbhit();
#endif