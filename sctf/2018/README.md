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
