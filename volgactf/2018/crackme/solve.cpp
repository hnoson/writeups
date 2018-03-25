#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cryptopp/aes.h>
#include <cryptopp/cryptlib.h>
#include <cryptopp/filters.h>
#include <cryptopp/modes.h>

std::string decrypt(unsigned char *enc, int len, unsigned char *key) {
    unsigned char iv[CryptoPP::AES::BLOCKSIZE], cipher[0x100];
    std::string decrypted;
    memcpy(iv,enc,CryptoPP::AES::BLOCKSIZE);
    memcpy(cipher,enc+CryptoPP::AES::BLOCKSIZE,len - CryptoPP::AES::BLOCKSIZE);

    CryptoPP::AES::Decryption aesDecryption(key, CryptoPP::AES::DEFAULT_KEYLENGTH);
    CryptoPP::CBC_Mode_ExternalCipher::Decryption cbcDecryption(aesDecryption, iv);

    CryptoPP::StreamTransformationFilter stfDecryptor(cbcDecryption, new CryptoPP::StringSink(decrypted));
    stfDecryptor.Put(cipher, len - CryptoPP::AES::BLOCKSIZE);
    stfDecryptor.MessageEnd();
    return decrypted;
}

int main(void) {
    FILE *fp = fopen("CrackMe.txt","r");
    unsigned char enc[0x100], key[16];
    int len = fread(enc,1,0xff,fp);

    // 0x36524421
    for (unsigned int i = 0; i < 0x40; i++) {
        for (unsigned int j = 0; j < 0x100; j++) {
            printf("\r0x%02x%02x0000",i,j);
            fflush(stdout);
            for (unsigned int k = 0; k < 0x100; k++) {
                for (unsigned int l = 0; l < 0x80; l++) {
                    for (unsigned int m = 0; m < 2; m++) {
                        for (int n = 0; n < 4; n++) {
                            key[n*4] = l << 1;
                            key[n*4+1] = k;
                            key[n*4+2] = j;
                            key[n*4+3] = i | (m * 0xc0);
                        }
                        try {
                            std::string decrypted = decrypt(enc,len,key);
                            if (decrypted.find("VolgaCTF") != std::string::npos) {
                                std::cout << decrypted << std::endl;
                            }
                        } catch(std::exception e){}
                    }
                }
            }
        }
    }
    return 0;
}
