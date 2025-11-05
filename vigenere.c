#include <stdio.h>
#include <stdlib.h>

int mode, keylen;
char* inputPath;
char* outputPath;
char* key;
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

int get_keylen() {
    int length = 0;
    while (key[length] != '\0') {
        length++;
    }
    return length;
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



char process_char(char chr, char keychr){
    int chrpos = get_alphabet_position(chr);
    int keypos = get_alphabet_position(keychr);

    //printf("%i | %i\n",chrpos, ((chrpos*a)+b)%n);

    int newpos;

    if(mode == 'e'){
        newpos = (chrpos + keypos)%n;
    } else {
        newpos = (chrpos - keypos)%n;
    }
    
    //printf("%i | %i \n",newpos, n-newpos);
    if(newpos < 0){
        newpos = n+newpos;
    }
    return newpos;
}



void process_file(){
    char inchr, outchr;
    int keyindex = 0;
    while ((inchr = fgetc(inptr)) != EOF)
    {
        //printf("%i | %c \n", inchr, inchr);
        outchr = alphabet[process_char(inchr, key[keyindex])];
        keyindex = (keyindex+1) % keylen;
        fputc(outchr, outptr);
    }
}



int main(int argc, char** argv){
    if(argc != 5){
        SYNERROR:
        printf("synopsis:\n%s [e/d] [KEY] [INPUT PATH] [OUTPUT PATH]\n",argv[0]);
        return 1;
    }
    mode = argv[1][0];
    if (mode != 'e' && mode != 'd'){
        printf("invalid mode. Use e for encryption or d for decryption\n");
        goto SYNERROR;
    }

    key = argv[2];
    keylen = get_keylen();
    if(keylen == 0){
        printf("somehow primaty key length is 0");
        return 1;
    }

    inputPath = argv[3];
    inptr = fopen(inputPath, "r");
    if(inptr == NULL){
        printf("invalid input path\n");
        return 1;
    }

    outputPath = argv[4];
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

    printf("task completed succesfully! :D\n");
    return 0;
}