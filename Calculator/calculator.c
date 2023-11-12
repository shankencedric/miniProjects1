#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define newline printf("\n")

char * parseInput () {
    return 0;
}

char* stringArrayToParagraph(char stringArray[][2]) {
    char* string; 
    //for (int i = 0; i < stringArray; i) {
    //    strcat(string, stringArray[i]);
    //}
    //d
    printf("%s", string);
    return 0;
}

void appendToStringArray(char*** pDestinationArray, int destinationArraySize, char stringToAppend[]) {
    // extend the destination array
    *pDestinationArray = (char**) realloc(*pDestinationArray, destinationArraySize + strlen(stringToAppend)); 
    // append str
    strcat(*pDestinationArray[destinationArraySize-1], stringToAppend);
}

void printConsole() {
}

void printEnterScreen() {
    printf("Welcome to CALCULATHOR! Made by shankencedric."); newline;
}

int main () {

    //d
    char** stringArray = malloc(sizeof(char)); // initial size of 2d array (ie, array of strings)
    int stringArraySize = 0;
    appendToStringArray(&stringArray, stringArraySize, "ABC");
    printf("%x", stringArray);
    free(stringArray);
   







    return 0; 

    printEnterScreen();

    printConsole();
    char* input = parseInput();




}