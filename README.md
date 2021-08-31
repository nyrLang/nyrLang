[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nyrLang/nyrLang/main.svg)](https://results.pre-commit.ci/latest/github/nyrLang/nyrLang/main)
[![codecov](https://codecov.io/gh/nyrLang/nyrLang/branch/main/graph/badge.svg?precision=2)](https://codecov.io/gh/nyrLang/nyrLang)

# nyr: A programming language

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
- CLI
	- When using the CLI the trailing semicolon is optional (so it won't crash just because of that)
- File input (must end with `.nyr`)

### How to run
- From the project root run `python3 -m Nyr` and then add some flags
- To run tests run `pytest` or `python3 -m pytest` in the project root

### Flags
- `-f [path/to/file].nyr`, `--file [Path].nyr` reads from file
	- If no input file is given it will enter CLI mode
- `-i`, `--interpret` wether to interpret the input
	- Note: Adding this flag will turn off interpreting
	- Note: Classes are not yet supported, and will raise a `NotImplementedError` if encountered
- `-o`, `--output` wether to dump the generated AST into an `ast.json` file (located at `./ast.json`)
- `-p`, `--print` wether to print the generated AST to terminal

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
	def Point(x, y) {
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
	def Point(x, y, z) {
		// super call to initialize x and y
		super(x, y);
		this.z = z;
	}

	// override calc
	def calc() {
		// call super().calc()
		return super() + this.z;
	}
}

let p = new Point3D(10, 20, 30);
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
