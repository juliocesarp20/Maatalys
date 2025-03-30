import logging

from src.search.search_topics import SearchTopics
from src.streaming.event_registry import EventRegistry

logger = logging.getLogger(__name__)


class SearchConsumer:
    @staticmethod
    async def handle_search(payload: dict):
        logger.info(f"Processing search payload: {payload}")
        raise Exception("falhou")


EventRegistry.register(SearchTopics.SEARCH_CONSUMER.value, SearchConsumer.handle_search)
