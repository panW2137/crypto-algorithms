#include <stdio.h>
#include <stdint.h>
#include "tables.h"

uint64_t block = 0x0000000000000000;
uint64_t key = 0x0000000000000000;
uint64_t roundKeys[16];

void print_hex(uint64_t hex){
    printf("0x%016llx",hex);
}
void println_hex(uint64_t hex){
    printf("0x%016llx\n",hex);
}

uint64_t permutate(uint64_t input, uint8_t inputWidth, uint8_t tableWidth, uint8_t tableHeight, uint8_t table[tableHeight][tableWidth]){
    uint64_t output = 0;
    
    for(int y=0; y<tableHeight; y++){
        for(int x=0; x<tableWidth; x++){
            output <<= 1;
            uint8_t bitPosition = inputWidth-table[y][x];
            uint64_t inputBit = (input >> bitPosition) & 1;
            output |= inputBit;
        }
    }
    return output;
}

uint64_t cyclic_shift_left(uint64_t value, uint8_t shift){
    return ((value << shift) | (value >> (28 - shift))) & 0x0FFFFFFF;
}

void generate_round_keys(uint64_t key, uint64_t output[16]) {
    uint64_t C = permutate(key, 64, 7, 4, PC1_C);
    uint64_t D = permutate(key, 64, 7, 4, PC1_D);
    
    for(int i = 0; i < 16; i++) {
        C = cyclic_shift_left(C, shifts[i]);
        D = cyclic_shift_left(D, shifts[i]);
        
        uint64_t CD = (C << 28) | D;
        
        output[i] = permutate(CD, 56, 6, 8, PC2);
    }
}

uint64_t lookup_sbox(uint64_t value, uint8_t sbox[4][16]){
    uint8_t row = ((value >> 4) & 0x02) | (value & 0x01);
    uint8_t col = (value >> 1) & 0x0F;

    return sbox[row][col];
}

//pojedyncza runda feistela
uint64_t feistel_round(uint64_t block, uint64_t roundKey){
    //pobierz lewa i prawa polowe
    uint64_t rightHalf = block & 0x00000000ffffffffULL;
    uint64_t leftHalf = block & 0xffffffff00000000ULL;

    //stara prawa to nowa lewa
    uint64_t newLeft = rightHalf << 32;

    //rozszerzenie prawej polowy
    uint64_t expandedBlock = permutate(rightHalf, 32, 6, 8, E);

    //xor z kluczem rundy
    expandedBlock ^= roundKey;

    //podziel na 6-bitowe grupy i wsadz do s-boxa
    uint64_t sboxOutput = 0;
    for(int i=0; i<8; i++){
        sboxOutput <<= 4;
        uint64_t chunk = (expandedBlock >> (42 - i * 6)) & 0x3f;
        sboxOutput |= lookup_sbox(chunk, S_BOXES[i]);
    }
    //permutacja
    sboxOutput = permutate(sboxOutput, 32, 8, 4, P);
    //xorowanie z lewa polowka
    uint64_t newRight = (leftHalf >> 32) ^ sboxOutput;

    //lewa i prawa polowka laczone sa w nowy blok 64-bitowy
    return newLeft | newRight;
}

int main(int argc, int** argv){
    println_hex(block);

    //permutacja poczatkowa
    block = permutate(block, 64, 8, 8, IP);
    //wygeneruj klucze rundy
    generate_round_keys(key, roundKeys);

    //16 rund feistela
    for(int i=0; i<16; i++){
        block = feistel_round(block, roundKeys[i]);
    }

    //permutacja konckowa
    block = ((block & 0xFFFFFFFF) << 32) | ((block >> 32) & 0xFFFFFFFF);
    block = permutate(block, 64, 8, 8, IP_inv);

    println_hex(block);
}
