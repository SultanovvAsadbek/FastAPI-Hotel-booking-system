from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from config import SessionLocal
from models.models import Rooms, ReservedRooms
from schemas.schemas import (
    RoomCreate,
    Room,
    ReservedRoom,
    UpdateRoom,
)
from typing import Annotated
from typing import List

router_admins = APIRouter()


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


@router_admins.get("/update-all-data")
def update_all_data(db: Session = Depends(get_db)):
    """
    Обновляет статусы всех зарезервированных комнат и записей бронирования,
    если дата выезда меньше или равна текущей дате.

    Аргументы:
    ----------
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    list
        Список обновленных записей о забронированных номерах.
    """

    current_date = datetime.today().date()

    # Получить все зарезервированные комнаты с датой выезда <= текущей даты
    reserved_rooms = (
        db.query(ReservedRooms).filter(ReservedRooms.checkout <= current_date).all()
    )

    if not reserved_rooms:
        return []

    room_ids = [reserved_room.id_room for reserved_room in reserved_rooms]

    # Обновить статус комнат в одной транзакции
    db.query(Rooms).filter(Rooms.id.in_(room_ids)).update(
        {"is_reserved": False}, synchronize_session=False
    )

    # Обновить статус резервов в одной транзакции
    db.query(ReservedRooms).filter(
        ReservedRooms.id.in_([reserved_room.id for reserved_room in reserved_rooms])
    ).update({"actual": False}, synchronize_session=False)

    # Закоммитить все изменения
    db.commit()

    return reserved_rooms


@router_admins.delete("/delete-room/{id}", description='Удаление номеров по его "id"')
def delete_room(id: int, db: Session = Depends(get_db)):
    """
    Удаляет номер по его идентификатору (id).

    Аргументы:
    ----------
    id : int
        Идентификатор номера, который необходимо удалить.
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    Rooms
        Удаленный номер, если он существует. В противном случае вызывается HTTPException.
    """
    db_room = db.query(Rooms).filter(Rooms.id == id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Номер не найден!")

    db.delete(db_room)
    db.commit()

    return db_room


@router_admins.get(
    "/read-reserved-rooms/",
    response_model=List[ReservedRoom],
    description="Получение забронированных номеров",
)
def read_reserved_room(db: Session = Depends(get_db)):
    """
    Получает все записи забронированных номеров из базы данных.

    Аргументы:
    ----------
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    List[ReservedRoom]
        Список всех записей забронированных номеров.

    Исключения:
    -----------
    HTTPException
        Если не найдено ни одной записи забронированных номеров, возвращает HTTP 404.
    """
    db_reserved_room = db.query(ReservedRooms).all()

    if db_reserved_room is None:
        raise HTTPException(
            status_code=404, detail="Забронированных номеров не найдено!"
        )
    return db_reserved_room


@router_admins.post(
    "/create-rooms/", response_model=Room, description="Создание номеров."
)
def create_room(room: Annotated[RoomCreate, Depends()], db: Session = Depends(get_db)):
    """
    Создает новый номер в базе данных.

    Аргументы:
    ----------
    room : RoomCreate
        Данные для создания нового номера, передаваемые через зависимость Depends().
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    Room
        Созданный номер.

    Исключения:
    -----------
    HTTPException
        Если номер с указанным номером комнаты уже существует, возвращает HTTP 400.
    """

    db_room = db.query(Rooms).filter(Rooms.room_number == room.room_number).first()
    if db_room:
        raise HTTPException(status_code=400, detail="Номер уже существует!")
    db_room = Rooms(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@router_admins.put(
    "/update-room/{id}",
    response_model=Room,
    description="Обновление данных номеров гостиниц.",
)
def update_room(
    id: int, room: Annotated[UpdateRoom, Depends()], db: Session = Depends(get_db)
):
    """
    Обновляет данные номера гостиницы по его идентификатору (id).

    Аргументы:
    ----------
    id : int
        Идентификатор номера, который необходимо обновить.
    room : UpdateRoom
        Данные для обновления номера, передаваемые через зависимость Depends().
    db : Session
        Сессия базы данных, передаваемая через Depends(get_db).

    Возвращает:
    -----------
    Room
        Обновленный номер.

    Исключения:
    -----------
    HTTPException
        Если номер с указанным id не найден, возвращает HTTP 404.
    """

    db_room = db.query(Rooms).filter(Rooms.id == id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Номер с таким id не найден!")

    if room.room_type is not None:
        db_room.room_type = room.room_type

    if room.room_number is not None:
        db_room.room_number = room.room_number

    if room.count_room is not None:
        db_room.count_room = room.count_room

    if room.description is not None:
        db_room.description = room.description

    if room.floor is not None:
        db_room.floor = room.floor

    if room.price is not None:
        db_room.price = room.price

    if room.is_reserved is not None:
        db_room.is_reserved = room.is_reserved

    db.commit()
    db.refresh(db_room)
    return db_room
