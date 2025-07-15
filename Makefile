main: main.c
	gcc -std=c99 -Wall -Werror -o main main.c

clean:
	rm -f main
