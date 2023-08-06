import asyncio as aio

from .wcd import main, LOGGER


try:
    aio.run(main())
except KeyboardInterrupt:
    LOGGER.info("Received 'KeyboardInterrupt'. Quitting...")

