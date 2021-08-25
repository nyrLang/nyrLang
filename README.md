[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/niyrme/NyrLang/senpai.svg)](https://results.pre-commit.ci/latest/github/niyrme/NyrLang/senpai)
[![codecov](https://codecov.io/gh/niyrme/NyrLang/branch/senpai/graph/badge.svg?token=E6B3LA2R9O)](https://codecov.io/gh/niyrme/NyrLang)

# Nyr: A programming language

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

### Flags
- `-f [path/to/file].nyr`, `--file [Path].nyr` reads from file (Default: `null`)
- `-i (true|false)`, `--interpret (true|false)` wether to interpret the input (`true`, `false`) (Default: `false`)
	- Note: Many statements/operations are not yet supported, and will raise a `NotImplementedError` if encountered
- `-o (true|false)`, `--output (true|false)` wether to dump the generated AST into an `ast.json` file (located at `./ast.json`) (Default: `false`)
- `-p (true|false)`, `--print (true|false)` wether to print the generated AST to terminal (Default: `false`)

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
// Double Quotes
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
	Binary operators:
		+, -, *, /, %

	Equality Operators:
		==, !=

	Relational Operators:
		>, <, >=, <=

	Logical Operators:
		&&, ||, !
*/
```

- - -

## Variables
```
// Variable declaration
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
else if (x != 4) += 1;
else x = 6;
```

- - -

## Loops
```
/* For-loop
	for ('init'; 'test'; 'update') { }
	any combination if init, test and update can be left empty
	example for (; i < 10; ) { }
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
// square function
def square(x) {
	return x * x;
}

// call square(2)
square(2);

// nested calls
super(super(2));

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

// Point3d inherits from Point
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
