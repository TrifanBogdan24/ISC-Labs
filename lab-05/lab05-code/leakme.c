#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>


void call_me_maybe() {
	FILE *f = fopen(".leakflag", "r");
	if (!f) {
		printf(
			"File opening failed!\n"
			"Note: there is no flag available locally, try it on the remote server!\n"
		);
		fflush(stdout);
		exit(1);
	}
	char buf[100];
	(void)fgets(buf, sizeof(buf) - 1, f);
	fclose(f);
	printf("%s\n", buf);
	exit(0);
}

void flush_stdin() {
	int c;
	while ((c = getchar()) != '\n' && c != EOF) { }
}

int get_user_info(char *fname, char *lname) {
	char input[30];
	int isvalid = 0;
	while (!isvalid) {
		printf("Please enter your full name:\n");
		if (scanf("%[^\n]s%*c", input) == EOF) return 0;
		flush_stdin();

		char *first_space = strchr(input, ' ');
		if (!first_space) {
			printf("Invalid name, please try again: \n");
		  	printf(input);
		  	printf("\n");
			continue;
		}
		*first_space = 0;
		int n = first_space - input;
		printf("n=%i, fspace=%s\n", n, first_space);
		memcpy(fname, input, n);
		fname[n] = 0;
		memcpy(lname, first_space + 1, 30 - n);
		lname[20] = 0;
		isvalid = 1;
	}
	return isvalid;
}

int main(int argc, char **argv) {
	char fname[20], lname[20];
	if (!get_user_info(fname, lname)) {
		exit(1);
	}
	printf("Welcome, %s son of %s!\n", fname, lname);
	printf("The function's address was: 0x%04lX :P!\n", (uintptr_t)call_me_maybe);
	return 0;
}
