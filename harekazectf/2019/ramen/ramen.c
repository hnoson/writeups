#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

#define DEFAULT_SIZE 0x08
#define MIN_SIZE 0x02
#define MAX_SIZE 0x20
#define FLAVORS 5
#define FLAVOR_MAX_LEN 0x10
#define TOPPINGS_LEN 0x20
#define LENGTH(q) (((q)->size + (q)->tail - (q)->head) % (q)->size)

void timeout() {
    puts("time out!");
    exit(-1);
}

void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);
}

void getnline(char *buf, int size) {
    int len = read(0, buf, size - 1);
    if (buf[len - 1] == '\n') {
        buf[len - 1] = '\0';
    }
    buf[len] = '\0';
}

int getint() {
    char buf[0x20];
    getnline(buf, 0x20);
    return atoi(buf);
}

int menu() {
    puts("1. Order Ramen");
    puts("2. Serve Ramen");
    puts("3. Increase the number of seats");
    printf("Choice: ");
    return getint();
}

int next_power_of_two(int n) {
    int ret = 1;
    while (ret < n) {
        ret <<= 1;
    }
    return ret;
}

char flavors[FLAVORS][FLAVOR_MAX_LEN] = {
    "Soy Sauce",
    "Salt",
    "Miso",
    "Chicken",
    "Tonkotu"
};

int ramen_menu() {
    for (int i = 0; i < FLAVORS; i++) {
        printf("%d. %s Ramen\n", i + 1, flavors[i]);
    }
    printf("Choice: ");
    return getint();
}

typedef struct {
    long long eggs;
    long long porks;
    long long bamboo_shoots;
    char name[FLAVOR_MAX_LEN];
    char *others;
} Ramen;

typedef struct {
    Ramen *buf;
    int head;
    int tail;
    int size;
} Orders;

void init_orders(Orders *orders) {
    orders->buf = calloc(DEFAULT_SIZE, sizeof(Ramen));
    orders->head = 0;
    orders->tail = 0;
    orders->size = DEFAULT_SIZE;
}

void shrink_buf(Orders *orders, int new_size) {
    int head = orders->head;
    int tail = orders->tail;
    int size = orders->size;

    if (tail < head) {
        int n = size - new_size;
        for (int i = head; i < size; i++) {
            orders->buf[i - n] = orders->buf[i];
        }
        orders->head -= n;
    } else if (head >= new_size) {
        for (int i = head; i < tail; i++) {
            orders->buf[i - head] = orders->buf[i];
        }
        orders->tail -= orders->head;
        orders->head = 0;
    } else if (tail >= new_size) {
        for (int i = new_size; i < tail; i++) {
            orders->buf[i - new_size] = orders->buf[i];
        }
        orders->tail -= new_size;
    }

    orders->buf = realloc(orders->buf, sizeof(Ramen) * new_size);
    orders->size = new_size;
}

void expand_buf(Orders *orders, int new_size) {
    int head = orders->head;
    int tail = orders->tail;
    int size = orders->size;

    orders->buf = realloc(orders->buf, sizeof(Ramen) * new_size);
    orders->size = new_size;

    if (head <= tail) {
        // Nop
    } else if (tail < size - head) {
        for (int i = 0; i < tail; i++) {
            orders->buf[i + size] = orders->buf[i];
        }
        orders->tail += size;
    }
    else {
        int n = new_size - size;
        for (int i = head; i < size; i++) {
            orders->buf[i + n] = orders->buf[i];
        }
        orders->head += n;
    }
}

void order_ramen(Orders *orders) {
    if (LENGTH(orders) == orders->size - 1) {
        puts("Seats are full.");
        return;
    }

    int choice = ramen_menu();
    if (choice < 1 || choice > FLAVORS) {
        puts("Invalid choice.");
        return;
    }

    Ramen ramen;
    memset(ramen.name, 0, FLAVOR_MAX_LEN);
    strcpy(ramen.name, flavors[choice - 1]);
    printf("How many eggs? ");
    ramen.eggs = getint();
    printf("How many grilled pork? ");
    ramen.porks = getint();
    printf("How many bamboo shoots? ");
    ramen.bamboo_shoots = getint();
    printf("If you want other toppings, put them down: ");
    ramen.others = malloc(TOPPINGS_LEN);
    memset(ramen.others, 0, TOPPINGS_LEN);
    getnline(ramen.others, TOPPINGS_LEN);
    orders->buf[orders->tail] = ramen;
    orders->tail = (orders->tail + 1) % orders->size;

    puts("Done.");
}

void serve_ramen(Orders *orders) {
    if (orders->head == orders->tail) {
        puts("No order remains.");
        return;
    }

    Ramen *ramen = &orders->buf[orders->head];
    orders->head = (orders->head + 1) % orders->size;
    printf("Serving %s Ramen...\n", ramen->name);
    printf("Eggs: %d\n", (int)ramen->eggs);
    printf("Grilled pork: %d\n", (int)ramen->porks);
    printf("Bamboo shoots: %d\n", (int)ramen->bamboo_shoots);
    printf("Other toppings: %s\n", ramen->others);
    free(ramen->others);

    puts("Done.");
}

void increase_number(Orders *orders) {
    printf("Number of seats: ");
    int num = getint() + 1;
    if (num < MIN_SIZE || num > MAX_SIZE) {
        puts("Invalid input.");
        return;
    }

    int size = next_power_of_two(num);
    if (num < orders->size) {
        if (num <= LENGTH(orders)) {
            printf("Less than the number of remaining orders.");
            return;
        }
        shrink_buf(orders, size);
    } else {
        expand_buf(orders, size);
    }

    puts("Done.");
}

int main(void) {
    Orders orders;

    initialize();
    init_orders(&orders);

    puts("Welcome to Harekaze Ramen Shop!!");
    for (;;) {
        switch (menu()) {
            case 1:
                order_ramen(&orders);
                break;
            case 2:
                serve_ramen(&orders);
                break;
            case 3:
                increase_number(&orders);
                break;
            defalut:
                puts("Invalid choice.");
        }
    }
    return 0;
}
