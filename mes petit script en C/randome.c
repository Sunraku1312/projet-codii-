int seed = 123456789;

int rand_custom() {
    seed = (1103515245 * seed + 12345) & 0x7FFFFFFF;
    return seed;
}

int rand_range(int min, int max) {
    return min + (rand_custom() % (max - min + 1));
}

void print_number(int n) {
    if (n == 0) {
        putchar('0');
        return;
    }
    if (n < 0) {
        putchar('-');
        n = -n;
    }
    char buf[10];
    int i = 0;
    while (n > 0) {
        buf[i++] = '0' + (n % 10);
        n /= 10;
    }
    while (i--) putchar(buf[i]);
}

int main() {
    int r = rand_range(1, 100);
    print_number(r);
    putchar('\n');
    return 0;
}
