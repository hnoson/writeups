#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>

void timeout() {
    puts("time out!");
    exit(-1);
}

typedef struct Note {
    char title[0x10];
    struct Note *prev;
    struct Note *next;
    char *content;
} Note;

Note head;
int size;

void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);

    head.prev = &head;
    head.next = &head;
}

void getnline(char *buf, int size) {
    int i;
    for (i = 0; i < size; i++) {
        if (read(0, &buf[i], 1) != 1) {
            exit(-1);
        } else if (buf[i] == '\n') {
            buf[i] = '\0';
            break;
        }
    }
    buf[size - 1] = '\0';
}

int getint() {
    char buf[0x20];
    getnline(buf, 0x20);
    return atoi(buf);
}

int menu() {
    puts("1. Create note");
    puts("2. Write content");
    puts("3. Show content");
    puts("4. Delete note");
    printf("Choice: ");
    return getint();
}

void create_note() {
    if (size >= 0x50) {
        puts("Too many notes");
    }

    Note *note = malloc(sizeof(Note));
    printf("Title: ");
    getnline(note->title, 0x10);
    note->next = &head;
    note->prev = head.prev;
    head.prev->next = note;
    head.prev = note;
    size++;
}

Note *find_note(char *title) {
    for (Note *p = head.next; p != &head; p = p->next) {
        if (strcmp(title, p->title) == 0) {
            return p;
        }
    }
    puts("No such a note with the title");
    return NULL;
}

void write_content() {
    char title[0x10];
    printf("Title of note to write content: ");
    getnline(title, 0x10);
    Note *note = find_note(title);
    if (note == NULL) {
        return;
    }
    if (note->content != NULL) {
        puts("You have already written content");
        return;
    }
    printf("Size of content: ");
    int size = getint();
    if (size <= 0 || size > 0x50) {
        puts("Too big");
        return;
    }
    note->content = malloc(size);
    printf("Content: ");
    getnline(note->content, size);
}

void show_content() {
    char title[0x10];
    printf("Title of note to show content: ");
    getnline(title, 0x10);
    Note *note = find_note(title);
    if (note == NULL) {
        return;
    }
    if (note->content) {
        puts(note->content);
    }
}

void delete_note() {
    char title[0x10];
    printf("Title of note to delete: ");
    getnline(title, 0x10);
    Note *note = find_note(title);
    if (note == NULL) {
        return;
    }
    note->prev->next = note->next;
    note->next->prev = note->prev;
    free(note->content);
    free(note);
    size--;
}

int main(void) {
    initialize();

    for (;;) {
        switch (menu()) {
            case 1:
                create_note();
                break;
            case 2:
                write_content();
                break;
            case 3:
                show_content();
                break;
            case 4:
                delete_note();
                break;
            default:
                puts("Invalid choice");
        }
    }
    return 0;
}
