from enum import Enum


class AGENCIES(Enum):
    TUCASAENCUBA = "Tucasaencuba"
    BOOKING_HAVANA = "Booking havana"
    RGN = "RGN"
    CUBAROOM = "CubaRoom"
    FLY_FOR_VACATION = "Fly for Vacations"
    CAPTIVATING_CUBA = "CaptivatingCuba"
    LATINAMERICATRAVEL = "latinamericatravel"
    CUBATRAVEL = "CubaTravel"
    JELOUU = "jelouu"
    EVOLUTION_VOYAGES = "Evolution Voyages"
    DISTAL_CARIBE = "Distal Caribe"
    ALAMO = "Alamano"

    @classmethod
    def key_from_value(cls, value):
        for key, member in cls.__members__.items():
            if member.value == value:
                return key
        return None


class CHANNELS(Enum):
    AIRBNB = "Airbnb"
    BOOKING = "Booking"
    DIRECTO = "Directo"
    AGENCIA = "Agencia"
    REFERIDO = "Referido"
    OTROS = "Otros"
    CORTESIA = "Cortesia"
    FACEBOOK = "Facebook"

    @classmethod
    def key_from_value(cls, value):
        for key, member in cls.__members__.items():
            if member.value == value:
                return key
        return None

class STATUS(Enum):
    CONFIRMADO = "Confirmado"
    CANCELADO = "Cancelado"

    @classmethod
    def key_from_value(cls, value):
        for key, member in cls.__members__.items():
            if member.value == value:
                return key
        return None
