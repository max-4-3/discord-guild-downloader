# How to Get Your *Discord* Account Token 🌟

---

## 🌐 Browser (Any)

First of all, open [discord.com](https://discord.com) and log into your account!

---

### 💻 Desktop

1. **Open Developer Console**  
   Press `Ctrl + Shift + J` to open the console.

2. **Paste the Code**  
   Enter this code in the Console:
   ```javascript
   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
   ```

3. **Copy Your Token**  
   Copy the token (without quotes).

---

### 📱 Android

1. **Open Chrome**  
   Open Chrome and go to: [Discord](https://discord.com/channels/@me)  
   Add this website as your bookmark (using the star icon at the top right).

2. **Modifying**  
   Click on the 3 dots -> Bookmarks -> Find the recently created bookmark (usually in `Mobile Bookmarks`).  
   Click on 3 dots again on the right side of the bookmark -> Edit.

3. **Editing**  
   Add these values:
   - **Name:**  
     `Discord`
   - **URL:**
     ```javascript
     javascript:(function(){webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m;const token=m.find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken();const blob=new Blob([token],{type:'text/plain'}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='token.txt';document.body.appendChild(link);link.click();document.body.removeChild(link);})();
     ```
   - Save Changes!

4. **Final**  
   Click on the Search Bar (on the Discord.com page) and type `Discord`.  
   Click on the Discord bookmark which has `/mobile bookmarks` below it instead of a URL.  
   Now, your token will be downloaded in `Downloads` as `token.txt`.

---

Now, you have your **Account Token**! 🎉

## 🧿 Discord App

**Note:** Not available for Android!

---

### Enabling Developer Tools

1. Quit Discord.
2. Press `Win + R` to open the Run dialog.
3. Type `%appdata%/discord/` and press Enter.
4. Open the `settings.json` file in Notepad or your favorite text editor.
5. At the bottom of the file, add:
   ```json
   "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING": true
   ```
6. Save the file.
7. Reopen Discord.

---

### Getting the Token

1. **Open Developer Console**  
   Press `Ctrl + Shift + I` to open the Developer Tools and navigate to the `Console` tab.

2. **Paste the Code**  
   Enter this code in the Console:
   ```javascript
   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
   ```

3. **Copy Your Token**  
   Copy the token (without quotes).

---

Now, you have your **Account Token**! 🚀

---
