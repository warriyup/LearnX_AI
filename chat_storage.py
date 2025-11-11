
import json
import os
import uuid
from datetime import datetime

DB_PATH = "chats.json"

def ensure_db_exists():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"chats": {}}, f, ensure_ascii=False, indent=2)

def load_db():
    ensure_db_exists()
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"chats": {}}

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def list_chats():
    db = load_db()
    return db.get("chats", {})

def create_chat():
    db = load_db()
    chats = db.setdefault("chats", {})
    chat_id = str(uuid.uuid4())
    chats[chat_id] = {
        "title": "Новый чат",
        "messages": [],
        "created_at": datetime.utcnow().isoformat()
    }
    save_db(db)
    return chat_id

def get_chat(chat_id):
    db = load_db()
    return db.get("chats", {}).get(chat_id, {"title": "Новый чат", "messages": []})

def add_message(chat_id, role, content):
    db = load_db()
    chats = db.setdefault("chats", {})
    if chat_id not in chats:
        chats[chat_id] = {"title": "Новый чат", "messages": []}
    chats[chat_id]["messages"].append({
        "role": role,
        "content": content,
        "time": datetime.utcnow().isoformat()
    })
    save_db(db)

def rename_chat(chat_id, title):
    db = load_db()
    chats = db.setdefault("chats", {})
    if chat_id in chats:
        chats[chat_id]["title"] = title
    else:
        chats[chat_id] = {"title": title, "messages": []}
    save_db(db)

def delete_chat(chat_id):
    db = load_db()
    chats = db.setdefault("chats", {})
    if chat_id in chats:
        del chats[chat_id]
        save_db(db)
        return True
    return False
