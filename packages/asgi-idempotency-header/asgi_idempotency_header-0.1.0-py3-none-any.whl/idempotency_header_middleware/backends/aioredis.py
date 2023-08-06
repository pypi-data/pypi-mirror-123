import json
from typing import Optional, Tuple

from aioredis.client import Redis
from aioredis.exceptions import LockError
from fastapi.responses import JSONResponse

from idempotency_header_middleware.backends.base import Backend


class AioredisBackend(Backend):
    """
    Redis backend.
    """

    def __init__(
        self, redis: Redis, keys_key: str = 'idempotency-key-keys', response_key: str = 'idempotency-key-responses'
    ):
        self.redis = redis
        self.KEYS_KEY = keys_key
        self.RESPONSE_KEY = response_key

    def _get_keys(self, idempotency_key: str) -> Tuple[str, str]:
        payload_key = self.RESPONSE_KEY + idempotency_key
        status_code_key = self.RESPONSE_KEY + idempotency_key + 'status-code'
        return payload_key, status_code_key

    async def get_stored_response(self, idempotency_key: str) -> Optional[JSONResponse]:
        """
        Return a stored response if it exists, otherwise return None.
        """
        payload_key, status_code_key = self._get_keys(idempotency_key)

        if not (payload := await self.redis.get(payload_key)):
            return None
        else:
            status_code = await self.redis.get(status_code_key)

        return JSONResponse(json.loads(payload), status_code=int(status_code))

    async def store_response_data(
        self, idempotency_key: str, payload: dict, status_code: int, expiry: Optional[int] = None
    ) -> None:
        """
        Store a response in redis.
        """
        payload_key, status_code_key = self._get_keys(idempotency_key)

        await self.redis.set(payload_key, json.dumps(payload))
        await self.redis.set(status_code_key, status_code)

        if expiry:
            await self.redis.expire(payload_key, expiry)
            await self.redis.expire(status_code_key, expiry)

    async def store_idempotency_key(self, idempotency_key: str) -> bool:
        """
        Store an idempotency key header value in a set.
        """
        try:
            # acquire lock
            async with self.redis.lock(self.KEYS_KEY + '-lock', timeout=1) as lock:
                # when lock is acquired, check if the key already exists
                keys = await self.redis.smembers(self.KEYS_KEY)
                if idempotency_key in keys:
                    return True
                else:
                    await lock.redis.sadd(self.KEYS_KEY, idempotency_key)
                    return False
        except LockError:  # pragma: no cover
            return await self.store_idempotency_key(idempotency_key)

    async def clear_idempotency_key(self, idempotency_key: str) -> None:
        """
        Remove an idempotency header value from the set.
        """
        await self.redis.srem(self.KEYS_KEY, idempotency_key)
