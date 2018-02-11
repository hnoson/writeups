// gcc -fno-stack-protector -pie -fPIE -fomit-frame-pointer -o alnush alnush.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>
#include <sys/mman.h>

char *mystrdup(char *str) {
    char *ret = malloc(strlen(str) + 1);
    register char *src asm ("rdi");
    register char *dest asm ("rsi");
    for (src = str, dest = ret; *src; src++,dest++) {
        *dest = *src;
    }
    *dest = '\0';
    return ret;
}

void readline(char **str) {
    char buf[0x200];
    read(0,buf,0x280);
    register char *p = strchr(buf,'\n');
    if (p != NULL) {
        *p = '\0';
    }
    *str = mystrdup(buf);
}

void readcode(char **code) {
    printf("Enter shellcode >> ");
    readline(code);
}

void read_and_check_code(char **code) {
    readcode(code);
    printf("Checking shellcode...");
    sleep(1);
    int size = strlen(*code);
    for (int i = 0; i < size; i++) {
        if (!isalnum((*code)[i])) {
            puts("Invalid!");
            exit(1);
        }
    }
    puts("OK!");
}

void init() {
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);
}

int main() {
    char *code;
    init();
    read_and_check_code(&code);
    mprotect((void *)((unsigned long long)code & ~0xfff),0x2000,PROT_READ | PROT_EXEC);
    ((void (*)())(code))();
    return 0;
}
