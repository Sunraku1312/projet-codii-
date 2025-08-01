#include <SFML/Graphics.hpp>
#include <time.h>

int fieldWidth = 10;
int fieldHeight = 20;
int blockSize = 30;

int field[20][10] = {0};

struct Point { int x, y; } a[4], b[4];

int figures[7][4] = {
    1,3,5,7, // I
    2,4,5,7, // Z
    3,5,4,6, // S
    3,5,4,7, // T
    2,3,5,7, // L
    3,5,7,6, // J
    2,3,4,5, // O
};

bool check() {
    for (int i=0; i<4; i++) {
        if (a[i].x<0 || a[i].x>=fieldWidth || a[i].y>=fieldHeight) return false;
        else if (field[a[i].y][a[i].x]) return false;
    }
    return true;
}

int main() {
    srand(time(0));

    sf::RenderWindow window(sf::VideoMode(fieldWidth*blockSize, fieldHeight*blockSize), "Tetris SFML");

    sf::Texture t;
    t.loadFromFile("tiles.png"); // une image 4x4 blocs 30x30px (à fournir)
    sf::Sprite sprite(t);

    int colorNum = 1;

    for (int i=0; i<4; i++) {
        a[i].x = figures[colorNum-1][i] % 2;
        a[i].y = figures[colorNum-1][i] / 2;
    }

    sf::Clock clock;
    float timer = 0, delay = 0.3;

    bool rotate = false;

    while (window.isOpen()) {
        float time = clock.restart().asSeconds();
        timer += time;

        sf::Event e;
        while (window.pollEvent(e)) {
            if (e.type == sf::Event::Closed)
                window.close();

            if (e.type == sf::Event::KeyPressed) {
                if (e.key.code == sf::Keyboard::Up) rotate = true;
                else if (e.key.code == sf::Keyboard::Left) {
                    for (int i=0; i<4; i++) { b[i] = a[i]; a[i].x--; }
                    if (!check()) for (int i=0; i<4; i++) a[i] = b[i];
                }
                else if (e.key.code == sf::Keyboard::Right) {
                    for (int i=0; i<4; i++) { b[i] = a[i]; a[i].x++; }
                    if (!check()) for (int i=0; i<4; i++) a[i] = b[i];
                }
                else if (e.key.code == sf::Keyboard::Down) delay = 0.05;
            }
        }

        if (rotate) {
            Point p = a[1];
            for (int i=0; i<4; i++) {
                int x = a[i].y - p.y;
                int y = a[i].x - p.x;
                a[i].x = p.x - x;
                a[i].y = p.y + y;
            }
            if (!check()) for (int i=0; i<4; i++) a[i] = b[i];
            rotate = false;
        }

        if (timer > delay) {
            for (int i=0; i<4; i++) { b[i] = a[i]; a[i].y++; }
            if (!check()) {
                for (int i=0; i<4; i++) field[b[i].y][b[i].x] = colorNum;
                colorNum = 1 + rand() % 7;
                for (int i=0; i<4; i++) {
                    a[i].x = figures[colorNum-1][i] % 2;
                    a[i].y = figures[colorNum-1][i] / 2;
                }
            }
            timer = 0;
            delay = 0.3;
        }

        int k = fieldHeight -1;
        for (int i=fieldHeight-1; i>0; i--) {
            int count = 0;
            for (int j=0; j<fieldWidth; j++) {
                if (field[i][j]) count++;
                field[k][j] = field[i][j];
            }
            if (count < fieldWidth) k--;
        }

        window.clear(sf::Color::Black);

        for (int i=0; i<fieldHeight; i++)
            for (int j=0; j<fieldWidth; j++) {
                if (field[i][j] == 0) continue;
                sprite.setTextureRect(sf::IntRect(field[i][j]*blockSize, 0, blockSize, blockSize));
                sprite.setPosition(j*blockSize, i*blockSize);
                window.draw(sprite);
            }

        for (int i=0; i<4; i++) {
            sprite.setTextureRect(sf::IntRect(colorNum*blockSize, 0, blockSize, blockSize));
            sprite.setPosition(a[i].x*blockSize, a[i].y*blockSize);
            window.draw(sprite);
        }

        window.display();
    }
    return 0;
}
