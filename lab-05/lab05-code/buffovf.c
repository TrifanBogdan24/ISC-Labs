#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define _R(x) _X(x,y)|_X(y,x)
#define _X(x, y) (~(x)&(y))
#define FLAGZ 523893274, 38443313, 503880245, 1460443404, 1410780961, 1427423268, 424516192, 0


void for_the_win(int a) {
	uint32_t buf[] = { FLAGZ };
	uint32_t y = 1685760339; 
	for (int i=0; i<7; i++) { buf[i] = _R(buf[i]); }

	if (a == 0xcafebabe) {
		puts("well done, here's the flag: \n");
		printf("%s\n", buf);
	} else {
		puts("almost there, try to supply the correct arguments!");
	}
}

void acquire_info() {
	char name[13];

	printf("what's ur name?\n");
	gets(name);

	printf("bye\n");
}

int main(int argc, char **argv) {
	if (argc == 1) {
		puts("Usage: %s <name>\n");
		return 1;
	}
	char buf[] = "hey";

	if (strcmp(argv[1], "Salam") == 0) {
		printf("Welcome, brilliant one!\n");
	} else {
		printf("%s, %s\n", buf, argv[1]);
	}

	acquire_info();

	exit(0);
}
