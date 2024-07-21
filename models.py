from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DECIMAL,
    DateTime,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()


class Users(Base):
    """
    Класс Users представляет таблицу пользователей в базе данных.

    Атрибуты:
    -----------
    id : int
        Уникальный идентификатор пользователя, первичный ключ.
    name : str
        Имя пользователя. Поле не может быть пустым.
    surname : str
        Фамилия пользователя. Поле не может быть пустым.
    passport_series : str
        Серия паспорта пользователя. Поле не может быть пустым и должно быть уникальным.
    phone_number : str
        Номер телефона пользователя. Поле не может быть пустым и должно быть уникальным.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    passport_series = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)


class Rooms(Base):
    """
    Класс Rooms представляет таблицу номеров в базе данных.

    Атрибуты:
    -----------
    id : int
        Уникальный идентификатор номера, первичный ключ.
    room_type : str
        Тип номера (например, стандарт, люкс и т.д.). Поле не может быть пустым.
    room_number : int
        Номер комнаты. Поле не может быть пустым.
    count_room : int
        Количество комнат в номере. Поле не может быть пустым.
    description : str
        Описание номера. Поле не может быть пустым.
    floor : str
        Этаж, на котором находится номер. Поле не может быть пустым.
    price : DECIMAL
        Стоимость номера. Поле не может быть пустым.
    is_reserved : bool
        Статус бронирования номера (забронирован или нет). Поле не может быть пустым, по умолчанию False.

    Связи:
    -----------
    reserved_rooms : relationship
        Связь с таблицей забронированных номеров. Используется для обратного взаимодействия с объектами класса ReservedRooms.
    """

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_type = Column(String, nullable=False)
    room_number = Column(Integer, nullable=False)
    count_room = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    floor = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    is_reserved = Column(Boolean, nullable=False, default=False)

    reserved_rooms = relationship("ReservedRooms", back_populates="room")


class ReservedRooms(Base):
    """
    Класс ReservedRooms представляет таблицу забронированных номеров в базе данных.

    Атрибуты:
    -----------
    id : int
        Уникальный идентификатор записи бронирования, первичный ключ.
    id_room : int
        Идентификатор номера, который был забронирован. Внешний ключ, ссылающийся на таблицу rooms.
    name : str
        Имя гостя, забронировавшего номер. Поле не может быть пустым.
    surname : str
        Фамилия гостя, забронировавшего номер. Поле не может быть пустым.
    passport_series : str
        Серия паспорта гостя. Поле не может быть пустым и должно быть уникальным.
    phone_number : str
        Номер телефона гостя. Поле не может быть пустым и должно быть уникальным.
    datetime : datetime
        Дата и время бронирования. Поле не может быть пустым, по умолчанию устанавливается текущее время.
    checkin : date
        Дата заезда. Поле не может быть пустым.
    checkout : date
        Дата выезда. Поле не может быть пустым.
    commentary : str
        Комментарий к бронированию. Поле не может быть пустым.
    actual : bool
        Статус актуальности бронирования. Поле не может быть пустым, по умолчанию True.

    Связи:
    -----------
    room : relationship
        Связь с таблицей номеров. Используется для обратного взаимодействия с объектами класса Rooms.
    """

    __tablename__ = "reserved_rooms"

    id = Column(Integer, primary_key=True)
    id_room = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    passport_series = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    datetime = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False
    )
    checkin = Column(Date, nullable=False)
    checkout = Column(Date, nullable=False)
    commentary = Column(String, nullable=True)
    actual = Column(Boolean, nullable=False, default=True)

    room = relationship("Rooms", back_populates="reserved_rooms")
