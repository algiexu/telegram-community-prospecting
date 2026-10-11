"""On-demand Telegram user-account reader. No chat mutations or read receipts."""
import argparse
import asyncio
import getpass
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, unquote

from dotenv import dotenv_values
from telethon import TelegramClient, errors, functions, types, utils
from telethon.network.connection import ConnectionTcpObfuscated

ROOT = Path(__file__).resolve().parent


class ReaderError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def parse_target(value):
    value = value.strip()
    if value.startswith('@'):
        value = value[1:]
    if '://' not in value and '/' not in value:
        if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{3,31}', value):
            return 'username', value.lower()
        raise ReaderError('INVALID_TARGET', '请提供群组/频道的 @username 或 t.me 链接。')
    if value.startswith('t.me/'):
        value = 'https://' + value
    u = urlparse(value)
    if u.scheme not in ('https', 'http') or u.netloc.lower() not in ('t.me', 'telegram.me', 'www.t.me'):
        raise ReaderError('INVALID_TARGET', '只接受 Telegram 群组/频道链接。')
    parts = u.path.strip('/').split('/')
    if parts[0].startswith('+') or parts[0] == 'joinchat':
        invite = parts[0][1:] if parts[0].startswith('+') else (parts[1] if len(parts) == 2 else '')
        if not re.fullmatch(r'[A-Za-z0-9_-]+', invite):
            raise ReaderError('INVALID_TARGET', '邀请链接格式无效。')
        return 'invite', invite
    if parts[0] == 'c' and len(parts) in (2, 3, 4) and all(p.isdigit() for p in parts[1:]):
        return 'internal', int(parts[1])
    if parts[0] == 's':
        parts = parts[1:]
    if parts and len(parts) <= 3 and all(p.isdigit() for p in parts[1:]):
        return parse_target('@' + parts[0])
    raise ReaderError('INVALID_TARGET', '无法解析这个 Telegram 链接。')


def config():
    values = dotenv_values(ROOT / '.env')
    api_id, api_hash = values.get('TG_API_ID', ''), values.get('TG_API_HASH', '')
    if not api_id or not api_hash:
        raise ReaderError('CONFIG_MISSING', '请在项目 .env 中填写 TG_API_ID 和 TG_API_HASH。')
    if not str(api_id).isdigit() or int(api_id) <= 0 or not re.fullmatch(r'[a-fA-F0-9]{32}', api_hash):
        raise ReaderError('CONFIG_INVALID', 'TG_API_ID 应为正整数，TG_API_HASH 应为 32 位十六进制字符串。')
    return int(api_id), api_hash


def session_path():
    name = dotenv_values(ROOT / '.env').get('TG_SESSION_NAME') or 'telegram_reader'
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}', name):
        raise ReaderError('SESSION_INVALID', 'TG_SESSION_NAME 只能是字母开头的简单文件名。')
    return ROOT / f'{name}.session'


def proxy_config():
    value = dotenv_values(ROOT / '.env').get('TG_PROXY_URL')
    if not value:
        return None
    try:
        proxy = urlparse(value)
        if proxy.scheme not in ('socks5', 'socks4', 'http') or not proxy.hostname or not proxy.port:
            raise ValueError()
        return {'proxy_type': proxy.scheme, 'addr': proxy.hostname, 'port': proxy.port,
                'rdns': True, 'username': unquote(proxy.username) if proxy.username else None,
                'password': unquote(proxy.password) if proxy.password else None}
    except ValueError:
        raise ReaderError('PROXY_INVALID', 'TG_PROXY_URL 格式无效；示例 socks5://127.0.0.1:7892。') from None


