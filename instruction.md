\# Problem Specification: Key-Value Log Compaction \& TTL Engine

so we are tasked with enhancing a lightweight append-only key-value storage engine (`engine.py`). Currently, the system blindly appends data records to a log file but never clears out stale, expired keys or duplicate histories.



\# our Tasks to Implement:



1\. \*\*Enforce TTL Expiration on Reads (`get` method):\*\*

&#x20;  - Update `get(key)` to inspect the `expires\_at` timestamp.

&#x20;  - If the current system time (`time.time()`) is greater than or equal to `expires\_at`, consider the key dead.

&#x20;  - we must remove it from `self.memory\_index`, ensure `get` returns `None`, and ensure subsequent calls recognize it as deleted.



2\. \*\*Implement Log Compaction (`compact\_log` method):\*\*

&#x20;  - The engine needs to reclaim disk space by purging redundant transaction history from `wal.log`.

&#x20;  - When called, `compact\_log()` must read the current log entries, determine the single latest active value for each key, and filter out any keys that have already expired.

&#x20;  - we will Rewrite `wal.log` cleanly so that it contains exactly one line per active key, minimizing file footprint.

&#x20;  - If no valid keys exist, the log file should end up empty.



\### Structural Requirements:

\- we do not import external third-party libraries. Use standard `json`, `os`, and `time` modules.

\- we will Ensure proper file closing states using contexts (`with` statements) to prevent file system locking during updates.

\-

