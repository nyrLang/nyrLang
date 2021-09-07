# nyr: bytecode interpreter

## Restrictions
The bytecode interpreter works, with the exception of some things..
- Logical and Bitwise operators
	- `!` (not/inverse/negate) works
- Compound assignment operators
	- `+=`, `-=`, etc.

## How to run
1. Run `make` in this directory (with the `Makefile`)
	- If you get some errors with a message something like this: `fatal error: opening dependency file build/.dep: No such file or directory`; make sure a directory with the name `build` exists as it will dump all the make files in there not to clutter the source dir
	- Debug messages are off by default. To turn them on remove the comments on these four lines in `common.h`:
		```C
		// #define DEBUG_PRINT_CODE
		// #define DEBUG_TRACE_EXECUTION

		// #define DEBUG_STRESS_GC
		// #define DEBUG_LOG_GC
		```
2. run `./nyr`
	- When adding no arguments it will enter a REPL
	- When a file path is provided it will try to run that file

### Note
Most of this code is from the [Crafting Interpreters](https://craftinginterpreters.com/) Book.
So huge thanks to Robert Nystrom for making this a lot easier!
