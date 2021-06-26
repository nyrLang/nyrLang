[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/niyrme/NyrLang/senpai.svg)](https://results.pre-commit.ci/latest/github/niyrme/NyrLang/senpai)

# Nyr: A soon-to-be programming language

## Features
- CLI
- File input (must end with `.nyr`)

### Flags
- `-f [Path].nyr`, `--file [Path].nyr` reads from file
- `-i (true|false)`, `--interpret (true|false)` wether to interpret the input (`true`, `false`)
	- Note: Many statements/operations are not yet supported, and will raise a `RuntimeError` if one is encountered
- `-o (true|false)`, `--output (true|false)` wether to dump the generated AST into an `ast.json` file (located at `./Nyr/ast.json`)

- - -

### Can parse:
- Numbers (Integers, Floats)
- Strings (`"A string";`, `'Another string, but with single quotes';`)
- Comments (`// A comment`, `/* A Multiline Comment */`)

- Binary Expressions (`+`, `-`, `*`, `/`)
- Assignment Expressions (`x = 5;`, `x = y = 7;`, `a += 2;`)

- Equality Operators (`==`, `!=`)
- Relational Operators (`>`, `<`, `>=`, `<=`)
- Logical Operators (`&&`, `||`)

- Block Statements (`{ x = 5; }`)
- If Statements (`if (x > 5) x = 0;`)
	- Else Statements (`if (x > 5) x = 0; else { x += 1; }`)
- Variable Statements (`let i = 0;`, `let j;`)
- Variable members (`x.y;`)
	- Computed members (`x[0];`)

- For-loops (init, test and update can each be empty)
	- `for (let i=0; i < 10; i += 1) { x += i; }`
	- `for (;;) { x += 1; }`
- While-loops (`while (x < 5) { x += 1; }`)
- Do-While-loops (`do { x += 1; } while (x < 10); `)

- Functions (`def square(x) { return x * x; }`)
- Function calls
	- Simple calls (`foo();`)
	- With arguments (`foo(x);`)
	- Nested function calls (`square(square(2));`)
	- Chained function calls (`callbackFunction()();`)
	- Member function calls (`core.print("Hello, World!")`)
