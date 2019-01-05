#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define LEN 48

void xor(char *a, char *b, int n) {
    for (int i = 0; i < n; i++) {
        a[i] ^= b[i];
    }
}

char *from_bytes(char *a, char *b, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < 8; j++) {
            b[i * 8 + 7 - j] = (a[i] >> j) & 1;
        }
    }
}

void from_bitvector(char *a, char *b, int n) {
    memset(b, 0, n / 8);
    for (int i = 0; i < n / 8; i++) {
        for (int j = 0; j < 8; j++) {
            b[i] = (b[i] << 1) + a[i * 8 + j];
        }
    }
}

char *triple(char *a, int n) {
    char *ret = malloc(n * 3);
    for (int i = 0; i < n * 3; i++) {
        ret[i] = a[i / 3];
    }
    return ret;
}

void print(char *a, int n) {
    for (int i = 0; i < n; i++) {
        printf("%d", a[i]);
    }
    puts("");
}

void swap(char *a, char *b) {
    char tmp = *a;
    *a = *b;
    *b = tmp;
}

char *matinv(char *mat, int n) {
    char *ret = malloc(n * n);
    char *tmp = malloc(n * n);
    memcpy(tmp, mat, n * n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            ret[i * n + j] = i == j;
        }
    }
    for (int i = 0; i < n; i++) {
        if (tmp[i * n + i] == 0) {
            for (int j = i + 1; j < n; j++) {
                if (tmp[i * n + j] == 1) {
                    for (int k = 0; k < n; k++) {
                        swap(&tmp[k * n + i], &tmp[k * n + j]);
                        swap(&ret[k * n + i], &ret[k * n + j]);
                    }
                }
            }
        }
        if (tmp[i * n + i] == 0) {
            return NULL;
        }
        for (int j = 0; j < n; j++) {
            if (i != j && tmp[i * n + j] == 1) {
                for (int k = 0; k < n; k++) {
                    tmp[k * n + j] ^= tmp[k * n + i];
                    ret[k * n + j] ^= ret[k * n + i];
                }
            }
        }
    }
    return ret;
}

void read_flag(char **buf) {
    char filename[20];
    for (int i = 0; i < 31; i++) {
        sprintf(filename, "data/flag_%02d", i);
        FILE *fp = fopen(filename, "rb");
        buf[i] = malloc(6 * (LEN + 1));
        fread(buf[i], 6, LEN + 1, fp);
    }
}

char *mul(char *mat, char *vec, char *dst, int n) {
    for (int i = 0; i < n; i++) {
        dst[i] = 0;
        for (int j = 0; j < n; j++) {
            dst[i] ^= vec[j] * mat[j * n + i];
        }
    }
}

void insert_noise(char *v, int x) {
    for (int i = 0; x; i++) {
        v[i * 3 + x % 3] ^= 1;
        x /= 3;
    }
}

void decode(char *a, char *b, int n) {
    for (int i = 0; i < n; i++) {
        char sum = 0;
        for (int j = 0; j < 3; j++) {
            sum += a[i * 3 + j];
        }
        b[i] = sum / 2;
    }
}

void decrypt(char *enc, char *key, char *dst) {
    char x[LEN];
    char mat[LEN * LEN];
    from_bytes(enc, mat, 6 * LEN);
    mul(mat, key, x, LEN);
    char y[LEN];
    from_bytes(enc + 6 * LEN, y, 16);
    xor(x, y, LEN);
    char m[16];
    decode(x, m, 16);
    from_bitvector(m, dst, 16);
}

int main(void) {
    char *inv = NULL;
    char *x;
    for (int i = 0; !inv && i < 1024 + 512; i++) {
        char pt[2], ct[6 * (LEN + 1)];
        char pfn[0x20], cfn[0x20];
        sprintf(pfn, "data/plaintext_%03d", i);
        FILE *fpt = fopen(pfn, "rb");
        fread(pt, 2, 1, fpt);
        sprintf(cfn, "data/ciphertext_%03d", i);
        FILE *fct = fopen(cfn, "rb");
        fread(ct, 6, LEN + 1, fct);

        char tmp[0x100];
        from_bytes(pt, tmp, 2);
        x = triple(tmp, 16);
        from_bytes(ct + 6 * LEN, tmp, 6);
        xor(x, tmp, LEN);
        char mat[LEN * LEN];
        from_bytes(ct, mat, 6 * LEN);
        inv = matinv(mat, LEN);
    }
    char *enc[31];
    read_flag(enc);
    char key[LEN];
    for (int i = 0; i < 43046721; i++) {
        if (i % 0x100 == 0) {
            printf("\r%#x", i);
            fflush(stdout);
        }
        insert_noise(x, i);
        mul(inv, x, key, LEN);
        insert_noise(x, i);
        char m[3];
        m[2] = '\0';
        decrypt(enc[0], key, m);
        if (strcmp(m, "35") == 0) {
            decrypt(enc[1], key, m);
            if (strcmp(m, "C3") == 0) {
                puts("");
                for (int i = 0; i < 31; i++) {
                    decrypt(enc[i], key, m);
                    printf("%s", m);
                }
                break;
            }
        }
    }
    return 0;
}
