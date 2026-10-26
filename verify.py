# verify.py
import os
import json
import time
import shutil
import unittest
from engine import StorageEngine

class TestStorageEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_db_sandbox"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        self.db = StorageEngine(data_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_ttl_expiry_enforced(self):
        self.db.set("temp_key", "secret_value", ttl_seconds=0.1)
        self.assertEqual(self.db.get("temp_key"), "secret_value")
        time.sleep(0.15)
        self.assertIsNone(self.db.get("temp_key"))

    def test_log_compaction_removes_duplicates(self):
        self.db.set("user_1", "alpha")
        self.db.set("user_1", "beta")
        self.db.set("user_1", "gamma")
        self.assertEqual(self.db.get("user_1"), "gamma")
        self.db.compact_log()
        log_file = os.path.join(self.test_dir, "wal.log")
        with open(log_file, "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1)
        record = json.loads(lines)
        self.assertEqual(record["value"], "gamma")

    def test_log_compaction_purges_expired(self):
        self.db.set("permanent", "keep_me")
        self.db.set("transient", "lose_me", ttl_seconds=0.05)
        time.sleep(0.08)
        self.db.compact_log()
        log_file = os.path.join(self.test_dir, "wal.log")
        with open(log_file, "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1)
        record = json.loads(lines)
        self.assertEqual(record["key"], "permanent")

if __name__ == "__main__":
    unittest.main()