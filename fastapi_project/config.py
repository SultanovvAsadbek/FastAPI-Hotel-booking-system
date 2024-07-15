from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL базы данных. Замените на фактический URL вашей базы данных.
DATABASE_URL = f"postgresql://username:password@localhost/db_name"

# Создание engine для взаимодействия с базой данных
engine = create_engine(DATABASE_URL)

# Создание настроенного класса "Session"
# autocommit=False: Отключает автоматическое фиксирование транзакций
# autoflush=False: Отключает автоматическое сброс данных в базу до выполнения запроса
# bind=engine: Привязывает сессии к созданному engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)