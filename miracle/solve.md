# Miracle

ESLint, "use strict", deno, and most normal people block this weird js feature. Essentially, a leading
zero casts the number to octal. [https://eslint.org/docs/latest/rules/no-octal#rule-details](https://eslint.org/docs/latest/rules/no-octal#rule-details)

```javascript
let a = 77;

console.log(a); // 77

let b = 0x77; 

console.log(b); // 0x77, an obviously hexadecimal number, is 119 in decimal

let c = 077; //looks like a pseudo-normal number

console.log(c); // 63, since 77 in base 8 is 63 in base 10
```

the `Number(ans)` function is willing to strip leading zeros and correctly 
turns "077" into 77.

However, if we directly `eval(ans)` JS takes over, turning it into 63.