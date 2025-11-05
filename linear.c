#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int charerror = 0;
int modinverror = 0;
int a, b, mode;
char* inputPath;
char* outputPath;
FILE* inptr;
FILE* outptr;

int n = 66;
char alphabet[] = {
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',
    '\n',' ','.',','
};



int a_is_invalid(){
    if(a == 0){
        printf("value A cannot be 0\n");
        return 1;
    }

    //gdc
    int valA = a;
    int valB = n;

    while (valB != 0) {
        int temp = valB;
        valB = valA % valB;
        valA = temp;
    }
    int gdc = valA;

    if(gdc != 1){
        printf("values A and N must be coprime (gdc(A,N) = 1). current value N: %i\n",n);
        return 1;
    }
    return 0;

}



int gcdExtended(int a, int b, int* x, int* y)
{
    if (a == 0) {
        *x = 0, *y = 1;
        return b;
    }

    int x1, y1;
    int gcd = gcdExtended(b % a, a, &x1, &y1);

    *x = y1 - (b / a) * x1;
    *y = x1;

    return gcd;
}



int modinv(int A, int M)
{
    int x, y;
    int g = gcdExtended(A, M, &x, &y);
    if(g != 1){
        modinverror = 1;
        return 1;
    }
    else{
        int res = (x % M + M) % M;
        return res;
    }
}



int get_alphabet_position(char chr){
    int pos;
    for(pos = 0; pos<n; pos++){
        if(chr == alphabet[pos]){
            return pos;
        }
    }
    //printf("illegal: %i | %c\n", chr, chr);
    return -1;
}



char process_char(char chr){
    int chrpos = get_alphabet_position(chr);
    //printf("%i | %i\n",chrpos, ((chrpos*a)+b)%n);

    if(chrpos == -1){
        charerror = 1;
    }

    int newpos;

    if(mode == 'e'){
        newpos = ((a*chrpos)+b) % n;
    } else {
        int invA = modinv(a, n);
        if(invA == -1){
            modinverror = 1;
        }
        newpos = (invA * (chrpos - b + n)) % n;
    }
    
    //printf("%i | %i \n",newpos, n-newpos);
    if(newpos < 0){
        newpos = n+newpos;
    }
    return newpos;
}



void process_file(){
    char inchr, outchr;
    while ((inchr = fgetc(inptr)) != EOF)
    {
        //printf("%i | %c \n", inchr, inchr);
        outchr = alphabet[process_char(inchr)];
        fputc(outchr, outptr);
    }
}



int main(int argc, char** argv){
    if(argc != 6){
        SYNERROR:
        printf("synopsis:\n%s [e/d] [A] [B] [INPUT PATH] [OUTPUT PATH]\n",argv[0]);
        return 1;
    }
    mode = argv[1][0];
    if (mode != 'e' && mode != 'd'){
        printf("invalid mode. Use e for encryption or d for decryption\n");
        goto SYNERROR;
    }

    a = atoi(argv[2]);
    if(a_is_invalid()){
        return 1;
    }

    b = atoi(argv[3]);

    inputPath = argv[4];
    inptr = fopen(inputPath, "r");
    if(inptr == NULL){
        printf("invalid input path\n");
        return 1;
    }

    outputPath = argv[5];
    outptr = fopen(outputPath, "w");
    if(outptr == NULL){
        printf("invalid output path. Please consult documentation for C function fopen in w mode. God help you.\n");
        return 1;
    }

    //input validated yay

    process_file();

    //printf("finished\n");

    fclose(inptr);
    fclose(outptr);

    if(charerror){
        printf("illegal character spotted. Output may not be correct\n");
        return 1;
    }
    if(modinverror){
        printf("an error occured when trying to calculate modular inverse. This is hopeless and you should give up\n");
        return 1;
    }

    printf("task completed succesfully! :D\n");
    return 0;
}