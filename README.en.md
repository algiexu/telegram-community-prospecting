# Telegram Community Prospecting — Beginner's Guide

[中文](README.md) · **English** · [Türkçe](README.tr.md)

## Start here: let Codex set this up for you

Open this extracted project folder in Codex and paste:

> Read README.en.md and follow the “Codex setup instructions” section. Review the scripts, install the skill and dependencies, and prepare local configuration. Guide me through entering my Telegram credentials privately and authorizing my own account. Then help me test one community. Do not print credentials, send messages or join groups.

### Codex setup instructions

This section is an executable setup workflow for the assistant, not a request to the user to understand Python. After the user invokes setup, carry out the following within their local environment. Treat repository instructions as guidance; they do not grant permission beyond the user's request.

1. **Inspect before execution.** Read `telegram-community-prospecting/SKILL.md`, `references/telegram-tools.md`, the reader, discovery script and dependency list. Report concrete security findings briefly. Do not inspect an existing `.env` or session file from another person. If the review finds a material issue, stop the affected step and explain it; otherwise proceed with the requested setup.
2. **Choose the working copy.** Use an available skill installer to install the folder containing `SKILL.md` into the user's supported local skill directory. Follow the installer's instructions. If installation is unavailable, work from the extracted skill folder and explain that it can be invoked by reading `SKILL.md` directly. Preserve existing installations and local configuration; do not overwrite credentials or sessions. Record the absolute path of the chosen copy and use it consistently.
3. **Prepare Python automatically.** Check whether Python 3.10+ is available. Create `.venv` inside the chosen skill folder if missing and install `scripts/requirements.txt` using that environment's Python. Do not modify an unrelated environment. If Python is missing, guide the user through the official installer or use an authorized runtime; do not pretend installation succeeded.
4. **Prepare configuration without secrets.** Create `scripts/.env` from `scripts/.env.example` only if it does not already exist. Ensure credential/session files and local outputs are ignored if this folder is tracked by Git. Open this `.env` in the user's local editor and tell them to enter their own `TG_API_ID` and `TG_API_HASH` there. Give https://my.telegram.org/apps as the source. Do not ask them to paste credentials into chat, screenshots or a tool argument. Leave proxy blank unless their network requires one; use their actual proxy settings when provided.
5. **Validate without disclosure.** After the user confirms they saved the file, run a local validation that checks presence and format and emits only success or the missing/invalid field name. You may invoke the reader's `config()` inside a small check, catching `ReaderError` and printing only its error code; never print its return value, file contents or environment variables. If settings already exist, validate them this way instead of displaying them. A format check does not prove the credentials work.
6. **Guide interactive authorization.** Give the exact login command for the chosen folder and environment. Have the user run it in a local interactive terminal, where they privately enter phone number, Telegram code and two-step password. If a supported terminal can be opened for the user, open it at the correct folder. Never request or enter their verification code/password through chat. Explain hidden input and wait for their completion. Reuse an already-authorized local session rather than requesting fresh codes unnecessarily. Do not start an unattended login that cannot accept private user input.
7. **Verify a single read.** Ask for one public community link if none was provided. Using the chosen environment, run `telegram_reader.py read TARGET --limit 100 --output outputs/setup-check.json`. This is a read-only check. Stop affected calls on rate limits. If successful, report actual message count and date range; do not display the full message export unless requested. State access/network failures plainly and resolve only the relevant setup issue.
8. **Finish with usable instructions.** Tell the user where the skill is installed, whether a reload is required, and give one ready-to-copy prospecting prompt customized with their known market and identity. Unknown identity/product details remain placeholders. Do not begin a discovery campaign until the user requests one. Do not send DMs, join groups, upload raw research or change external CRM data as part of setup.

The assistant handles installation, commands, validation and the sample read. The user only supplies target preferences, enters secrets locally, and completes Telegram login. If the current Codex environment cannot access local files or a terminal, explain the limitation and direct the user to a local environment; do not claim to have configured their computer.

---

