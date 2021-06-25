[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/niyrme/NyrLang/senpai.svg)](https://results.pre-commit.ci/latest/github/niyrme/NyrLang/senpai)

# Nyr: A soon-to-be programming language

## Features
- CLI
- File input (must end with `.nyr`)

### Flags
- `-f [Path].nyr`, `--file [Path].nyr` reads from file
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
