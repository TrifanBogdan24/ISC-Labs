#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>


// just ignore those...
#define S1 "7\xdf\xc3\xa9\x81,q\xe0j\xf7\x04\xa9\xf1\x83\x17\xf7\xf0\xb0 \x11"
#define S2 "\t\xfb\xf7\xa5\x91?d\xc8{\xb0\x01\x81\xf2\xc7\b\xdf\xf0\xf6\x39\x1b"
#define Z2(x) x=
#define Z6(y) y++
#define X0(y) ^y
#define Y5(z) *z
#define X7(x) x

char *s = S2;
char *decrypt_flag(char *r) {
	while (Y5(r)){Z2(Y5(Z6(r)))X7(119)X0(Y5(r)X0(*s));Z6(s);};
	return r;
}

volatile int deez = 0;

int check_fl0gz0rx(char *input) {
	char buf[] = S1;
	int n = strlen(input);
	if (!deez || n != strlen(buf)) return 0;
	return strcmp(input, decrypt_flag(buf)-n) == 0;
}

int main(int argc, char **argv) {
	if (argc == 1) {
		puts("Usage: %s <secret_flag>\n");
		return 1;
	}

	if (check_fl0gz0rx(argv[1])) {
		printf("Congratulations, you got the flag: %s\n", argv[1]);
		exit(0);
	} else {
		printf("Nope, your given flag was invalid!\n");
		exit(2);
	}
	return 3;
}


