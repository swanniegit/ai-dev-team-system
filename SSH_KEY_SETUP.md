# SSH Key Setup for GitHub

This guide explains how to generate SSH keys, add them to GitHub, and configure your repository for secure access.

---

## 1. Check for Existing SSH Keys

Open a terminal and run:

```sh
ls ~/.ssh
```
If you see `id_rsa` and `id_rsa.pub`, you already have SSH keys. If not, proceed to generate them.

---

## 2. Generate a New SSH Key Pair

Run the following command and follow the prompts (press Enter to accept defaults):

```sh
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
- When asked for a file location, press Enter to use the default.
- You may set a passphrase for extra security (optional).

---

## 3. Add Your SSH Key to the SSH Agent

Start the SSH agent and add your key:

```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

---

## 4. Copy the Public Key

Copy your public key to the clipboard:

- **Linux/macOS:**
  ```sh
  cat ~/.ssh/id_rsa.pub | pbcopy  # macOS
  cat ~/.ssh/id_rsa.pub | xclip   # Linux (requires xclip)
  ```
- **Windows (PowerShell):**
  ```powershell
  Get-Content $env:USERPROFILE\.ssh\id_rsa.pub | Set-Clipboard
  ```
- Or open the file and copy manually:
  ```sh
  cat ~/.ssh/id_rsa.pub
  ```

---

## 5. Add the SSH Key to GitHub

1. Go to [GitHub SSH Keys](https://github.com/settings/keys)
2. Click **New SSH key**
3. Give it a descriptive title (e.g., "Work Laptop")
4. Paste your public key into the **Key** field
5. Click **Add SSH key**

---

## 6. Test Your SSH Connection

Run:

```sh
ssh -T git@github.com
```
You should see a success message ("Hi <username>! You've successfully authenticated...").

---

## 7. Set Your Git Remote to Use SSH

If your repo uses HTTPS, switch to SSH:

```sh
git remote set-url origin git@github.com:swanniegit/ai-dev-team-system.git
```

---

## Troubleshooting
- If you get permission errors, ensure your public key is added to GitHub and your private key is loaded in the SSH agent.
- For more help, see: [GitHub SSH Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

## Automated Script (Optional)
You can use the provided script:

```sh
scripts/setup_ssh_keys.bat   # Windows
# or
powershell -ExecutionPolicy Bypass -File scripts/setup_ssh_keys.ps1
```

This will generate keys and print instructions for adding them to GitHub. 