// gcc -fno-stack-protector -o babyrop babyrop.c
#include <stdio.h>
#include <stdlib.h>

char binsh[] = "/bin/sh";

int main(void) {
    char name[0x10];
    system("echo -n \"What's your name? \"");
    scanf("%s", name);
    printf("Welcome to the Pwn World, %s!\n", name);
    return 0;
}