async def authorize(client):
    if await asyncio.wait_for(client.is_user_authorized(), timeout=25):
        return
    if not sys.stdin.isatty():
        raise ReaderError('LOGIN_REQUIRED', '尚未登录；请在本机交互终端运行 telegram_reader.py login。')
    phone = getpass.getpass('Telegram 手机号（含国家代码；输入隐藏）: ')
    if not re.fullmatch(r'\+[0-9]{6,15}', phone):
        raise ReaderError('PHONE_INVALID', '请输入含国家代码的手机号，例如 +86...。')
    sent = await client.send_code_request(phone)
    code = getpass.getpass('Telegram 验证码（输入隐藏）: ')
    try:
        await client.sign_in(phone, code, phone_code_hash=sent.phone_code_hash)
    except errors.SessionPasswordNeededError:
        await client.sign_in(password=getpass.getpass('Telegram 两步验证密码（输入隐藏）: '))


async def resolve(client, target):
    kind, value = parse_target(target)
    if kind == 'invite':
        result = await client(functions.messages.CheckChatInviteRequest(value))
        if not isinstance(result, types.ChatInviteAlready):
            raise ReaderError('NOT_JOINED', '此账号尚未加入该邀请群；只读模式不会自动加群。')
        entity = result.chat
    elif kind == 'internal':
        entity = None
        async for dialog in client.iter_dialogs():
            if dialog.entity.id == value and isinstance(dialog.entity, types.Channel):
                entity = dialog.entity
                break
        if entity is None:
            raise ReaderError('NO_ACCESS', '当前账号的会话列表中找不到此内部群 ID。')
    else:
        entity = await client.get_entity(value)
    if not isinstance(entity, (types.Channel, types.Chat)):
        raise ReaderError('NOT_COMMUNITY', '目标不是群组或频道，不读取用户私聊。')
    return entity


def identity(sender):
    if sender is None:
        return None
    return {
        'id': utils.get_peer_id(sender),
        'type': type(sender).__name__,
        'username': getattr(sender, 'username', None),
        'display_name': utils.get_display_name(sender),
        'is_bot': getattr(sender, 'bot', None),
    }


async def read_community(client, target, limit=200):
    entity = await resolve(client, target)
    warnings = []
    about, count = None, None
    try:
        if isinstance(entity, types.Channel):
            full = (await client(functions.channels.GetFullChannelRequest(entity))).full_chat
        else:
            full = (await client(functions.messages.GetFullChatRequest(entity.id))).full_chat
        about = getattr(full, 'about', None)
        count = getattr(full, 'participants_count', None)
        participants = getattr(full, 'participants', None)
        if count is None and isinstance(participants, types.ChatParticipants):
            count = len(participants.participants)
    except errors.RPCError as exc:
        if isinstance(exc, errors.FloodWaitError):
            raise
        warnings.append({'code': type(exc).__name__, 'message': '简介/成员数读取失败，保留空值。'})
    messages = []
    async for msg in client.iter_messages(entity, limit=limit):
        # Use attached entity data; do not enumerate users or fetch phone numbers.
        messages.append({
            'id': msg.id,
            'date': msg.date.astimezone(timezone.utc).isoformat() if msg.date else None,
            'edit_date': msg.edit_date.astimezone(timezone.utc).isoformat() if msg.edit_date else None,
            'text': msg.message or '',
            'sender_id': msg.sender_id,
            'sender': identity(msg.sender),
            'post_author': getattr(msg, 'post_author', None),
            'media_type': type(msg.media).__name__ if getattr(msg, 'media', None) else None,
            'service_action': type(msg.action).__name__ if getattr(msg, 'action', None) else None,
            'reply_to_message_id': msg.reply_to_msg_id,
        })
    username = getattr(entity, 'username', None)
    return {
        'ok': True, 'read_at': datetime.now(timezone.utc).isoformat(),
        'community': {'id': utils.get_peer_id(entity), 'name': entity.title,
                      'username': username, 'tg_link': f'https://t.me/{username}' if username else None,
                      'description': about, 'member_count': count},
        'requested_limit': limit, 'message_count': len(messages),
        'order': 'newest_first', 'timezone': 'UTC', 'warnings': warnings, 'messages': messages,
    }


