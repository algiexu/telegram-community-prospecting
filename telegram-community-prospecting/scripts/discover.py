"""Read-only public community discovery; never joins or messages."""
import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from telethon import TelegramClient, functions, types, utils
from telethon.network.connection import ConnectionTcpObfuscated
from telegram_reader import authorize, config, failure, proxy_config, resolve, session_path, ReaderError


def community(entity):
    username = getattr(entity, 'username', None)
    return {'id': utils.get_peer_id(entity), 'name': getattr(entity, 'title', None),
            'username': username, 'tg_link': f'https://t.me/{username}' if username else None,
            'broadcast': getattr(entity, 'broadcast', False),
            'megagroup': getattr(entity, 'megagroup', False)}


async def discover(client, args):
    if args.command == 'search':
        result = await client(functions.contacts.SearchRequest(q=args.target, limit=args.limit))
        chats = [e for e in result.chats if isinstance(e, (types.Channel, types.Chat))]
    else:
        entity = await resolve(client, args.target)
        if args.command == 'similar':
            if not isinstance(entity, types.Channel) or not entity.broadcast:
                raise ReaderError('RECOMMENDATIONS_UNAVAILABLE', 'Similar recommendations require a broadcast channel; use search or a linked discussion group.')
            result = await client(functions.channels.GetChannelRecommendationsRequest(channel=entity))
            chats = result.chats
        else:
            if not isinstance(entity, types.Channel):
                raise ReaderError('NOT_CHANNEL', 'Linked discussions require a channel entity.')
            result = await client(functions.channels.GetFullChannelRequest(entity))
            linked_id = getattr(result.full_chat, 'linked_chat_id', None)
            chats = [e for e in result.chats if e.id == linked_id]
    seen, items = set(), []
    for entity in chats:
        if not isinstance(entity, (types.Channel, types.Chat)):
            continue
        item = community(entity)
        if item['id'] not in seen:
            seen.add(item['id'])
            items.append(item)
    return {'ok': True, 'read_at': datetime.now(timezone.utc).isoformat(),
            'source': {'method': args.command, 'target': args.target},
            'candidates': items[:args.limit]}


async def run(args):
    api_id, api_hash = config()
    client = TelegramClient(str(session_path()), api_id, api_hash,
                            connection=ConnectionTcpObfuscated, proxy=proxy_config(),
                            receive_updates=False, flood_sleep_threshold=0,
                            request_retries=1, connection_retries=1, timeout=15)
    try:
        await asyncio.wait_for(client.connect(), timeout=30)
        await authorize(client)
        me = await asyncio.wait_for(client.get_me(), timeout=25)
        if me.bot:
            raise ReaderError('USER_ACCOUNT_REQUIRED', 'Use a Telegram user session, not a bot account.')
        return await asyncio.wait_for(discover(client, args), timeout=90)
    finally:
        try:
            await asyncio.wait_for(client.disconnect(), timeout=5)
        except TimeoutError:
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('search', 'similar', 'linked'))
    parser.add_argument('target')
    parser.add_argument('--limit', type=int, choices=range(1, 51), default=10)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = asyncio.run(run(args))
        content = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content + '\n', encoding='utf-8')
            print(json.dumps({'ok': True, 'output': str(args.output.resolve()),
                              'candidate_count': len(result['candidates'])}))
        else:
            print(content)
        return 0
    except (KeyboardInterrupt, EOFError):
        print(json.dumps({'ok': False, 'error': {'code': 'CANCELLED'}}, ensure_ascii=False), file=sys.stderr)
        return 1
    except Exception as exc:
        print(json.dumps(failure(exc), ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
