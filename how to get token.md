# How to Get Your *Discord* Account Token

## Browser (Any)

1. **Open Developer Console**
    - Press `Ctrl + Shift + J` to open the console.
		
2. **Paste the Code**
    - Enter this code in the Console:
      ```javascript
      (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
      ```
3. **Copy Your Token**
    - Copy the token (without `'`).

Now, you have your **Account Token**!

## Discord App

### Enabling Developer Tools

1. Quit Discord.
2. Press `Win+R` to open the Run dialog.
3. Type `%appdata%/discord/` and press Enter.
4. Open the `settings.json` file in Notepad or your favorite text editor.
5. At the bottom of the file, add:
    ```json
    "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING": true
    ```
6. Save the file.
7. Reopen Discord.

### Getting the Token

1. **Open Developer Console**
    - Press `Ctrl + Shift + I` to open the Developer Tools and navigate to the `Console` tab.
		
2. **Paste the Code**
    - Enter this code in the Console:
      ```javascript
      (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
      ```
3. **Copy Your Token**
    - Copy the token (without `'`).

Now, you have your **Account Token**!
