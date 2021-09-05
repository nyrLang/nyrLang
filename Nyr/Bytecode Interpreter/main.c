#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "chunk.h"
#include "common.h"
#include "debug.h"
#include "vm.h"

static void repl() {
	char line[1024];
	for (;;) {
		printf("nyr> ");

		if (!fgets(line, sizeof(line), stdin)) {
			printf("\n");
			break;
		}

		interpret(line);
	}
}

static char* readFile(const char* path) {
	FILE* f = fopen(path, "rb");
	if (f == NULL) {
		fprintf(stderr, "Could not open file \"%s\".\n", path);
		exit(74);
	}

	fseek(f, 0L, SEEK_END);
	size_t fSize = ftell(f);
	rewind(f);

	char* buf = (char*)malloc(fSize + 1);
	if (buf == NULL) {
		fprintf(stderr, "Not enough memory to read \"%s\".\n", path);
		exit(74);
	}

	size_t bytesRead = fread(buf, sizeof(char), fSize, f);
	if (bytesRead < fSize) {
		fprintf(stderr, "Could not read file \"%s\".\n", path);
		exit(74);
	}

	buf[bytesRead] = '\0';

	fclose(f);
	return buf;
}

static void runFile(const char* path) {
	char* source = readFile(path);
	InterpretResult result = interpret(source);
	free(source);

	if (result == INTERPRET_COMPILE_ERROR) exit(65);
	if (result == INTERPRET_RUNTIME_ERROR) exit(70);
}

int main(int argc, const char* argv[]) {
	initVM();

	if (argc == 1) {
		repl();
	} else if (argc == 2) {
		runFile(argv[1]);
	} else {
		fprintf(stderr, "Usage: nyr [path]\n");
		exit(64);
	}

	freeVM();
	return 0;
}
