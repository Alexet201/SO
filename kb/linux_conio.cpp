#include "linux_conio.h"

#ifndef _WIN32

static struct termios old_attributes;
static bool conio_mode = false;

void enable_conio_mode() {
    if (conio_mode) return;
    
    // Obtener la configuración actual de la terminal
    tcgetattr(STDIN_FILENO, &old_attributes);
    
    struct termios new_attributes = old_attributes;
    // Desactivar modo canónico (ICANON) y el eco en pantalla (ECHO)
    new_attributes.c_lflag &= ~(ICANON | ECHO);
    // Configurar tiempo de espera en 0 para lectura no bloqueante de read()
    new_attributes.c_cc[VMIN] = 0;
    new_attributes.c_cc[VTIME] = 0;
    
    tcsetattr(STDIN_FILENO, TCSANOW, &new_attributes);
    conio_mode = true;
}

void disable_conio_mode() {
    if (!conio_mode) return;
    tcsetattr(STDIN_FILENO, TCSANOW, &old_attributes);
    conio_mode = false;
}

void setup_signal_interceptor() {
    // Implementación vacía básica para compatibilidad
}

int _getch() {
    char c = 0;
    // En modo no bloqueante, read lee de inmediato si hay algo en STDIN
    if (read(STDIN_FILENO, &c, 1) > 0) {
        return c;
    }
    return 0;
}

bool _kbhit() {
    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(STDIN_FILENO, &readfds);

    timeval timeout;
    timeout.tv_sec = 0;
    timeout.tv_usec = 0; // Respuesta instantánea (no bloqueante)

    return select(STDIN_FILENO + 1, &readfds, nullptr, nullptr, &timeout) > 0;
}

int getch_noblock() {
    return _getch();
}

#else
void setup_signal_interceptor() {}
void disable_conio_mode() {}
void enable_conio_mode() {}

int getch_noblock() {
    if (_kbhit()) return _getch();
    return EOF;
}
#endif