def failure(exc):
    if isinstance(exc, ReaderError):
        return {'ok': False, 'error': {'code': exc.code, 'message': exc.message}}
    messages = {
        'ApiIdInvalidError': 'Telegram API ID/HASH 无效。',
        'PhoneCodeInvalidError': '登录验证码错误，请重新登录。',
        'PhoneCodeExpiredError': '登录验证码已过期，请重新登录。',
        'PasswordHashInvalidError': '两步验证密码错误。',
        'PhoneNumberBannedError': 'Telegram 已限制此手机号。',
        'PhoneNumberInvalidError': '手机号无效。',
        'ChannelPrivateError': '此群为私有群、账号无权访问或已被封禁。',
        'ChatAdminRequiredError': '此操作需要管理员权限。',
        'UsernameNotOccupiedError': '该用户名不存在。',
        'UsernameInvalidError': '该用户名无效。',
        'InviteHashExpiredError': '邀请链接已过期或被撤销。',
        'InviteHashInvalidError': '邀请链接无效。',
        'AuthKeyUnregisteredError': '会话失效，请重新登录。',
        'SessionRevokedError': '会话已被撤销，请重新登录。',
    }
    name = type(exc).__name__
    if isinstance(exc, errors.FloodWaitError):
        message = f'Telegram 限流，请至少等待 {exc.seconds} 秒后重试。'
    elif isinstance(exc, (TimeoutError, ConnectionError, OSError)):
        message = '网络或本地文件操作失败，请检查 Telegram 网络连通性及文件权限。'
    else:
        message = messages.get(name, '读取未完成；请按错误类型排查，未返回推测数据。')
    return {'ok': False, 'error': {'code': name, 'message': message}}


async def run(args):
    api_id, api_hash = config()
    if args.command == 'read':
        parse_target(args.target)
    client = TelegramClient(str(session_path()), api_id, api_hash,
                            connection=ConnectionTcpObfuscated,
                            proxy=proxy_config(),
                            receive_updates=False, flood_sleep_threshold=0,
                            request_retries=1, connection_retries=1, timeout=15)
    try:
        print('正在连接 Telegram…', file=sys.stderr, flush=True)
        await asyncio.wait_for(client.connect(), timeout=30)
        print('连接成功，正在检查账号授权…', file=sys.stderr, flush=True)
        await authorize(client)
        me = await asyncio.wait_for(client.get_me(), timeout=25)
        if me.bot:
            raise ReaderError('USER_ACCOUNT_REQUIRED', '需要 Telegram 用户账号，不能使用 Bot 会话。')
        if args.command == 'login':
            return {'ok': True, 'authorized': True, 'account': identity(me)}
        return await asyncio.wait_for(read_community(client, args.target, args.limit), timeout=120)
    finally:
        try:
            await asyncio.wait_for(client.disconnect(), timeout=5)
        except TimeoutError:
            pass


def main():
    parser = argparse.ArgumentParser(description='Telegram 只读社区 Reader')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('login', help='首次授权或检查登录状态')
    read = sub.add_parser('read', help='读取有权访问的群组/频道')
    read.add_argument('target')
    read.add_argument('--limit', type=int, choices=range(1, 201), default=200, metavar='1..200')
    read.add_argument('--output', type=Path, help='保存 JSON 文件；省略时输出到终端')
    args = parser.parse_args()
    try:
        result = asyncio.run(run(args))
        content = json.dumps(result, ensure_ascii=False, indent=2)
        if getattr(args, 'output', None):
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content + '\n', encoding='utf-8')
            print(json.dumps({'ok': True, 'output': str(args.output.resolve()),
                              'message_count': result['message_count']}, ensure_ascii=False))
        else:
            print(content)
    except (KeyboardInterrupt, EOFError):
        print(json.dumps(failure(ReaderError('CANCELLED', '登录或读取已取消。')), ensure_ascii=False), file=sys.stderr)
        return 1
    except Exception as exc:
        print(json.dumps(failure(exc), ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
