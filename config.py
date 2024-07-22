from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL базы данных. Замените на фактический URL вашей базы данных.
DATABASE_URL = "postgresql://reserve_room_user:HUPSuuWtCE7mAd6tHmeDmrIMaWXjgIMM@dpg-cqeuk1o8fa8c73ef4j90-a.oregon-postgres.render.com/reserve_room"

# Создание engine для взаимодействия с базой данных
engine = create_engine(DATABASE_URL)

# Создание настроенного класса "Session"
# autocommit=False: Отключает автоматическое фиксирование транзакций
# autoflush=False: Отключает автоматическое сброс данных в базу до выполнения запроса
# bind=engine: Привязывает сессии к созданному engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