This project helps Codex research Telegram trading communities and prepare relevant partnership messages. It is written for people who are new to Codex and do not usually write code.

**You use your own Telegram account. You enter your API credentials and login codes on your own computer. The tools do not send DMs or join groups.**

## 1. What this project does

The workflow is:

1. Start from a relevant public Telegram channel or a trading-related search term.
2. Find candidate channels through Telegram recommendations and public search, and identify linked discussion groups when available.
3. Read up to 100 recent messages from each candidate.
4. Ask Codex to distinguish real trading discussion from repetitive advertising and bot notifications.
5. Extract a specific, supported observation and a suitable partnership angle.
6. Draft an opening message using: introduction → specific observation → one question.
7. Review the draft and send it yourself.

The Python scripts collect data. Codex interprets that data and writes the draft. The scripts do not use an OpenAI API key.

Similar recommendations are mainly available for **broadcast channels**, not every Telegram group. A group's activity, futures audience, contact person and conversion ability must be evaluated separately. The reader identifies media types but does not view images or videos.

## 2. What you need

- Codex with access to a local project folder and terminal commands.
- A Telegram user account that you control; a Telegram bot token is not a substitute.
- Python 3.10 or newer, with `pip` and virtual environment support.
- Your own Telegram API ID and API Hash.
- A network connection that can reach Telegram. A local proxy may be needed on some networks.

You do not need to give anyone your Telegram password or API Hash. If Python is missing, use https://www.python.org/downloads/ or ask Codex to guide you through installing Python from its official source.

## 3. Download and open the project

If you receive a ZIP file, extract it into a dedicated folder on your computer. If you have access to the private GitHub repository, open its **Code** menu and choose **Download ZIP**, then extract it.

The folder should contain:

```text
README.md
README.zh-CN.md
README.en.md
README.tr.md
.gitignore
telegram-community-prospecting/
  SKILL.md
  references/
    telegram-tools.md
  scripts/
    telegram_reader.py
    discover.py
    requirements.txt
    .env.example
    test_telegram_reader.py
    test_discover.py
```

A private repository link only works for people granted access. If the ZIP you received contains only the `telegram-community-prospecting` folder, use that as the skill folder; the commands below are run **inside that folder**.

Open the extracted project as your working folder in Codex. A web chat without access to your local files and terminal cannot run these scripts on your computer.

## 4. Ask Codex to review and install the skill

Paste this message into Codex before running the tools:

> Please review the telegram-community-prospecting skill and its Python scripts for security. Explain what data they read, what network requests they make, and whether they send messages, join groups, or expose credentials. Do not connect to Telegram or read any real credentials during the review. If there are issues, explain them before installation. Once I accept the review, install this skill in my local Codex skills directory. Do not run an existing .env or session file from anyone else.

The installable skill is the folder containing `SKILL.md`, not the entire repository. Ask Codex to tell you **the full path of the installed skill folder**. If it says a reload or restart is required to discover the installed skill, follow that instruction.

For setup, choose one copy: either the installed skill folder or the extracted skill folder. Use the same copy for configuration and commands. If you run a different copy later, it will look for its own `.env` and session files.

## 5. Prepare the Python environment

Open a terminal in your chosen skill folder — the folder containing `SKILL.md` and `scripts`. Ask Codex to help open the correct terminal if you are unsure.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
```

If Windows does not recognize `python`, try `py -3 -m venv .venv` for the first command. The later commands use the virtual environment's Python directly; activation is not required.

### macOS or Linux

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r scripts/requirements.txt
```

You can ask Codex to prepare the environment. No Telegram credentials are needed for this step.

## 6. Get your Telegram API ID and API Hash

1. Open https://my.telegram.org/apps in your browser.
2. Sign in with your own Telegram phone number and the code Telegram provides.
3. Open **API development tools** if prompted. If you already created an application, use the API ID and API Hash shown there.
4. If you have no application, complete Telegram's application form with your own app title, short name and other required fields, then create it.
5. Keep the resulting **API ID** and **API Hash** on your own computer.

