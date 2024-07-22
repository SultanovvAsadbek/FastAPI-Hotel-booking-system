from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from config import SessionLocal
from models.models import Users, Rooms, ReservedRooms
from schemas.schemas import (
    UserCreate,
    User,
    Room,
    ReservedRoomCreate,
    ReservedRoom,
)
from typing import Annotated
from typing import List
from sqlalchemy.exc import IntegrityError

router_users = APIRouter()


def get_db():
    """
    Создает и возвращает сессию базы данных.

    Эта функция является генератором, который создает сессию базы данных
    и гарантирует ее закрытие после завершения работы с ней.

    Использование:
    --------------
    Эта функция должна использоваться в качестве зависимости в маршрутах FastAPI,
    где требуется доступ к базе данных.

    Возвращает:
    -----------
    db : Session
        Сессия базы данных, созданная из SessionLocal().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_users.post(
    "/users/", response_model=User, description='"Регистрация" пользователя.'
)
def create_user(user: Annotated[UserCreate, Depends()], db: Session = Depends(get_db)):
    """
    Создает нового пользователя в системе.

    Аргументы:
    ----------
    user : UserCreate
        Данные для создания нового пользователя, передаваемые через зависимость Depends().
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    User
        Созданный пользователь.

    Исключения:
    -----------
    HTTPException
        Если возникает ошибка целостности данных (например, уникальное ограничение),
        возвращает HTTP 404 с сообщением об ошибке.
    """
    try:
        db_user = Users(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError as error:
        raise HTTPException(status_code=404, detail=error.orig.args[1])


@router_users.get(
    "/rooms/", response_model=List[Room], description="Получение номеров гостиниц."
)
def read_room(db: Session = Depends(get_db)):
    """
    Получает все записи о номерах гостиниц из базы данных.

    Аргументы:
    ----------
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    List[Room]
        Список всех записей о номерах гостиниц.

    Исключения:
    -----------
    HTTPException
        Если не найдено ни одного номера гостиниц, возвращает HTTP 404.
    """
    db_rooms = db.query(Rooms).all()

    if not db_rooms:
        raise HTTPException(status_code=404, detail="Номера не найдены!")
    return db_rooms


@router_users.post(
    "/create-reserved-rooms/",
    response_model=ReservedRoom,
    description="Забронирование номеров.",
)
def create_reserved_room(
    reserved_room: Annotated[ReservedRoomCreate, Depends()],
    db: Session = Depends(get_db),
):
    """
    Забронировать номер гостиницы.

    Аргументы:
    ----------
    reserved_room : ReservedRoomCreate
        Данные для создания новой записи о забронированном номере, передаваемые через зависимость Depends().
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    ReservedRoom
        Созданная запись о забронированном номере.

    Исключения:
    -----------
    HTTPException
        Если номер уже забронирован (атрибут is_reserved == True), возвращает HTTP 404 с сообщением об ошибке.
    """
    room = db.query(Rooms).filter(Rooms.id == reserved_room.id_room).first()
    if room.is_reserved:
        raise HTTPException(status_code=404, detail="Номер забронирован!")

    room.is_reserved = True

    db_reserved_room = ReservedRooms(**reserved_room.dict())

    db.add(db_reserved_room)
    db.commit()
    db.refresh(db_reserved_room)
    return db_reserved_room
