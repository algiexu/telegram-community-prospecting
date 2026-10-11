import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from telethon import types
import telegram_reader as reader


class ReaderTests(unittest.IsolatedAsyncioTestCase):
    def test_link_normalization_and_rejection(self):
        for value in ('@ExampleGroup', 'https://t.me/ExampleGroup/', 'https://t.me/s/ExampleGroup/42'):
            self.assertEqual(reader.parse_target(value), ('username', 'examplegroup'))
        self.assertEqual(reader.parse_target('https://t.me/+AbC_d-E'), ('invite', 'AbC_d-E'))
        self.assertEqual(reader.parse_target('https://t.me/c/123/42'), ('internal', 123))
        for value in ('https://evil.test/example', 'https://t.me/example/path', '@bad!'):
            with self.assertRaises(reader.ReaderError):
                reader.parse_target(value)

    async def test_invite_never_joins(self):
        client = AsyncMock(return_value=types.ChatInvite(title='Private', photo=types.PhotoEmpty(id=1), participants_count=2, color=0))
        with self.assertRaises(reader.ReaderError) as error:
            await reader.resolve(client, 'https://t.me/+AbC')
        self.assertEqual(error.exception.code, 'NOT_JOINED')
        self.assertEqual(type(client.call_args.args[0]).__name__, 'CheckChatInviteRequest')
        self.assertEqual(client.call_count, 1)

    async def test_private_user_rejected(self):
        client = SimpleNamespace(get_entity=AsyncMock(return_value=types.User(id=1)))
        with self.assertRaises(reader.ReaderError) as error:
            await reader.resolve(client, '@ExampleUser')
        self.assertEqual(error.exception.code, 'NOT_COMMUNITY')

    async def test_read_serializes_real_fields_and_no_mutations(self):
        entity = types.Channel(id=7, title='Community', photo=types.ChatPhotoEmpty(), date=datetime.now(timezone.utc), username='ExampleGroup')
        calls = []

        class ReadOnlyFake:
            async def get_entity(self, value):
                return entity

            async def __call__(self, request):
                calls.append(type(request).__name__)
                return SimpleNamespace(full_chat=SimpleNamespace(about='Description', participants_count=None))

            async def iter_messages(self, entity, limit):
                self.limit = limit
                yield types.Message(id=9, peer_id=types.PeerChannel(7), date=datetime.now(timezone.utc), message='Hello')

        client = ReadOnlyFake()
        result = await reader.read_community(client, '@ExampleGroup')
        self.assertEqual(client.limit, 200)
        self.assertEqual(calls, ['GetFullChannelRequest'])
        self.assertIsNone(result['community']['member_count'])
        self.assertIsNone(result['messages'][0]['sender'])
        self.assertEqual(result['messages'][0]['text'], 'Hello')
        self.assertEqual(result['message_count'], 1)

    def test_missing_config_does_not_leak(self):
        with patch('telegram_reader.dotenv_values', return_value={}):
            with self.assertRaises(reader.ReaderError) as error:
                reader.config()
        self.assertEqual(error.exception.code, 'CONFIG_MISSING')


if __name__ == '__main__':
    unittest.main()
