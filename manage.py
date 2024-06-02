import asyncio

from sqlmodel import Session

from app.database.base import engine, initialize_db
from app.database.operations import get_all_resources
from app.utils import get_logger

logger = get_logger(__name__)


async def check_database_for_resources(session: Session) -> None:
    """
    Check the database for resources every 10 seconds.
    """
    try:
        while True:
            logger.info("Checking database for resources...")
            resources = get_all_resources(session)
            logger.info(f"Found resources: {resources}")

            await asyncio.sleep(10)
    except asyncio.CancelledError:
        logger.info("Cancelled task gracefully")


async def main():
    initialize_db()

    with Session(engine) as session:
        await check_database_for_resources(session)


if __name__ == "__main__":
    asyncio.run(main())
