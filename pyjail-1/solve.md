This is what `PyJail` problems are built off of, where they restrict inputs, functions, or anything else to make it more challenging to get the flag.

Based off of the banned keys, `gdvxftundmn'~`\``@#$%^&*-/.{}`, there are only a few functions we can use, one of which is the key to solving the problem, `locals`.

`locals` is a function that has reference to all of the local parameters, including the `flag` variable which stores the flag. However, it is not as simple as just printing this out, as the `t` in `print` is blocked by the sanitizer.

To get around this, we can raise an error with a custom error message.

```
raise OSError(locals()[chr(102)+chr(108)+chr(97)+chr(103)])
```

Using the input, the problem exits in an error, but is caught by the `try-except block`, which then prints out the error message.