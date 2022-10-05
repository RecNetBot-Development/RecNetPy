"""
This is reserved for manager unit tests.
Test function names resemble their manager counterparts with a "test_" prefix.
"""

import unittest
from src import Client
from src.rest.exceptions import BadRequest

"""
Unit tests for the AccountManager
"""
class AccountManagerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.rec_net = Client()
        self.test_data = {
            "names": {
                "existing": ["Coach", 1, False],
                "fake": "ä",
            },
            "ids": {
                "existing": [1, "1"],
                "fake": 3,
                "invalid": [-1, "bruh"]
            }
        }
        
    async def test_get(self):
        existing = self.test_data["names"]["existing"]
        fake = self.test_data["names"]["fake"]
        
        # Check existing accounts
        for name in existing:
            user = await self.rec_net.accounts.get(name)
            self.assertEqual(str(name).lower(), user.username.lower(), "Should be the same username")
            
        # Check non-existant accounts
        user = await self.rec_net.accounts.get(fake)
        self.assertIsNone(user, "Shouldn't exist")
        
    async def test_get_many(self):
        existing = self.test_data["names"]["existing"]
        fake = self.test_data["names"]["fake"]
        
        # Check bulk and if it excludes non-existent accounts
        bulk = [fake] + existing
        user_bulk = await self.rec_net.accounts.get_many(bulk)
        self.assertEqual(len(existing), len(user_bulk), "Should exclude non-existent account")

    async def test_fetch(self):
        existing = self.test_data["ids"]["existing"]
        fake = self.test_data["ids"]["fake"]
        invalid = self.test_data["ids"]["invalid"]
        
        # Check existing accounts
        for id in existing:
            user = await self.rec_net.accounts.fetch(id)
            self.assertEqual(int(id), user.id, "Should be the same id")
            
        # Check non-existant accounts
        user = await self.rec_net.accounts.fetch(fake)
        self.assertIsNone(user, "Shouldn't exist")
        
        # Check invalid inputs
        for data in invalid:
            with self.assertRaises(BadRequest):
                user = await self.rec_net.accounts.fetch(data)
        
    async def test_search(self):
        fake = self.test_data["names"]["fake"]
        existing = self.test_data["names"]["existing"]
        
        # Check if it finds accounts
        for query in existing:
            search = await self.rec_net.accounts.search(query)
            self.assertTrue(search)
            
        # Check if it doesn't find fake accounts
        search = await self.rec_net.accounts.search(fake)
        self.assertFalse(search)
        
    async def asyncTearDown(self):
        await self.rec_net.close()
        
        
"""
Unit tests for the EventManager
"""        
class EventManagerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.rec_net = Client()
        self.test_data = {}
        
    async def test_fetch(self):
        ...
        
    async def test_fetch_many(self):
        ...
        
    async def test_search(self):
        ...
        
    async def test_from_account(self):
        ...
        
    async def test_in_room(self):
        ...
        
    async def test_get_events(self):
        ...
        
    async def asyncTearDown(self):
        await self.rec_net.close()
      
        
"""
Unit tests for the ImageManager
"""
class ImageManagerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.rec_net = Client()
        self.test_data = {}
        
    async def test_fetch(self):
        ...
        
    async def test_fetch_many(self):
        ...
        
    async def test_from_account(self):
        ...
        
    async def test_player_feed(self):
        ...
        
    async def test_during_event(self):
        ...
        
    async def test_in_room(self):
        ...
        
    async def test_front_page(self):
        ...
        
    async def asyncTearDown(self):
        await self.rec_net.close()
        
        
"""
Unit tests for the InventionManager
"""
class InventionManagerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.rec_net = Client()
        self.test_data = {}
        
    async def test_fetch(self):
        ...
        
    async def test_search(self):
        ...
    
    async def test_featured(self):
        ...
        
    async def test_top_today(self):
        ...
    
    async def asyncTearDown(self):
        await self.rec_net.close()    

    
"""
Unit tests for the RoomManager
"""
class RoomManagerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.rec_net = Client()
        self.test_data = {}
        
    async def test_fetch(self):
        ...
        
    async def test_get_many(self):
        ...
        
    async def test_fetch_many(self):
        ...
        
    async def test_search(self):
        ...
        
    async def test_created_by(self):
        ...
        
    async def test_owned_by(self):
        ...
        
    async def test_hot(self):
        ...
        
    async def asyncTearDown(self):
        await self.rec_net.close()


if __name__ == "__main__":
    unittest.main()