# engine.py
import json
import os
import time

class StorageEngine:
    def __init__(self, data_dir="db_data"):
        self.data_dir = data_dir
        self.log_path = os.path.join(self.data_dir, "wal.log")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.memory_index = {}
        self._recover_index()

    def _recover_index(self):
        if not os.path.exists(self.log_path):
            return
        with open(self.log_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                key = record["key"]
                self.memory_index[key] = {
                    "value": record["value"],
                    "expires_at": record.get("expires_at")
                }

    def set(self, key, value, ttl_seconds=None):
        expires_at = None
        if ttl_seconds is not None:
            expires_at = time.time() + ttl_seconds

        record = {
            "key": key,
            "value": value,
            "expires_at": expires_at,
            "timestamp": time.time()
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(record) + "\n")

        self.memory_index[key] = {
            "value": value,
            "expires_at": expires_at
        }
        return True

    def get(self, key):
        if key not in self.memory_index:
            return None
        return self.memory_index[key]["value"]

    def compact_log(self):
        pass