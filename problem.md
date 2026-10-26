# Problem Benchmark: Persistent Key-Value Storage Log Compaction & TTL Isolation Engine

### 1. Application Context & Problem Scenario
In system engineering, fast data ingestion is often achieved using an append-only Write-Ahead Log (WAL). Every transaction (insert, update, delete) is appended sequentially to the end of a log file on disk to guarantee durability with low runtime overhead. However, this architectural design naturally causes continuous file size inflation because old, redundant data updates and dead records are preserved indefinitely. 

To prevent disk saturation and ensure data accuracy, storage systems must execute background performance routines. This benchmark requires an autonomous AI engineer to upgrade an incomplete, basic persistent log storage script (`engine.py`) by adding automatic time-based record eviction and transactional file volume reduction features.

### 2. Codebase Architecture & Technical Gaps
The base implementation provides basic setup routines: directory creation, sequential record serialization to `wal.log`, and an internal database startup index recovery hook. The system has two distinct code gaps marked with `TODO` strings and placeholder `pass` keywords inside the entry point class `StorageEngine`:

* **Task 1: Time-To-Live (TTL) Eviction Strategy (`get` method)**
  - Modify the public retrieval method `get(key)`.
  - The script must read the record's metadata from memory and compare the active host platform runtime epoch time (`time.time()`) directly against the record's tracking timestamp boundary (`expires_at`).
  - If the current execution time is greater than or equal to the designated expiration time, the engine must immediately clean up the stale key reference from the memory map index (`self.memory_index`) and return `None`.

* **Task 2: Transaction Log Compaction Mechanics (`compact_log` method)**
  - Implement the internal structural logic for the `compact_log()` routine.
  - The engine must read the existing `wal.log` file from start to finish, tracking updates sequentially to identify the single latest data payload value for each unique key string.
  - It must filter out and discard all duplicate transaction history entries and any keys that have already expired based on the current execution system clock.
  - The engine must cleanly truncate and rewrite the physical `wal.log` file so it contains exactly one single structured line per active key, minimizing the physical disk space footprint.
  - The engine's active in-memory dictionary index tracking mapping (`self.memory_index`) must be fully re-synchronized with the newly compressed log file data.

### 3. Strict Quality & Evaluation Constraints
- **Standard Library Isolation:** The environment blocks third-party dependency installations. All code updates must be executed using native, standard Python packages (`json`, `os`, `time`, `shutil`) only.
- **Resource Sanitation:** The solution must use clean context manager scopes (`with` blocks) during file reading, truncating, and writing operations to guard against resource deadlocks and background file access locking.
- **Objective Testing Pipeline:** The code is automatically checked against a hidden validation script (`verify.py`) running in a dedicated filesystem path sandbox (`test_db_sandbox`). It tests the logic using randomized key access, high-frequency duplicate logs, and near-instant token lifecycles to calculate a strict, objective true/false pass rate.
-
