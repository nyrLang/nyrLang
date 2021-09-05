.PHONY = nyr clean buildDir
CC = gcc

LINKERFLAG = -lm
COMPILERFLAGS = -Wincompatible-pointer-types

SRCS := $(wildcard *.c)
OBJS := $(SRCS:%c=build/%o)

nyr: ${buildDir} ${OBJS}
	@echo "Checking..."
	@set -e
	${CC} ${LINKERFLAG} $^ -o nyr
	@rm -rvf a.out>/dev/null

build/dep: build/.dep
build/.dep: $(SRCS)
	@rm -f "$@"
	@${CC} -MMD $^ -MF "$@"

include build/.dep

build/%.o: %.c ${build/.dep} common.h
	@echo "Creating object: $@"
	@${CC} -o "$@" -c $< ${COMPILERFLAGS}

clean:
	@echo "Cleaning up..."
	@rm -rvf build/*.o
	@rm -rvf build/.dep>/dev/null
	@echo "Done!"

rm: clean
	@echo "Removing..."
	@rm -rvf nyr
	@echo "Done!"
