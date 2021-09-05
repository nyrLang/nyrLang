#ifndef nyr_compiler_h
#define nyr_compiler_h

#include "object.h"
#include "scanner.h"
#include "vm.h"

ObjFunction* compile(const char* source);

void markCompilerRoots();

static Chunk* currentChunk();

static void errorAt(Token* token, const char* message);
static void error(const char* message);
static void errorAtCurrent(const char* message);

#endif
