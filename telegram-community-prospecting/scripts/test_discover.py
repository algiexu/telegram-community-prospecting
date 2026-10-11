import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from telethon import types, functions, errors
import discover


def channel(broadcast=True):
    return types.Channel(id=42, title='Example', photo=types.ChatPhotoEmpty(),
                         date=datetime.now(timezone.utc), username='ExampleChannel',
                         broadcast=broadcast, megagroup=not broadcast)


class DiscoveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_similar_calls_only_recommendation_and_deduplicates(self):
        entity = channel()
        client = AsyncMock(return_value=SimpleNamespace(chats=[entity, entity]))
        args = SimpleNamespace(command='similar', target='@ExampleChannel', limit=10)
        with patch.object(discover, 'resolve', AsyncMock(return_value=entity)):
            result = await discover.discover(client, args)
        self.assertEqual(len(result['candidates']), 1)
        self.assertEqual(client.call_count, 1)
        self.assertIsInstance(client.call_args.args[0], functions.channels.GetChannelRecommendationsRequest)

    async def test_group_does_not_trigger_recommendations(self):
        client = AsyncMock()
        args = SimpleNamespace(command='similar', target='@ExampleGroup', limit=10)
        with patch.object(discover, 'resolve', AsyncMock(return_value=channel(False))):
            with self.assertRaises(discover.ReaderError):
                await discover.discover(client, args)
        client.assert_not_called()

    async def test_search_excludes_users(self):
        entity = channel()
        client = AsyncMock(return_value=SimpleNamespace(chats=[entity, types.User(id=9)]))
        result = await discover.discover(client, SimpleNamespace(command='search', target='trading', limit=5))
        self.assertEqual(len(result['candidates']), 1)
        self.assertIsInstance(client.call_args.args[0], functions.contacts.SearchRequest)

    async def test_rate_limit_propagates_without_retry(self):
        client = AsyncMock(side_effect=errors.FloodWaitError(request=None, capture=60))
        with self.assertRaises(errors.FloodWaitError):
            await discover.discover(client, SimpleNamespace(command='search', target='trading', limit=5))
        self.assertEqual(client.call_count, 1)


if __name__ == '__main__':
    unittest.main()
