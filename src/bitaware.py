from typing import Any, Generic, TypeVar
from enum import IntFlag, EnumMeta
from pydantic_core import core_schema


class BitFlagMeta(EnumMeta):
    @staticmethod
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0

    def __new__(metacls, cls, bases, classdict):
        for name, value in classdict.items():
            if not name.startswith("_") and not metacls.is_power_of_two(value):
                raise ValueError(f"Value {value} for '{name}' is not a power of 2")
        return super().__new__(metacls, cls, bases, classdict)


class BitFlag(IntFlag, metaclass=BitFlagMeta):
    """
    A class that represents a bit flag, allowing for bitwise operations
    and enumeration of flags.
    """

    pass


BaseFlag = TypeVar("BaseFlag", bound=BitFlag)


class BitAware(int, Generic[BaseFlag]):
    """
    A class that represents a bit-aware integer, allowing for bitwise operations
    and flag management.
    """

    def __init__(self, value: int, flags: BaseFlag):
        self.flags = flags
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer.")
        if value > self.__sum_flags():
            raise ValueError(f"Value {value} exceeds the possible flag setup.")
        self.value = value

    def has(self, flag: BaseFlag) -> bool:
        return bool(self.value & flag)

    def __int__(self):
        return self.value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BitAware):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __sum_flags(self) -> int:
        return sum(flag.value for flag in self.flags)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):
        return core_schema.no_info_after_validator_function(cls.validate, core_schema.int_schema())

    @classmethod
    def validate(cls, value: Any) -> "BitAware":
        if isinstance(value, cls):
            return value
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer.")
        return cls(value)
