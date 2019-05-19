#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int getnline(char *buf, size_t n) {
    for (int i = 0; i < n; i++) {
        if (read(0, &buf[i], 1) != 1) {
            exit(1);
        }
        if (buf[i] == '\n') {
            buf[i] = '\0';
            return i;
        }
    }

    return n;
}

int main(void) {
    char csets[0x50], format[0x55], password[0x50], buf[0x50];
    size_t n;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

start:
    puts("Create an account first.");
    printf("# of charsets: ");
    scanf("%lu", &n);
    getchar();
    if (n > 0x4f) {
        puts("Too big");
        goto start;
    }
    printf("charsets: ");
    getnline(csets, n);
    sprintf(format, "%%79[%s]", csets);
    printf("password: ");
    int result = scanf(format, password);
    getchar();
    if (result != 1) {
        puts("Invalid password");
        goto start;
    }

    puts("Account created. Please input password again to log in.");
    printf("password: ");
    getnline(buf, 0x4f);
    if (strcmp(password, buf) != 0) {
        puts("Incorrect");
        goto start;
    }
    puts("Successfully logged in.");
    puts("bye.");
    return 0;
}
