#!/usr/bin/env python3
import sqlite3
import msgpack
import json

DB_PATH = ".data/langraph.sqlite"

def main(limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT thread_id, checkpoint_id, checkpoint FROM checkpoints ORDER BY ROWID DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()

    for thread_id, checkpoint_id, blob in rows:
        print(f"\n🧵 Thread ID: {thread_id}")
        print(f"🧠 Checkpoint: {checkpoint_id}")
        try:
            state = msgpack.unpackb(blob, raw=False)
            # just pretty-print the state JSON
            print(json.dumps(state, indent=2, default=str))
        except Exception as e:
            print("❌ Failed to decode:", e)

    conn.close()

if __name__ == "__main__":
    main()
