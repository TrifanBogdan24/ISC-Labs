# generate the flags

.PHONY: all

all: obfusflag buffovf leakme

obfusflag: obfusflag.c
	gcc $< -o $@ -g

buffovf: buffovf.c
	# just do it!
	gcc $< -o $@ -std=c99 -Wno-deprecated-declarations -fno-stack-protector \
		-no-pie -fno-pic -m32 -g

leakme: leakme.c
	gcc $< -o $@ -std=c99 -Wno-deprecated-declarations -fno-stack-protector -m32 -g

clean:
	rm -f obfusflag buffovf leakme

