from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL базы данных. Замените на фактический URL вашей базы данных.
DATABASE_URL = "postgresql://booking_room_jdwv_user:kDtdujPTZay3f8X3C2AESkk6SqdX9AsS@dpg-cqeg8i1u0jms739b5oug-a.oregon-postgres.render.com/booking_room_jdwv"

# Создание engine для взаимодействия с базой данных
engine = create_engine(DATABASE_URL)

# Создание настроенного класса "Session"
# autocommit=False: Отключает автоматическое фиксирование транзакций
# autoflush=False: Отключает автоматическое сброс данных в базу до выполнения запроса
# bind=engine: Привязывает сессии к созданному engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)