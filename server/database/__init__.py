from tortoise import Tortoise, run_async

async def init_db():
    try:
        # Initialize Tortoise ORM with SQLite
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models']}
        )
        # Generate schemas
        await Tortoise.generate_schemas()
    except Exception as e:
        print(f"Error initializing database: {e}")

async def close_db():
    try:
        # Close database connections
        await Tortoise.close_connections()
    except Exception as e:
        print(f"Error closing database connections: {e}")