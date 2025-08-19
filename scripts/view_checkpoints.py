import sqlite3
import msgpack
from app.config.settings import settings

DB_PATH = settings.LANGRAPH_DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Step 1: Get latest checkpoint_id per thread
cursor.execute("""
    SELECT thread_id, MAX(checkpoint_id) as checkpoint_id
    FROM checkpoints
    GROUP BY thread_id
""")
latest_ids = cursor.fetchall()

# Step 2: Fetch actual checkpoint blobs
checkpoints = []
for thread_id, checkpoint_id in latest_ids:
    cursor.execute("SELECT checkpoint FROM checkpoints WHERE checkpoint_id = ?", (checkpoint_id,))
    row = cursor.fetchone()
    if row:
        blob = row[0]
        checkpoints.append((thread_id, checkpoint_id, row[0]))

print(f"🧠 Found {len(checkpoints)} latest checkpoints (1 per thread)\n")

# Mapping for pretty thread type names
thread_type_map = {
    "company_profile": "company",
    "product": "product",
    "service": "service"
}

# Step 3: Decode and print state
for thread_id, checkpoint_id, blob in checkpoints:
    try:
        data = msgpack.unpackb(blob, raw=False)
        values = data.get("channel_values", {})

        # Flatten __start__ if present
        if "__start__" in values:
            values.update(values.pop("__start__"))

        print(f"🧵 Thread ID: {thread_id}")
        print(f"🆔 Checkpoint ID: {checkpoint_id}")
        print("📦 State Summary:")

        summary_keys = ["user_id", "company_id", "module", "stage", "step", "next_action", "messages"]
        for key in summary_keys:
            if key in values:
                val = values[key]
                if key == "messages":
                    print(f"   🗨️ Messages: {len(val)}")
                    for i, m in enumerate(val[-2:], 1):
                        print(f"     {i}. [{m.get('role')}] {m.get('content')[:80]}...")
                else:
                    print(f"   {key}: {val}")

        # Extract and map thread type from context
        context = values.get("context", {})
        thread_type = values.get("thread_type", "unknown")   # ✅ Correct!

        print("   Context:")
        for k, v in context.items():
         print(f"     {k}: {v}")
        print(f"   thread_type: {thread_type}")

        print("=" * 80)

    except Exception as e:
        print(f"❌ Failed to decode checkpoint {checkpoint_id}: {e}")
