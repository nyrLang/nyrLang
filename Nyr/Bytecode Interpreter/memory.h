#ifndef nyr_memory_h
#define nyr_memory_h

#include "common.h"
#include "object.h"

void* reallocate(void* ptr, size_t oldSize, size_t newSize);
void freeObjects();

void collectGarbage();
void markValue(Value value);
void markObject(Obj* object);

#define ALLOCATE(type, count) (type*)reallocate(NULL, 0, sizeof(type) * (count))

#define FREE(type, ptr) reallocate(ptr, sizeof(type), 0)

#define GROW_CAPACITY(cap) ((cap) < 8 ? 8 : (cap) * 2)

#define GROW_ARRAY(type, ptr, oldCount, newCount) \
	(type*)reallocate(ptr, sizeof(type) * (oldCount), sizeof(type) * (newCount))

#define FREE_ARRAY(type, ptr, oldCount) reallocate(ptr, sizeof(type) * (oldCount), 0)

#endif
