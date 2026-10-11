# Local Telegram tools

Use Python 3.10+ and a Telegram user account. Paths below are relative to this skill folder. Commands are usable in PowerShell and a standard terminal when `python` resolves to the chosen Python environment.

```text
python -m pip install -r scripts/requirements.txt
```

Get your own API ID and API Hash at https://my.telegram.org/apps. Copy `scripts/.env.example` to `scripts/.env` locally and fill the fields. The script resolves configuration beside itself, not in the current working directory. Never send API Hash, login codes, passwords or session files to the model/chat or commit them. Run interactive login yourself:

```text
python scripts/telegram_reader.py login
```

Read recent messages:

```text
python scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

Public usernames/posts, accessible internal links and already-joined invitation links are supported. Private/unjoined groups require access obtained by the user; tools never join them. Outputs contain message text, dates, available attached sender data and media types. They do not download media, infer hidden authors or prove administrator roles.

Discover public search results:

```text
python scripts/discover.py search "crypto futures" --limit 10 --output outputs/search.json
```

Get recommended channels and linked discussion metadata:

```text
python scripts/discover.py similar @PUBLIC_CHANNEL --limit 10 --output outputs/similar.json
python scripts/discover.py linked @PUBLIC_CHANNEL --output outputs/linked.json
```

Similar recommendations use Telegram's `channels.getChannelRecommendations`, only for broadcast channels. Results depend on Telegram/account availability and are not a complete inventory. Search returns only community entities, not private user contacts. Linked metadata is a lead, not proof of read permission or an instruction to join.

Each discovery output records UTC read time and discovery source. Follow recommendations selectively, deduplicate IDs/usernames, then use `read --limit 100` to evaluate content. Do not automatically recursively crawl indefinitely. A rate limit returns an error and exits; stop related calls.

Optional proxy: set `TG_PROXY_URL` locally to an HTTP/SOCKS proxy URL. Keep any proxy credentials local. Session files retain Telegram account access; the tools' read-only behavior is implemented by limiting calls, not by issuing a read-only account token.
