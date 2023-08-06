import asyncio
import logging
from asyncio import Task
from typing import Optional

from aioredis import Redis, create_redis

from komolibs.core.utils.async_utils import safe_ensure_future
from komolibs.logger import KomoLogger
from komolibs.pubsub import check_redis_connection_sync


class Publisher:
    publisher_logger: Optional[KomoLogger] = None
    _shared_instance: "Publisher" = None

    @classmethod
    def get_instance(cls,
                     url: str,
                     port: int,
                     password: str,
                     db: int = 0,
                     ssl: bool = True,
                     channel: Optional[str] = "*") -> "Publisher":
        if cls._shared_instance is None:
            cls._shared_instance = Publisher(url=url, port=port, password=password, db=db, ssl=ssl, channel=channel)
        return cls._shared_instance

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls.publisher_logger is None:
            cls.publisher_logger = logging.getLogger(__name__)
        return cls.publisher_logger

    def __init__(self,
                 url: str,
                 port: int,
                 password: str,
                 db: int = 0,
                 ssl: bool = True,
                 channel: Optional[str] = "*"):
        self._url: str = url
        self._port = port
        self._password = password
        self._db = db
        self._ssl =ssl
        self._channel: Optional[str] = channel
        self._redis: Optional[Redis] = None
        self._ready: bool = False

        self._publish_message_loop_task: Optional[Task] = None
        self._publish_stream: asyncio.Queue = asyncio.Queue()

    @property
    def ready(self):
        return self._ready

    @property
    def publish_stream(self) -> asyncio.Queue:
        return self._publish_stream

    async def publish(self, message: dict):
        self.publish_stream.put_nowait(message)

    async def start(self):
        self._redis = await create_redis((self._url, self._port), db=self._db, password=self._password, ssl=self._ssl)
        # await self._redis.set("MYKEY", "HELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOO")
        # key = await self._redis.get("MYKEY")
        # print(key)
        self._publish_message_loop_task = safe_ensure_future(self.publish_message_loop())
        self._ready = True

    async def stop(self):
        self._redis.close()
        await self._redis.wait_closed()
        if self._publish_message_loop_task is not None:
            self._publish_message_loop_task.cancel()
            self._publish_message_loop_task = None

    async def publish_message_loop(self):
        message = None
        try:
            while True:
                try:
                    message = await self._publish_stream.get()
                    assert type(message) is dict, "Only dictionary type is processed by this publisher."
                    assert self._channel is not None, f"Please supply valid publication channel. {self._channel} is not valid. "
                    await self._redis.publish_json(self._channel, message)
                    await asyncio.sleep(0.1)
                except AssertionError as e:
                    self.logger().error(f"{e}. {type(message)}")
        except asyncio.CancelledError:
            raise
        except Exception:
            raise
        finally:
            await self.stop()

    def is_connection_ok(self):
        try:
            check_redis_connection_sync(url=self._url,
                                        port=int(self._port),
                                        password=self._password)
            return True
        except Exception as e:
            self.logger().error(f"Redis connection error {e}")
            return False
