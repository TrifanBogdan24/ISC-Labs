#include <stdio.h>
#include <string.h>

int main() {
    char input[50];
    printf("What do you say? ");
    fgets(input, 50, stdin);

    if (strcmp(input, "PLEASE!!!11oneone") == 0) {
        printf("Okay, here's your flag: %s\n", "FLAG_GOES_HERE");
    } else {
        printf("Wrong answer!\n");
    }

    return 0;
}
