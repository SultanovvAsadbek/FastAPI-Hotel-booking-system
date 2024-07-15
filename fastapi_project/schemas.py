import re
from pydantic import BaseModel, validator, Field
from datetime import date
from fastapi import HTTPException
from typing import Optional

from pydantic import BaseModel, validator
from fastapi import HTTPException
import re


class UserCreate(BaseModel):
    """
    Модель данных для создания пользователя.

    Атрибуты:
    - name (str): Имя пользователя.
    - surname (str): Фамилия пользователя.
    - passport_series (str): Серия и номер паспорта пользователя.
    - phone_number (str): Номер телефона пользователя в формате "+998хх xxx-xx-xx".
    """

    name: str
    surname: str
    passport_series: str
    phone_number: str

    @validator("passport_series")
    def validate_passport_series(cls, value):
        """
        Валидатор для проверки формата серии и номера паспорта.

        Параметры:
        - value (str): Значение серии и номера паспорта.

        Возвращает:
        - str: Значение серии и номера паспорта, если прошло проверку формата.

        Исключения:
        - HTTPException: Если формат не соответствует ожидаемому, выбрасывается исключение с кодом 404 и деталями ошибки.
        """
        pattern = re.compile(r"^[A-Z]{2}\d{7}$")
        if not pattern.match(value):
            raise HTTPException(
                status_code=404,
                detail="Номер паспорта должен быть в формате «XX1234567» где XX — серия паспорта, за которыми следуют 7 цифр.",
            )
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        """
        Валидатор для проверки формата номера телефона.

        Параметры:
        - value (str): Номер телефона.

        Возвращает:
        - str: Номер телефона, если прошло проверку формата.

        Исключения:
        - HTTPException: Если формат не соответствует ожидаемому, выбрасывается исключение с кодом 404 и деталями ошибки.
        """
        pattern = re.compile(r"^\+998\d{2} \d{3}-\d{2}-\d{2}$")
        if not pattern.match(value):
            raise HTTPException(
                status_code=404,
                detail="Номер телефона должен быть в формате «+998хх xxx-xx-xx», где x — цифра.",
            )
        return value

class User(UserCreate):
    """
    Модель данных для пользователя с идентификатором.

    Наследует:
    - UserCreate: Базовая модель данных для создания пользователя.

    Атрибуты:
    - id (int): Уникальный идентификатор пользователя.

    Вложенный классы:
    - Config: Настройки конфигурации модели.

    """

    id: int

    class Config:
        """
        Конфигурация модели User.

        Атрибуты:
        - from_attributes (bool): Если True, инициализация модели из атрибутов включает
          только атрибуты, определенные в атрибутах класса UserCreate.
        """

        from_attributes = True


class RoomCreate(BaseModel):
    """
    Модель данных для создания комнаты.

    Атрибуты:
    - room_type (str): Тип комнаты.
    - room_number (int): Номер комнаты.
    - count_room (int): Количество комнат в номере.
    - description (str): Описание комнаты.
    - floor (int): Этаж, на котором расположена комната.
    - is_reserved (bool, optional): Флаг зарезервированности комнаты (по умолчанию False).
    - price (float): Цена за проживание в комнате.
    """

    room_type: str
    room_number: int
    count_room: int
    description: str
    floor: int
    is_reserved: bool = False
    price: float



class UpdateRoom(BaseModel):
    """
    Модель данных для обновления атрибутов комнаты.

    Атрибуты (все атрибуты являются опциональными):
    - room_type (str, optional): Новый тип комнаты.
    - room_number (int, optional): Новый номер комнаты.
    - count_room (int, optional): Новое количество комнат в номере.
    - description (str, optional): Новое описание комнаты.
    - floor (int, optional): Новый этаж, на котором расположена комната.
    - is_reserved (bool, optional): Новый флаг зарезервированности комнаты.
    - price (float, optional): Новая цена за проживание в комнате.
    """

    room_type: Optional[str] = None
    room_number: Optional[int] = None
    count_room: Optional[int] = None
    description: Optional[str] = None
    floor: Optional[int] = None
    is_reserved: Optional[bool] = None
    price: Optional[float] = None


class Room(RoomCreate):
    """
    Модель данных для комнаты с уникальным идентификатором.

    Наследует:
    - RoomCreate: Базовая модель данных для создания комнаты.

    Атрибуты:
    - id (int): Уникальный идентификатор комнаты.

    Вложенный классы:
    - Config: Настройки конфигурации модели.

    """

    id: int

    class Config:
        """
        Конфигурация модели Room.

        Атрибуты:
        - from_attributes (bool): Если True, инициализация модели из атрибутов включает
          только атрибуты, определенные в базовой модели RoomCreate.
        """

        from_attributes = True


class ReservedRoomCreate(BaseModel):
    """
    Модель данных для создания зарезервированной комнаты.

    Атрибуты:
    - id_room (int): Уникальный идентификатор комнаты.
    - name (str): Имя. 
    - surname (str): Фамилия.
    - passport_series (str): Серия и номер паспорта.
    - phone_number (str): Номер телефона.
    - checkin (date): Дата заезда в формате YYYY-MM-DD.
    - checkout (date): Дата выезда в формате YYYY-MM-DD.
    - commentary (str): Комментарий.
    - actual (bool, optional): Флаг актуальности резервации (по умолчанию True).

    Вложенный класс:
    - Config: Настройки конфигурации модели.
    """
    id_room: int
    name: str = Field(..., description="Фамилия")
    surname: str = Field(..., description="Фамилия")
    passport_series: str = Field(..., description="Серия и паспорт номера")
    phone_number: str = Field(..., description="Телефон номер")
    checkin: date = Field(..., description="Дата заезда в формате YYYY-MM-DD")
    checkout: date = Field(..., description="Дата выезда в формате YYYY-MM-DD")
    commentary: str
    actual: bool = True

    class Config:
        """
        Конфигурация модели ReservedRoomCreate.

        Атрибуты:
        - from_attributes (bool): Если True, инициализация модели из атрибутов включает
          только атрибуты, определенные в модели ReservedRoomCreate.
        """
        from_attributes = True


class ReservedRoom(ReservedRoomCreate):
    """
    Представляет зарезервированную комнату, расширяя класс ReservedRoomCreate, добавляя уникальный идентификатор.

    Атрибуты:
        id (int): Уникальный идентификатор зарезервированной комнаты.
    """
    id: int

    class Config:
        from_attributes = True