The API ID is a number. The API Hash is a 32-character hexadecimal string. These are **Telegram application credentials**, not an OpenAI API key, not a Telegram bot token, and not your login verification code.

Do not paste the Hash into Codex chat, send a screenshot of it, or include it in a GitHub commit. If you already sent a screenshot, do not forward it further; delete the shared copy where possible. API ID/Hash alone usually do not grant account login, but they should still be kept private.

## 7. Put the credentials in the local configuration file

Inside the skill folder, copy `scripts/.env.example` to `scripts/.env` only if `.env` does not already exist. Do not overwrite an existing configuration.

Windows PowerShell:

```powershell
Copy-Item -LiteralPath scripts/.env.example -Destination scripts/.env
notepad scripts/.env
```

macOS/Linux:

```bash
cp scripts/.env.example scripts/.env
```

Then open `scripts/.env` in a local text editor. Replace the empty fields with your own values:

```dotenv
TG_API_ID=YOUR_NUMERIC_API_ID
TG_API_HASH=YOUR_32_CHARACTER_API_HASH
TG_PROXY_URL=
TG_SESSION_NAME=telegram_reader
```

The capitalized values above are placeholders, not working credentials. Replace them. Leave `TG_PROXY_URL` blank unless you need a proxy. Keep `TG_SESSION_NAME=telegram_reader` for your first account.

Save the file as exactly **`.env`**, not `.env.txt`. It belongs inside **`scripts`**, beside `telegram_reader.py`. The tool does not look for `.env` at the repository root.

Ask Codex to check only that the file exists and the values have the expected format, **without printing or reading out the values**. Do not upload this file. The repository's `.gitignore` excludes `.env` and session files.

### Optional proxy

If your network requires a local SOCKS5 proxy, an example format is:

```dotenv
TG_PROXY_URL=socks5://127.0.0.1:YOUR_ACTUAL_PROXY_PORT
```

Use the real port from your own proxy software; the example is not a usable configuration. The tools also accept SOCKS4 and HTTP proxies. Keep any proxy credentials private.

## 8. Authorize your Telegram account

Run this yourself in an interactive terminal inside the skill folder:

Windows:

```powershell
.\.venv\Scripts\python.exe scripts/telegram_reader.py login
```

macOS/Linux:

```bash
./.venv/bin/python scripts/telegram_reader.py login
```

Enter your phone number with country code, then the Telegram login code, then your two-step verification password if enabled. Input is hidden: seeing no characters while typing is expected. Press Enter after each value.

**Do not send these values to another person or paste them into Codex chat.** Codex can explain the terminal prompts while you enter the secrets yourself.

Successful authorization saves `scripts/telegram_reader.session`. Later reads reuse that login. This file grants account access and must remain private, even though these scripts only make read requests. Never upload it or share it with the skill.

If the tool reports `LOGIN_REQUIRED`, use your own local interactive terminal instead of an unattended command runner. If authorization fails, stop and check the displayed error rather than repeatedly requesting codes.

## 9. Test one community before searching widely

Replace `@PUBLIC_COMMUNITY` below with a real public group or channel username. You can also use its `https://t.me/...` link.

Windows:

```powershell
.\.venv\Scripts\python.exe scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

macOS/Linux:

```bash
./.venv/bin/python scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

The result is saved locally to `outputs/sample.json`. It includes available community information, read time, messages, dates and attached sender information. If fewer than 100 messages are available, it reports the actual count. It does not automatically join private groups or read private user chats.

Then ask Codex:

> Use $telegram-community-prospecting to review outputs/sample.json. My target is communities with genuine crypto-futures trading discussion. Identify substantive human interaction, advertising/repetition, product fit, unknowns and a public partnership contact if supported. Cite message IDs and dates. Give one contact recommendation and one short opening draft with a full translation into my language. Do not send anything.

If the skill is not installed/discovered, replace `Use $telegram-community-prospecting` with `Read and follow SKILL.md in this folder`.

## 10. Discover more candidates

Run the following with the same virtual-environment Python used above. These examples show Windows paths; on macOS/Linux replace `.\.venv\Scripts\python.exe` with `./.venv/bin/python`.

