web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"