#!/usr/bin/env python3
import sqlite3
import msgpack
import json
from typing import Any, Dict, List, Optional

DB_PATH = ".data/langraph.sqlite"

def _truncate(text: str, n: int = 140) -> str:
    if text is None:
        return ""
    text = str(text).strip()
    return text if len(text) <= n else text[: n - 1] + "…"

def _summarize_messages(raw: Any) -> Dict[str, Any]:
    """
    Return only high-signal info about messages:
    - total count
    - last human preview (if available)
    - last assistant preview (if available)
    We avoid importing LangChain classes; handle dicts or generic shapes.
    """
    msgs: List[Any] = raw if isinstance(raw, list) else []
    out: Dict[str, Any] = {"count": len(msgs)}

    # Try to extract previews if items look like dicts {"role","content"}
    def _role_and_content(m: Any) -> Optional[Dict[str, str]]:
        # dict shape
        if isinstance(m, dict):
            role = m.get("role") or m.get("type")
            content = m.get("content")
            if isinstance(content, (str, int, float)):
                return {"role": str(role), "content": str(content)}
        # LangChain BaseMessage-like (duck typed)
        if hasattr(m, "type") and hasattr(m, "content"):
            try:
                return {"role": str(getattr(m, "type")), "content": str(getattr(m, "content"))}
            except Exception:
                pass
        # Stored as pair [<ver>, <payload>] from some checkpoint writers
        if isinstance(m, list) and len(m) == 2 and isinstance(m[1], str):
            # Not decoding binary payloads; just mark as packed
            return {"role": "packed", "content": "<binary message payload>"}
        return None

    last_human = None
    last_ai = None
    for m in msgs:
        rc = _role_and_content(m)
        if not rc:
            continue
        role = (rc.get("role") or "").lower()
        if role in ("human", "user"):
            last_human = _truncate(rc.get("content", ""))
        elif role in ("ai", "assistant", "bot"):
            last_ai = _truncate(rc.get("content", ""))

    if last_human:
        out["last_human"] = last_human
    if last_ai:
        out["last_assistant"] = last_ai

    # If everything looked binary/opaque, keep it minimal.
    if "last_human" not in out and "last_assistant" not in out and len(msgs) > 0:
        out["note"] = "messages are packed/opaque; previews unavailable"

    return out

def _clean_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reduce the raw checkpoint to the bits you actually care about.
    """
    cv = state.get("channel_values", {}) if isinstance(state, dict) else {}
    context = cv.get("context", {}) if isinstance(cv, dict) else {}

    cleaned = {
        # top-level, if present
        "ts": state.get("ts"),
        "id": state.get("id"),
        # core channels
        "module": cv.get("module"),
        "stage": cv.get("stage"),
        "user_id": cv.get("user_id"),
        "company_id": cv.get("company_id"),
        "context": {
            "thread_type": context.get("thread_type"),
            "entity_id": context.get("entity_id"),
        },
        # high-signal message summary
        "messages": _summarize_messages(cv.get("messages")),
    }

    # Include updated channels if present
    if isinstance(state.get("updated_channels"), list):
        cleaned["updated_channels"] = state["updated_channels"]

    # Keep branch hints only if set (helps debugging routing)
    for k in list(cv.keys()):
        if k.startswith("branch:to:") and cv.get(k) is not None:
            cleaned.setdefault("branches", {})[k] = cv.get(k)

    return cleaned

def main(limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT thread_id, checkpoint_id, checkpoint
            FROM checkpoints
            ORDER BY ROWID DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()

        for thread_id, checkpoint_id, blob in rows:
            print(f"\n🧵 Thread ID: {thread_id}")
            print(f"🧠 Checkpoint: {checkpoint_id}")
            try:
                state = msgpack.unpackb(blob, raw=False)
                cleaned = _clean_state(state if isinstance(state, dict) else {})
                print(json.dumps(cleaned, indent=2, ensure_ascii=False, default=str))
            except Exception as e:
                print(json.dumps({"error": f"failed to decode checkpoint: {e}"}, indent=2))
    finally:
        conn.close()

if __name__ == "__main__":
    main()