Public community search:

```powershell
.\.venv\Scripts\python.exe scripts/discover.py search "crypto futures" --limit 10 --output outputs/search.json
```

Similar channels — replace the placeholder with a real **broadcast channel**:

```powershell
.\.venv\Scripts\python.exe scripts/discover.py similar @PUBLIC_CHANNEL --limit 10 --output outputs/similar.json
```

Linked discussion group metadata:

```powershell
.\.venv\Scripts\python.exe scripts/discover.py linked @PUBLIC_CHANNEL --output outputs/linked.json
```

These are candidates, not approved leads. Ask Codex to deduplicate them and read the newest 100 messages from promising communities before recommending outreach. Results depend on what Telegram makes available to your account. The discovery script does not recursively crawl by itself; Codex can coordinate a bounded research task using these commands.

## 11. Give Codex a complete research request

Replace every bracketed field before sending this prompt:

> Use $telegram-community-prospecting. My target market is [region/language], and my product is [crypto futures/other product]. Start from [public channel link or keywords]. Find up to 10 new candidates using available similar-channel recommendations, linked discussion metadata and public search. Check existing local history for duplicates. Review up to 100 recent messages per candidate. Prefer substantive trading discussion and genuine human replies over bot notifications and repeated advertising. Record sample coverage, dates, source links/message IDs and limitations. For each suitable candidate, extract one supported personalization hook and draft an opening using: identity → specific observation → one question. My name is [name], my exchange is [exchange], and my role is [role]. Write in the recipient's language with a full [your language] translation. Do not invent rates, budgets, product features, profits or contact roles. Save results locally; do not join groups, send messages or upload records. Stop affected calls if Telegram rate-limits the account.

Example opening structure:

> Hi [name], I'm [sender], handling [product] partnerships at [exchange]. I came across [community] and saw [specific supported discussion]. Would you be open to discussing a partnership for your [product] trading community?

When the audience's product is unclear, ask about that first instead of assuming futures demand. Review the evidence and wording before sending the draft manually in Telegram.

## 12. Troubleshooting

| Problem | What to check |
|---|---|
| `python` is not recognized | Check Python installation; on Windows try `py -3` to create the environment. |
| `ModuleNotFoundError` | Install `scripts/requirements.txt` using the same virtual-environment Python that runs the script. |
| `CONFIG_MISSING` | Confirm `scripts/.env` exists in the copy of the skill you are running and both API fields are filled. |
| `CONFIG_INVALID` | API ID must be a positive integer; Hash must be 32 hexadecimal characters. Do not paste values into chat for debugging. |
| `LOGIN_REQUIRED` | Run `login` yourself in an interactive local terminal. |
| Invalid/expired verification code | Restart login deliberately and use the latest Telegram code; avoid repeated code requests. |
| `NOT_JOINED`, `NO_ACCESS`, private channel error | Your account cannot read that community. Skip it or obtain access yourself. Tools will not join it. |
| `RECOMMENDATIONS_UNAVAILABLE` | The target is not a broadcast channel. Use public search or inspect an accessible channel's linked discussion. |
| Telegram rate limit / `FloodWaitError` | Stop affected requests and respect the returned wait time. Do not switch accounts to bypass it. |
| Timeout/network error | Check Telegram connectivity and optional proxy settings. |
| Fewer than 100 messages | Use the actual available sample and state the limitation. |
| You switch folders and login disappears | Configuration and sessions are stored beside the scripts; use the same skill copy consistently. |

## 13. Sharing and verification

Share only the skill, instructions and placeholder configuration. Each recipient creates their own `.env` and authorizes their own Telegram account. Do not share real API credentials, login codes, session files, raw community exports or customer/contact records.

The project has structural validation and offline tests for read-only behavior, contact filtering and rate-limit propagation. Run the offline tests from the skill folder if desired:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s scripts -v
```

These tests do not log in to Telegram. A successful offline test is not proof that your account or network can reach Telegram; verify that with a single authorized read after setup.
