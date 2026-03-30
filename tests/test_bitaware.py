import pytest
from bitaware import BitFlag, BitAware, DefinedFlag


class MyFlags(BitFlag):
    FLAG_A = 1
    FLAG_B = 2
    FLAG_C = 4


class MyBit(BitAware[MyFlags]):
    OPTION_ONE = MyFlags.FLAG_A
    OPTION_TWO = MyFlags.FLAG_B | MyFlags.FLAG_A
    OPTION_THREE = MyFlags.FLAG_C | MyFlags.FLAG_B | MyFlags.FLAG_A

    def __init__(self, value: int):
        super().__init__(value, MyFlags)


def test_bitaware_init_valid():
    b = MyBit(1)
    assert int(b) == 1
    assert b.flags is MyFlags


def test_bitaware_init_invalid_value_type():
    with pytest.raises(ValueError):
        MyBit("invalid")


def test_bitaware_init_negative_value():
    with pytest.raises(ValueError):
        MyBit(-1)


def test_bitaware_init_zero_value():
    with pytest.raises(ValueError):
        MyBit(0)


def test_bitaware_init_value_exceeds_flags():
    # sum of flags: 1 + 2 + 4 = 7, so 8 is invalid
    with pytest.raises(ValueError):
        MyBit(8)


def test_bitaware_has_flag():
    b = MyBit(3)  # 3 = FLAG_A | FLAG_B
    assert b.has(MyFlags.FLAG_A)
    assert b.has(MyFlags.FLAG_B)
    assert not b.has(MyFlags.FLAG_C)


def test_bitaware_repr_and_int():
    b = MyBit(2)
    assert repr(b) == "MyBit(MyFlags.FLAG_B)"
    assert int(b) == 2


def test_bitaware_eq_with_int():
    b = MyBit(4)
    assert b == 4
    assert not (b == 2)


def test_bitaware_eq_with_bitaware():
    b1 = MyBit(1)
    b2 = MyBit(1)
    b3 = MyBit(2)
    assert b1 == b2
    assert b1 != b3


def test_bitflagmeta_non_power_of_two():
    with pytest.raises(ValueError):

        class BadFlags(BitFlag):
            FLAG_X = 3  # not a power of two


def test_bitaware_validate_int():
    b = MyBit.validate(2)
    assert isinstance(b, BitAware)
    assert int(b) == 2


def test_bitaware_validate_bitaware():
    b1 = MyBit(1)
    b2 = BitAware.validate(b1)
    assert b1 is b2


def test_bitaware_validate_invalid():
    with pytest.raises(ValueError):
        BitAware.validate(-1)
    with pytest.raises(TypeError):
        BitAware.validate("bad")


def test_bitaware_defined_flags():
    b = MyBit.defined_flags()

    assert isinstance(b, list)
    assert all(isinstance(flag, DefinedFlag) for flag in b)
    assert len(b) == 3
    assert b[0].name == "OPTION_ONE"
    assert b[1].name == "OPTION_TWO"
    assert b[2].name == "OPTION_THREE"
    assert b[0].value == 1
    assert b[1].value == 3
    assert b[2].value == 7
