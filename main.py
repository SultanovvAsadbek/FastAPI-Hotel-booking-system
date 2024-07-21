from fastapi import FastAPI
from router_users import router_users
from router_admins import router_admins

# Создание экземпляра FastAPI с указанием заголовка приложения
app = FastAPI(title="Hotel booking system")

# Подключение маршрутизатора для пользователей
# prefix='/hotel': Добавляет префикс ко всем маршрутам в этом маршрутизаторе
# tags=['For users']: Добавляет теги для группировки маршрутов в документации
app.include_router(router_users, prefix='/hotel', tags=['For users'])

# Подключение маршрутизатора для администраторов
# prefix='/hotel/admin': Добавляет префикс ко всем маршрутам в этом маршрутизаторе
# tags=['For admins']: Добавляет теги для группировки маршрутов в документации
app.include_router(router_admins, prefix='/hotel/admin', tags=['For admins'])

