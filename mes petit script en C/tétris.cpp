#include <SFML/Graphics.hpp>
#include <time.h>
using namespace sf;

int field[20][10] = {0};

int figures[7][4] = {
    1,3,5,7,
    2,4,5,7,
    3,5,4,6,
    3,5,4,7,
    2,3,5,7,
    3,5,7,6,
    2,3,4,5
};

struct Point { int x, y; } a[4], b[4];

bool check() {
    for (int i = 0; i < 4; i++) {
        if (a[i].x < 0 || a[i].x >= 10 || a[i].y >= 20) return false;
        if (field[a[i].y][a[i].x]) return false;
    }
    return true;
}

Color getColor(int num) {
    Color colors[] = {
        Color::Black,
        Color::Cyan,
        Color::Yellow,
        Color::Magenta,
        Color::Green,
        Color::Red,
        Color::Blue,
        Color(255,165,0)
    };
    return colors[num % 8];
}

int main() {
    srand(time(0));
    const int blockSize = 24;
    RenderWindow window(VideoMode(10 * blockSize + 200, 20 * blockSize), "Tetris");

    RectangleShape block(Vector2f(blockSize - 1, blockSize - 1));
    int dx = 0; bool rotate = 0; int colorNum = 1;
    float timer = 0, delay = 0.5;
    Clock clock;

    int n = rand() % 7;
    for (int i = 0; i < 4; i++) {
        a[i].x = figures[n][i] % 2;
        a[i].y = figures[n][i] / 2;
    }

    while (window.isOpen()) {
        float time = clock.getElapsedTime().asSeconds();
        clock.restart();
        timer += time;

        Event e;
        while (window.pollEvent(e))
            if (e.type == Event::Closed) window.close();

        if (Keyboard::isKeyPressed(Keyboard::Left)) dx = -1;
        else if (Keyboard::isKeyPressed(Keyboard::Right)) dx = 1;
        else dx = 0;

        if (Keyboard::isKeyPressed(Keyboard::Up)) rotate = true;
        if (Keyboard::isKeyPressed(Keyboard::Down)) delay = 0.05;

        for (int i = 0; i < 4; i++) { b[i] = a[i]; a[i].x += dx; }
        if (!check()) for (int i = 0; i < 4; i++) a[i] = b[i];

        if (rotate) {
            Point p = a[1];
            for (int i = 0; i < 4; i++) {
                int x = a[i].y - p.y;
                int y = a[i].x - p.x;
                a[i].x = p.x - x;
                a[i].y = p.y + y;
            }
            if (!check()) for (int i = 0; i < 4; i++) a[i] = b[i];
        }

        if (timer > delay) {
            for (int i = 0; i < 4; i++) { b[i] = a[i]; a[i].y += 1; }
            if (!check()) {
                for (int i = 0; i < 4; i++) field[b[i].y][b[i].x] = colorNum;
                colorNum = 1 + rand() % 7;
                n = rand() % 7;
                for (int i = 0; i < 4; i++) {
                    a[i].x = figures[n][i] % 2;
                    a[i].y = figures[n][i] / 2;
                }
            }
            timer = 0;
        }

        int k = 19;
        for (int i = 19; i >= 0; i--) {
            int count = 0;
            for (int j = 0; j < 10; j++) {
                if (field[i][j]) count++;
                field[k][j] = field[i][j];
            }
            if (count < 10) k--;
        }

        window.clear(Color::Black);

        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 10; j++) {
                if (field[i][j] == 0) continue;
                block.setFillColor(getColor(field[i][j]));
                block.setPosition(j * blockSize, i * blockSize);
                window.draw(block);
            }

        for (int i = 0; i < 4; i++) {
            block.setFillColor(getColor(colorNum));
            block.setPosition(a[i].x * blockSize, a[i].y * blockSize);
            window.draw(block);
        }

        window.display();
        rotate = 0; delay = 0.5;
    }

    return 0;
}
