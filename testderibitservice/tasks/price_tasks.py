import asyncio
import time

from testderibitservice.celery import celery_app
from testderibitservice.services.deribit_client import DeribitClient
from testderibitservice.database import SessionLocal
from testderibitservice.models.price import Price
from settings import settings


@celery_app.task(name="testderibitservice.tasks.price_tasks.fetch_prices")
def fetch_prices():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_fetch_prices_async())
    loop.close()


async def _fetch_prices_async():
    client = DeribitClient()
    db = SessionLocal()

    try:
        for ticker in settings.tickers:
            price = await client.get_index_price(ticker)

            price_row = Price(ticker=ticker, price=price, timestamp=int(time.time()))

            db.add(price_row)

        db.commit()

    except Exception:
        db.rollback()

    finally:
        db.close()
