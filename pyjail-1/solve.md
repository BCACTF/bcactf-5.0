This is what `PyJail` problems are built off of, where they restrict inputs, functions, or anything else to make it more challenging to get the flag.

Based off of the banned keys, `gdvxftundmn'~`\``@#$%^&*-/.{}`, there are only a few functions we can use, one of which is the key to solving the problem, `locals`.

`locals` is a function that has reference to all of the local parameters, including the `flag` variable which stores the flag. However, it is not as simple as just printing this out, as the `n` and `t` in `print` is blocked by the sanitizer.

To get around this, we can raise an error with a custom error message.

```py
raise OSError(locals()[chr(102)+chr(108)+chr(97)+chr(103)])
```

Note: There is an unintended solution to both original JailBreak challenges, which is by abusing Python normalization and submitting a payload such as `𝘱𝘳𝘪𝘯𝘵(𝘧𝘭𝘢𝘨)`. Other unintended solutions to JailBreak 1 involve `help()`.