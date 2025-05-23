import redis
import json

r = redis.Redis(host='redis.cache.svc.cluster.local', port=6379, decode_responses=True)

def get_messages_from_redis():
    data = r.get("messages")
    return json.loads(data) if data else []

def cache_message(message):
    messages = get_messages_from_redis()
    messages.append(message)
    r.set("messages", json.dumps(messages))