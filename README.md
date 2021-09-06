[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nyrLang/nyrLang/main.svg)](https://results.pre-commit.ci/latest/github/nyrLang/nyrLang/main)
[![codecov](https://codecov.io/gh/nyrLang/nyrLang/branch/main/graph/badge.svg?precision=2)](https://codecov.io/gh/nyrLang/nyrLang)

# nyr: A programming language

## IMPORTANT NOTE
Since I've got a working bytecode interpreter now, I'll stop working on the python script monster.
Don't know if I will ever pick it back up.
If not I'll move the bytecode one into it's own repo (and maybe archive this one? or leave open for PRs of others that want to work on this one)
Since some spec has changed with the addition of the bytecode interpreter, please refer to the README from [this commit](https://github.com/nyrLang/nyrLang/tree/5195dafff7e30c21d48c0028a44f8ca8a74fda55)

## TOC
- [Features]
- [Flags]
- [Requirements]
- ["Types"]
	- [Comments]
	- [Numbers]
	- [Strings]
- [Operators]
- [Variables]
- [Conditionals]
- [Loops]
- [Functions]
- [Classes]

- - -

## Features
- Interactive mode
	- When using the Interactive mode the trailing semicolon is optional (so it won't crash just because of that)
- File input (must end with `.nyr`)
- A Bytecode Interpreter can be found in `Nyr/Bytecode Interpreter/`

### How to run
- From the project root run `python3 -m Nyr` and then add some flags
- To run tests run `pytest` or `python3 -m pytest` in the project root

### Flags
| Short Flag | Long Flag     | Description | Note |
|------------|---------------|-------------|------|
| `-h`       | `--help`      | print a short help message |
| `-f`       | `--file`      | read from file (must end with `.nyr`); not providing one will enter Interactive mode mode |
| `-i`       | `--interpret` | turn off interpretation | Classes are not yet supported, and will raise a `NotImplementedError` if encountered
| `-o`       | `--output`    | dump generated AST to `ast.json` (located at project rood) |
| `-p`       | `--print`     | print generated AST to terminal |
| `-d`       | `--debug`     | print debug messages on what the interpreter is doing |

- - -

## Requirements
- Python 3.9

- - -

## "Types"

### Comments
```
// A single-line comment
/*
	A multiline
	comment
*/
```

### Numbers
```
// Integers
42;
-3;

// Floats
3.141;
-2.718;
```

### Strings
```
"A very nice string";

// Multi-line
"A string
can also be
multi-line!";
```

- - -

## Operators
```
/*
	Binary Operators:
		+, // add
		-, // subtract
		*, // multiply
		/, // divide
		%  // modulo

	Equality Operators:
		==, // equals
		!=  // inequals

	Relational Operators:
		>,  // greater than
		<,  // less than
		>=, // greater than or equal
		<=  // less than or equal

	Logical Operators:
		&&, // and
		||, // or
		!   // not

	Bitwise Operators:
		&, // bitwise and
		|, // bitwise or
		^  // bitwise xor
*/
```

- - -

## Variables
```
// variable declaration
let x = 0;

// declaration without initial value
let y;

// multiple declarations
let a, b = "word", c;

// variable members
// static members
b.length;

// computed members
b[0];
```

- - -

## Conditionals
```
// if, else-if, else
if (x < 10) {
	x += 1;
} else if (x == 4) {
	x = 4;
} else {
	x = 0;
}

// short if, else-if, else
if (x >= 10) x = 0;
else if (x != 4) x += 1;
else x = 6;

// they can also be on different lines
if (x >= 10)
	x = 0;
else if (x != 4)
	x += 1;
else
	x = 6;
```

- - -

## Loops
```
/* For-loop
	for ('init'; 'test'; 'update') { }
	any combination if init, test and update can be left empty
	example:
		for (; i < 10; ) { }
*/
for (let i = 0; i < 10; i += 1) {

}

// While-loop
while(x < 10) {
	x += 1;
}

// Do-While-loop
do {
	x += 1;
} while (x < 10);
```

- - -

## Functions
```
// function declaration
def square(x) {
	return x * x;
}

// recursion
def factorial(x) {
	if (x <= 1) {
		return 1;
	} else {
		return x * factorial(x - 1);
	}
}

// call square(2)
square(2);

// nested calls
square(square(2));

// chaied functions
callbackFuntion()();

// member functions
core.print("Hello, nyr!");
```

- - -

## Classes
```
// A class definition
class Point {
	// This is how the default constructor will look like
	def init(x, y) {
		this.x = x;
		this.y = y;
	}

	// class method 'calc'
	def calc() {
		return this.x + this.y;
	}
}

// Point3D inherits from Point
class Point3D : Point {
	def init(x, y, z) {
		super.init(x, y);
		this.z = z;
	}

	// override calc
	def calc() {
		return super.calc() + this.z;
	}
}

let p = Point3D(10, 20, 30);
```

[Features]: #Features
[Flags]: #Flags
[Requirements]: #Requirements
["Types"]: #"Types"
[Comments]: #Comments
[Numbers]: #Numbers
[Strings]: #Strings
[Operators]: #Operators
[Variables]: #Variables
[Conditionals]: #Conditionals
[Loops]: #Loops
[Functions]: #Functions
[Classes]: #Classes
