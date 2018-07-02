# SamsungCTF 2018 Writeup

## CowBoy [Attack 109pts]
The given program uses an original malloc implementation.
```c
struct node_t {
    char *addr;
    node_t *next;
};

int sizes[8];   // 0x6020c0 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 0x800
node_t **list;  // 0x6020e8
char *base;     // 0x6020f0
char **used;    // 0x6020f8

char *mymalloc(unsigned int size) {
    if (size > 0x800) return -1;
    int bini;
    for (int i = 0; i < 8; i++) {
        if (sizes[i] >= size) {
            bini = i;
            break;
        }
    }
    int chunki = -1;
    for (int i = 0; i < 0x1000 / sizes[bini]; i++) {
        if (!used[bini][i]) {
            used[bini][i] = 1;
            chunki = i;
            break;
        }
    }
    if (chunki == -1) return -1;
    char *addr = base + (bini << 0xc) + chunki * sizes[bini];
    node_t *node = malloc(0x10);
    node->addr = addr;
    node_t *now = list[bini];
    while (now) {
        now = now->next;
    }
    now->next = node;
    return addr;
}
```
There are 8 bins which contain chunks different in size and chunks are singly linked.
The important thing is that `node->next` isn't initialized.
Therefore, we can create a fake node by freeing a 0x10 chunk in advance which contains pointer to the fake node.
We can do that in "4. fill data".
```c
void fill() {
    int num, bini, chunki;
    printf("bin num? : ");
    scanf("%hu", &num);
    bini = num;
    getchar();
    printf("chunk num? : ");
    scanf("%hu", &num);
    chuni = num;
    getchar();
    node_t *now = list[bini]->next;
    while (chunk--) {
        now = now->next;
    }
    int size = sizes[bini];
    char *buf = malloc(size);
    memset(buf, 0, size);
    printf("input: ");
    int len = read(0, buf, size);
    memcpy(now->addr, buf, len);
    free(buf);
}
```
It allocates buffer of the same size of the chunk, and frees it at the end.
So, we can create a fake node by allocating a 0x10 chunk and modifying it.
By using this bug, arbitrary address can be leaked and overwriten.
I used one-gadget RCE to execute `/bin/sh`.
The exploit code is [here](https://github.com/hnoson/writeups/blob/master/sctf/2018/cowboy/exploit.py).

## BankRobber [Defense 103pts]
There are 4 bugs.

1. In donate function, if value is larger than balance, balance will overflow and increase.

```solidity
function donate(uint256 value) public {
    require(balance[msg.sender] >= value); // add
    balance[msg.sender] -= value;
    donation_deposit += value;
}
```

2. Also, in multiTransfer function, there is an integer overflow.

```solidity
function multiTransfer(address[] to_list, uint256 value) public {
    require(balance[msg.sender] >= value*to_list.length);
    require(value*to_list.length >= value); // add
    balance[msg.sender] -= value*to_list.length;
    for(uint i=0; i < to_list.length; i++){
        balance[to_list[i]] += value;
    }
}
```

3. Sending ethers must be done after decreasing balance, otherwise attackers would quit the execution before decreasing balance.

```solidity
function withdraw(uint256 value) public{
    require(balance[msg.sender] >= value);
    balance[msg.sender] -= value;    // swap
    msg.sender.call.value(value)();  // swap
}
```

4. `tx.origin` gives the origin of the chain. On the other hand, `msg.sender` gives the direct sender of the message.

```solidity
    function deliver(address to) public {
        // require(tx.origin == owner); // remove
        require(msg.sender == owner);   // add
        to.transfer(donation_deposit);
        donation_deposit = 0;
    }
```

## dingJMax [Reversing 106pts]
First of all, we need to extract the patterns. They are at `0x603280` according to `0x401675`. 
```
gdb-peda$ x/10gx 0x603280 + 0x120
0x6033a0:       0x0000000000402284      0x0000000000402275
0x6033b0:       0x0000000000402275      0x0000000000402275
0x6033c0:       0x0000000000402275      0x0000000000402275
0x6033d0:       0x0000000000402275      0x0000000000402275
0x6033e0:       0x000000000040227f      0x0000000000402275
gdb-peda$ x/s 0x402284
0x402284:       "o   "
gdb-peda$ x/s 0x402275
0x402275:       "    "
gdb-peda$ x/s 0x40227f
0x40227f:       " o  "
```
All patterns are [here](https://github.com/hnoson/writeups/blob/master/sctf/2018/dingjmax/pattern).

Next, the flag is modified when you hit a key. We can see the algorithm at `0x40145d`. Firstly, global variables are mixed.
Then, the flag letters are modified one by one by using the global variables.
The algorithm is a little complicated to describe it in languages,
so please look at [my solution](https://github.com/hnoson/writeups/blob/master/sctf/2018/dingjmax/solve.py).

Now, we know the patterns and the algorithm of shuffling flag. Therefore, we can get the flag by simulating the program.

## Catch the bug [Attack 192pts]
I solved this challenge after the contest finished.

There are 4 options.

0. Exit  
Return from the main function.

1. Catch a bug  
It randomly chooses a bug and puts it into a bag (up to 3 bugs). We can name the bug (up to 3 bytes).

2. Inspect the bug  
It outputs the ascii art of the bug and the name we named before.
And, there is a fsb which can be used only for leaking libc address.

3. Submit a report  
Write a report to buffer whose size is 0x700. It sometimes overflows if you add 3 bugs in the bag.
Look at the following code.
```c
char report[0x700]; // 0x2030a0
char password[8]; // 0x2037a0
char *report_addr; // 0x2037a8
char *password_addr; // 0x2037b0

void submit() {
    puts("Submit a report about your work");
    puts("Report title");
    report_addr += readn(report_addr, 0x40);
    puts("Report subtitle");
    report_addr += readn(report_addr, 0x80);
    for (int i = 0; i < num; i++) {
        *(long *)report_addr = *(long *)(bugs[num]->name);
        report_addr += 8;
        strcpy(report_addr, bug_ascii[bugs[num]->type]);
        report_addr += strlen(bug_ascii[bugs[num]->type]);
    }
    puts("Report body");
    report_addr += readn(report_addr, 0x100); // buffer overflow
    puts("Report tag");
    report_addr += readn(report_addr, 0x8);
    puts("Report password");
    readn(password_addr, 0x8);
}
```
It overflows when writing body and we can overwrite `report_addr` and `password_addr`.
So, we have two chances to overwrite buffer at arbitrary address.
But, we have only libc address and PIE is enabled, on top of that, the program finishes after "3. Submit a report".

Let's look at the code after returning from the main function.  
It calls `__GI_exit`.
```
=> 0x7fc3e54081c1 <__libc_start_main+241>:      mov    edi,eax
   0x7fc3e54081c3 <__libc_start_main+243>:      call   0x7fc3e5422f00 <__GI_exit>
```
In `__GI_exit`, `__run_exit_handlers` is called.
```
   0x7fc3e5422f07 <__GI_exit+7>:        sub    rsp,0x8
   0x7fc3e5422f0b <__GI_exit+11>:       mov    ecx,0x1
   0x7fc3e5422f10 <__GI_exit+16>:       mov    edx,0x1
=> 0x7fc3e5422f15 <__GI_exit+21>:       call   0x7fc3e5422dd0 <__run_exit_handlers>
```
After that, it calls `_dl_fini`.
```
RCX: 0x7fc3e57c2d50 --> 0x4
RDX: 0x7fc3e57d7ee0 (<_dl_fini>:        push   rbp)
RSI: 0x0
RDI: 0x0
RBP: 0x7fc3e57c16f8 --> 0x7fc3e57c2d40 --> 0x0
RSP: 0x7fffba81f3d0 --> 0x7fffba81f4e0 --> 0x1
RIP: 0x7fc3e5422ebe (<__run_exit_handlers+238>: call   rdx)
R8 : 0x7fc3e57c2520 --> 0x7fc3e57be6c0 --> 0x7fc3e558ca16 --> 0x636d656d5f5f0043 ('C')
R9 : 0x3
R10: 0x1f
R11: 0x246
R12: 0x1
R13: 0x7fc3e57c2d40 --> 0x0
R14: 0x0
R15: 0x0
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x7fc3e5422ead <__run_exit_handlers+221>:    mov    rdi,QWORD PTR [rax+0x20]
   0x7fc3e5422eb1 <__run_exit_handlers+225>:    ror    rdx,0x11
   0x7fc3e5422eb5 <__run_exit_handlers+229>:    xor    rdx,QWORD PTR fs:0x30
=> 0x7fc3e5422ebe <__run_exit_handlers+238>:    call   rdx
   0x7fc3e5422ec0 <__run_exit_handlers+240>:    jmp    0x7fc3e5422df8 <__run_exit_handlers+40>
```
In `_dl_fini`, there is a function call and the address is stored in memory which we can overwrite.
```
=> 0x7fc3e57d7f56 <_dl_fini+118>:
    call   QWORD PTR [rip+0x217fe4]        # 0x7fc3e59eff40 <_rtld_global+3840>
```
```
gdb-peda$ vmmap
...
0x00007fc3e53e7000 0x00007fc3e55bd000 r-xp      /lib/x86_64-linux-gnu/libc-2.26.so
0x00007fc3e55bd000 0x00007fc3e57bd000 ---p      /lib/x86_64-linux-gnu/libc-2.26.so
0x00007fc3e57bd000 0x00007fc3e57c1000 r--p      /lib/x86_64-linux-gnu/libc-2.26.so
0x00007fc3e57c1000 0x00007fc3e57c3000 rw-p      /lib/x86_64-linux-gnu/libc-2.26.so
0x00007fc3e57c3000 0x00007fc3e57c7000 rw-p      mapped
0x00007fc3e57c7000 0x00007fc3e57ee000 r-xp      /lib/x86_64-linux-gnu/ld-2.26.so
0x00007fc3e59d8000 0x00007fc3e59da000 rw-p      mapped
0x00007fc3e59ee000 0x00007fc3e59ef000 r--p      /lib/x86_64-linux-gnu/ld-2.26.so
0x00007fc3e59ef000 0x00007fc3e59f0000 rw-p      /lib/x86_64-linux-gnu/ld-2.26.so
```
Since the distance between ld-2.26.so and libc-2.26.so is always the same, we can get the address from libc address.
By overwriting the address with one-gadget RCE, we can execute `/bin/sh`.
The exploit code is [here](https://github.com/hnoson/writeups/blob/master/sctf/2018/catchthebug/exploit.py)
