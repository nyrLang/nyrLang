#include <stdio.h>
#include <string.h>

#include "memory.h"
#include "object.h"
#include "table.h"
#include "vm.h"

#define ALLOCATE_OBJ(type, objectType) (type*)allocateObject(sizeof(type), objectType)

static Obj* allocateObject(size_t size, ObjType type) {
	Obj* object = (Obj*)reallocate(NULL, 0, size);
	object->type = type;
	object->isMarked = false;
	object->next = vm.objects;
	vm.objects = object;

#ifdef DEBUG_LOG_GC
	printf("%p allocate %zu for %d\n", (void*)object, size, type);
#endif

	return object;
}

static ObjString* allocateString(char* chars, int length, uint32_t hash) {
	ObjString* string = ALLOCATE_OBJ(ObjString, OBJ_STRING);
	string->length = length;
	string->chars = chars;
	string->hash = hash;

	push(OBJ_VAL(string));
	tableSet(&vm.strings, string, NULL_VAL);
	pop();

	return string;
}

static uint32_t hashString(const char* key, int length) {
	uint32_t hash = 2166136261u;

	for (int i = 0; i < length; i++) {
		hash ^= (uint8_t)key[i];
		hash *= 16777619;
	}

	return hash;
}

ObjString* takeString(char* chars, int length) {
	uint32_t hash = hashString(chars, length);
	ObjString* interned = tableFindString(&vm.strings, chars, length, hash);

	if (interned != NULL) {
		FREE_ARRAY(char, chars, length + 1);
		return interned;
	}

	return allocateString(chars, length, hash);
}

ObjString* copyString(const char* chars, int length) {
	uint32_t hash = hashString(chars, length);
	ObjString* interned = tableFindString(&vm.strings, chars, length, hash);

	if (interned != NULL) return interned;

	char* heapChars = ALLOCATE(char, length + 1);
	memcpy(heapChars, chars, length);
	heapChars[length] = '\0';
	return allocateString(heapChars, length, hash);
}

ObjFunction* newFunction() {
	ObjFunction* fn = ALLOCATE_OBJ(ObjFunction, OBJ_FUNCTION);
	fn->arity = 0;
	fn->name = NULL;
	initChunk(&fn->chunk);
	return fn;
}

static void printFunction(ObjFunction* fn) {
	if (fn->name == NULL) {
		printf("<script>");
		return;
	}
	printf("<fn %s>", fn->name->chars);
}

ObjNative* newNative(NativeFn function) {
	ObjNative* native = ALLOCATE_OBJ(ObjNative, OBJ_NATIVE);
	native->function = function;
	return native;
}

ObjClosure* newClosure(ObjFunction* function) {
	ObjUpvalue** upvalues = ALLOCATE(ObjUpvalue*, function->upvalueCount);
	for (int i = 0; i < function->upvalueCount; i++) {
		upvalues[i] = NULL;
	}
	ObjClosure* closure = ALLOCATE_OBJ(ObjClosure, OBJ_CLOSURE);
	closure->function = function;
	closure->upvalues = upvalues;
	closure->upvalueCount = function->upvalueCount;
	return closure;
}

ObjUpvalue* newUpvalue(Value* slot) {
	ObjUpvalue* upvalue = ALLOCATE_OBJ(ObjUpvalue, OBJ_UPVALUE);
	upvalue->location = slot;
	upvalue->next = NULL;
	upvalue->closed = NULL_VAL;
	return upvalue;
}

ObjClass* newClass(ObjString* name) {
	ObjClass* cls = ALLOCATE_OBJ(ObjClass, OBJ_CLASS);
	cls->name = name;

	initTable(&cls->methods);

	return cls;
}

ObjInstance* newInstance(ObjClass* cls) {
	ObjInstance* instance = ALLOCATE_OBJ(ObjInstance, OBJ_INSTANCE);
	instance->cls = cls;
	initTable(&instance->fields);

	return instance;
}

ObjBoundMethod* newBoundMethod(Value receiver, ObjClosure* method) {
	ObjBoundMethod* bound = ALLOCATE_OBJ(ObjBoundMethod, OBJ_BOUND_METHOD);
	bound->receiver = receiver;
	bound->method = method;

	return bound;
}

void printObject(Value value) {
	switch (OBJ_TYPE(value)) {
		case OBJ_STRING: {
			printf("%s", AS_CSTRING(value));
			break;
		}
		case OBJ_FUNCTION: {
			printFunction(AS_FUNCTION(value));
			break;
		}
		case OBJ_NATIVE: {
			printf("<native >");
			break;
		}
		case OBJ_CLOSURE: {
			printFunction(AS_CLOSURE(value)->function);
			break;
		}
		case OBJ_UPVALUE: {
			printf("upvalue");
			break;
		}
		case OBJ_CLASS: {
			printf("%s", AS_CLASS(value)->name->chars);
			break;
		}
		case OBJ_INSTANCE: {
			printf("%s instance", AS_INSTANCE(value)->cls->name->chars);
			break;
		}
		case OBJ_BOUND_METHOD: {
			printFunction(AS_BOUND_METHOD(value)->method->function);
			break;
		}
	}
}