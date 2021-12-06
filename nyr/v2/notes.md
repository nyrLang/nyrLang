# notes
some notes for future plans?

## core
- `main` function as entry point?

## operators
operators are now custom
- can be of any lengh
- can be of any combination

maybe allow user to create custom ones
- bind complex operators to functions (in background)
- would be defined like normal functions
  ```
  let `!==` {
    return left != right;
  }
  ```
- special variables `left` and `right` for operator definitions?

characters usable for operator: `+ - * / % ! & | ^ = > <`
<br>valid custom operators (whatever they would be used for):
- `|>>%`
- `|*^*|`
- `+-*/%!&|^=><`
