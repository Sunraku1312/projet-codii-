#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define WIDTH 80
#define HEIGHT 24
#define DELAY 50000

void clear_screen() {
    printf("\033[2J\033[H");
}

void set_color_green() {
    printf("\033[32m");
}

void reset_color() {
    printf("\033[0m");
}

int main() {
    char screen[HEIGHT][WIDTH];
    int drops[WIDTH];
    srand(time(NULL));

    for (int i = 0; i < WIDTH; i++)
        drops[i] = rand() % HEIGHT;

    clear_screen();
    set_color_green();

    while (1) {
        for (int i = 0; i < HEIGHT; i++) {
            for (int j = 0; j < WIDTH; j++) {
                if (drops[j] == i)
                    putchar('0' + rand() % 2);  // '0' ou '1'
                else
                    putchar(' ');
            }
            putchar('\n');
        }
        for (int i = 0; i < WIDTH; i++) {
            if (rand() % 10 > 7)
                drops[i] = (drops[i] + 1) % HEIGHT;
        }
        usleep(DELAY);
        printf("\033[%dA", HEIGHT);  // remonter le curseur
    }

    reset_color();
    return 0;
}
