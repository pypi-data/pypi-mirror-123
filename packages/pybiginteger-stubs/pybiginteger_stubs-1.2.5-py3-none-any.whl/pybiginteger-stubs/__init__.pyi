"""A C++ port of the C# BigInteger class"""
import pybiginteger
import typing

__all__ = [
    "BigInteger"
]


class BigInteger():
    def __abs__(self) -> BigInteger: ...
    @typing.overload
    def __add__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __add__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __and__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __and__(self, arg0: int) -> BigInteger: ...
    def __bytes__(self) -> bytes: 
        """
                        Return the value of the BigInteger in little endian order.
                        For more information on the byte representation see:
                        https://docs.microsoft.com/en-us/dotnet/api/system.numerics.biginteger.tobytearray?view=netcore-3.1
        """
    def __deepcopy__(self, arg0: object) -> BigInteger: ...
    @typing.overload
    def __divmod__(self, arg0: BigInteger) -> tuple: ...
    @typing.overload
    def __divmod__(self, arg0: int) -> tuple: ...
    @typing.overload
    def __eq__(self, arg0: BigInteger) -> bool: ...
    @typing.overload
    def __eq__(self, arg0: int) -> bool: ...
    def __float__(self) -> float_: ...
    @typing.overload
    def __floordiv__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __floordiv__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __ge__(self, arg0: BigInteger) -> bool: ...
    @typing.overload
    def __ge__(self, arg0: int) -> bool: ...
    @typing.overload
    def __gt__(self, arg0: BigInteger) -> bool: ...
    @typing.overload
    def __gt__(self, arg0: int) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: bytes) -> None: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    def __int_(self) -> int: ...
    def __invert__(self) -> BigInteger: ...
    @typing.overload
    def __le__(self, arg0: BigInteger) -> bool: ...
    @typing.overload
    def __le__(self, arg0: int) -> bool: ...
    @typing.overload
    def __lshift__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __lshift__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __lt__(self, arg0: BigInteger) -> bool: ...
    @typing.overload
    def __lt__(self, arg0: int) -> bool: ...
    @typing.overload
    def __mod__(self, arg0: BigInteger) -> BigInteger: 
        """
                        Note: this always uses the modulo operation of the BigInteger class.
                        C# uses truncated division whereas Python uses floored division.
                        For more information see:
                        https://en.wikipedia.org/wiki/Modulo_operation
        """
    @typing.overload
    def __mod__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __mul__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __mul__(self, arg0: int) -> BigInteger: ...
    def __neg__(self) -> BigInteger: ...
    @typing.overload
    def __or__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __or__(self, arg0: int) -> BigInteger: ...
    def __pos__(self) -> BigInteger: ...
    @typing.overload
    def __pow__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __pow__(self, arg0: BigInteger, arg1: BigInteger) -> BigInteger: ...
    @typing.overload
    def __pow__(self, arg0: BigInteger, arg1: int) -> BigInteger: ...
    @typing.overload
    def __pow__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __pow__(self, arg0: int, arg1: BigInteger) -> BigInteger: ...
    def __radd__(self, arg0: int) -> int: ...
    def __rand__(self, arg0: int) -> int: ...
    def __rdivmod__(self, arg0: int) -> tuple: ...
    def __rfloordiv__(self, arg0: int) -> int: ...
    def __rlshift__(self, arg0: int) -> int: ...
    def __rmod__(self, arg0: int) -> int: 
        """
                        Note: this always uses the modulo operation of the BigInteger class.
                        C# uses truncated division whereas Python uses floored division.
                        For more information see:
                        https://en.wikipedia.org/wiki/Modulo_operation
        """
    def __rmul__(self, arg0: int) -> int: ...
    def __ror__(self, arg0: int) -> int: ...
    def __rpow__(self, arg0: int) -> int: ...
    def __rrshift__(self, arg0: int) -> int: ...
    @typing.overload
    def __rshift__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __rshift__(self, arg0: int) -> BigInteger: ...
    def __rsub__(self, arg0: int) -> int: ...
    def __rtruediv__(self, arg0: int) -> int: ...
    def __rxor__(self, arg0: int) -> int: ...
    def __str__(self) -> str: ...
    @typing.overload
    def __sub__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __sub__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __truediv__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __truediv__(self, arg0: int) -> BigInteger: ...
    @typing.overload
    def __xor__(self, arg0: BigInteger) -> BigInteger: ...
    @typing.overload
    def __xor__(self, arg0: int) -> BigInteger: ...
    def get_bit_Length(self) -> int: ...
    def is_even(self) -> bool: ...
    def is_power_of_two(self) -> bool: ...
    @staticmethod
    @typing.overload
    def log(value: BigInteger) -> float: ...
    @staticmethod
    @typing.overload
    def log(value: BigInteger, base_value: float) -> float: ...
    @staticmethod
    @typing.overload
    def log(value: int) -> float: ...
    @staticmethod
    @typing.overload
    def log(value: int, base_value: float) -> float: ...
    @staticmethod
    @typing.overload
    def log10(value: BigInteger) -> float: ...
    @staticmethod
    @typing.overload
    def log10(value: int) -> float: ...
    @staticmethod
    def minus_one() -> BigInteger: ...
    @staticmethod
    def one() -> BigInteger: ...
    def to_array(self, is_unsigned: bool = False, is_bigendian: bool = False) -> bytes: 
        """
                        Return the value of the BigInteger.
                        For more information on the options see:
                        https://docs.microsoft.com/en-us/dotnet/api/system.numerics.biginteger.tobytearray?view=netcore-3.1#System_Numerics_BigInteger_ToByteArray_System_Boolean_System_Boolean_
        """
    @staticmethod
    def zero() -> BigInteger: ...
    @property
    def sign(self) -> int:
        """
        :type: int
        """
    __version__ = '1.2'
    __version_bindings__ = '1.2.5'
    pass
