# CleverChat.py
API wrapper for clever-chat ChatBot API

## Example Sync Usage
```python
from clever_chat import Client

client = Client()

res = client.get_response("Hi")
print(res.message)
client.close()
```

## Example Async Usage
```python
from clever_chat import AsyncClient
import asyncio

client = AsyncClient()

async def main():
    response = await client.get_response("Hi")
    print(response.message)
    await client.close()

asyncio.get_event_loop().run_until_complete(main())
```

## Links
- **Docs:** https://hype3808.github.io/CleverChat.py/
