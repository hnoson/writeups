// gcc -fno-stack-protector -o babyrop2 babyrop2.c
#include <stdio.h>
#include <unistd.h>

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    char name[0x10];
    printf("What's your name? ");
    int len = read(0, name, 0x100);
    name[len - 1] = '\0';
    printf("Welcome to the Pwn World again, %s!\n", name);
    return 0;
}
