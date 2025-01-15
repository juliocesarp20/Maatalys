from abc import ABC, abstractmethod
from typing import List, Tuple


class EventProducerService(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: str) -> None:
        pass

    @abstractmethod
    async def publish_many(self, event_list: List[Tuple[str, str]]) -> None:
        pass
