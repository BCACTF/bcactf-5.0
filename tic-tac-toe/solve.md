There's a million ways to solve this, but they're all centered around the
idea that Player X can make moves in spots already occupied by Player O.

Example solution (enter into browser console):
```js
for (let i = 0; i < 3; i++) {
    const cell = document.querySelector(`#cell${i}`)
    cell.disabled = false
    cell.innerText = ''
    cell.click()
}
```