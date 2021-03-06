#include <stdio.h>
#include <string.h>

#include "common.h"
#include "scanner.h"

typedef struct {
	const char* start;
	const char* current;
	int line;
} Scanner;

Scanner scanner;

void initScanner(const char* source) {
	scanner.start = source;
	scanner.current = source;
	scanner.line = 1;
}

static bool isAtEnd() {
	return *scanner.current == '\0';
}

static char advance() {
	scanner.current++;
	return scanner.current[-1];
}

static char peek() {
	return *scanner.current;
}

static char peekNext() {
	if (isAtEnd()) return '\0';
	return scanner.current[1];
}

static bool match(char expected) {
	if (isAtEnd()) return false;
	if (*scanner.current != expected) return false;
	advance();
	return true;
}

static Token makeToken(TokenType type) {
	Token token;

	token.type = type;
	token.start = scanner.start;
	token.length = (int)(scanner.current - scanner.start);
	token.line = scanner.line;

	return token;
}

static Token errorToken(const char* message) {
	Token token;

	token.type = TOKEN_ERROR;
	token.start = message;
	token.length = (int)strlen(message);
	token.line = scanner.line;

	return token;
}

static void skipWhitespace() {
	for (;;) {
		char c = peek();
		switch (c) {
			case ' ':
			case '\r':
			case '\t': {
				advance();
				break;
			}
			case '\n': {
				scanner.line++;
				advance();
				break;
			}
			case '/': {
				// Handle single-line comments
				if (peekNext() == '/') {
					while (peek() != '\n' && !isAtEnd())
						advance();
				}
				// Handle multi-line comments
				else if (peekNext() == '*') {
					advance();
					do {
						advance();
						if (peek() == '\n') {
							scanner.line++;
						}
					} while (peek() != '*' && peekNext() != '/' && !isAtEnd());
				}
				else {
					return;
				}
				break;
			}
			default: return;
		}
	}
}

static Token string() {
	while (peek() != '"' && !isAtEnd()) {
		if (peek() == '\n') scanner.line++;
		advance();
	}

	if (isAtEnd()) return errorToken("Unterminated string.");

	advance();
	return makeToken(TOKEN_STRING);
}

static bool isDigit(char c) {
	return c >= '0' && c <= '9';
}

static Token number() {
	while (isDigit(peek())) advance();

	if (peek() == '.' && isDigit(peekNext())) {
		do {
			advance();
		} while (isDigit(peek()));
	}

	return makeToken(TOKEN_NUMBER);
}

static bool isAlpha(char c) {
	return (c >= 'a' && c <= 'z')
		|| (c >= 'A' && c <= 'Z')
		|| (c == '_');
}

static TokenType checkKeyword(int start, int length, const char* rest, TokenType type) {
	if (
		((scanner.current - scanner.start) == start + length)
		&& (memcmp(scanner.start + start, rest, length) == 0)) {
		return type;
	}

	return TOKEN_IDENTIFIER;
}

static TokenType identifierType() {
	switch (scanner.start[0]) {
		case 'c': return checkKeyword(1, 4, "lass", TOKEN_CLASS);
		case 'd': {
			if (scanner.current - scanner.start > 1) {
				switch (scanner.start[1]) {
					case 'e': return checkKeyword(2, 1, "f", TOKEN_DEF);
					case 'o': return checkKeyword(2, 0, "", TOKEN_DO);
				}
			}
			break;
		}
		case 'e': return checkKeyword(1, 3, "lse", TOKEN_ELSE);
		case 'f': {
			if (scanner.current - scanner.start > 1) {
				switch (scanner.start[1]) {
					case 'a': return checkKeyword(2, 3, "lse", TOKEN_FALSE);
					case 'o': return checkKeyword(2, 1, "r", TOKEN_FOR);
				}
			}
			break;
		}
		case 'i': return checkKeyword(1, 1, "f", TOKEN_IF);
		case 'l': return checkKeyword(1, 2, "et", TOKEN_LET);
		case 'n': return checkKeyword(1, 3, "ull", TOKEN_NULL);
		case 'p': return checkKeyword(1, 4, "rint", TOKEN_PRINT);
		case 'r': return checkKeyword(1, 5, "eturn", TOKEN_RETURN);
		case 's': return checkKeyword(1, 4, "uper", TOKEN_SUPER);
		case 't': {
			if (scanner.current - scanner.start > 1) {
				switch (scanner.start[1]) {
					case 'h': return checkKeyword(2, 2, "is", TOKEN_THIS);
					case 'r': return checkKeyword(2, 2, "ue", TOKEN_TRUE);
				}
			}
			break;
		}
		case 'w': return checkKeyword(1, 4, "hile", TOKEN_WHILE);
	}
	return TOKEN_IDENTIFIER;
}

static Token identifier() {
	while (isAlpha(peek()) || isDigit(peek())) advance();
	return makeToken(identifierType());
}

Token scanToken() {
	skipWhitespace();
	scanner.start = scanner.current;

	if (isAtEnd()) {
		return makeToken(TOKEN_EOF);
	}

	char c = advance();
	if (isDigit(c)) {
		return number();
	}
	if (isAlpha(c)) {
		return identifier();
	}

	switch (c) {
		case '(': return makeToken(TOKEN_LPAREN);
		case ')': return makeToken(TOKEN_RPAREN);
		case '{': return makeToken(TOKEN_LBRACE);
		case '}': return makeToken(TOKEN_RBRACE);
		case '[': return makeToken(TOKEN_LBRACKET);
		case ']': return makeToken(TOKEN_RBRACKET);
		case '.': return makeToken(TOKEN_DOT);
		case ':': return makeToken(TOKEN_COLON);
		case ',': return makeToken(TOKEN_COMMA);
		case ';': return makeToken(TOKEN_SEMICOLON);
		case '+': return makeToken(match('=') ? TOKEN_PLUS_EQUAL : TOKEN_PLUS);
		case '-': return makeToken(match('=') ? TOKEN_MINUS_EQUAL : TOKEN_MINUS);
		case '*': return makeToken(match('=') ? TOKEN_ASTERISK_EQUAL : TOKEN_ASTERISK);
		case '/': return makeToken(match('=') ? TOKEN_SLASH_EQUAL : TOKEN_SLASH);
		case '!': return makeToken(match('=') ? TOKEN_BANG_EQUAL : TOKEN_BANG);
		case '=': return makeToken(match('=') ? TOKEN_EQUAL_EQUAL : TOKEN_EQUAL);
		case '>': return makeToken(match('=') ? TOKEN_GREATER_EQUAL : TOKEN_GREATER);
		case '<': return makeToken(match('=') ? TOKEN_LESS_EQUAL : TOKEN_LESS);
		case '"': return string();
	}

	return errorToken("Unexpected character");
}
