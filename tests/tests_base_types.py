import unittest
import sys
import random
from attrs import define

from typing import Union, TypeAlias, Any, Optional, TypeVar, Type, Tuple, Callable, Iterable, Iterator, Sequence, Mapping, MutableMapping, Set, MutableSet, MappingView, KeysView, ItemsView, ValuesView, Awaitable, AsyncIterable, AsyncIterator, Coroutine, Collection, Container, Reversible, Generator, AsyncGenerator, SupportsAbs, SupportsBytes, SupportsComplex, SupportsFloat, SupportsIndex, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.types import BaseValueTypes, BaseTypesInterface, BaseContainerTypes


class TestBaseTypesInterface(unittest.TestCase):
    def setUp(self):

        @define(frozen=True, slots=True, weakref_slot=False)
        class BaseTypesExample(BaseTypesInterface):
            integer: TypeAlias = int
            floating_point: TypeAlias = float
            boolean: TypeAlias = bool
            string: TypeAlias = str
            bytes_: TypeAlias = bytes

            @property
            def all(self) -> Union[TypeAlias, TypeAlias]:
                return int | float | bool | str | bytes

            @property
            def aliases(self) -> dict[TypeAlias, tuple[str]]:
                return {
                    self.integer: ("int", "integer"),
                    self.floating_point: ("float", "floating_point"),
                    self.boolean: ("bool", "boolean"),
                    self.string: ("str", "string"),
                    self.bytes_: ("bytes", "bytestring")
                }

        self.base_types_interface = BaseTypesExample()

    def test_base_type_interface_init_(self):
        self.assertEqual(
            self.base_types_interface.aliases, {
                self.base_types_interface.integer: ("int", "integer"),
                self.base_types_interface.floating_point: ("float", "floating_point"),
                self.base_types_interface.boolean: ("bool", "boolean"),
                self.base_types_interface.string: ("str", "string"),
                self.base_types_interface.bytes_: ("bytes", "bytestring")
            }
        )

    def test_base_type_interface_has_slots(self):
        for slot in self.base_types_interface.__slots__:
            self.assertEqual(hasattr(self.base_types_interface, slot), True)

    def test_base_type_interface_has_no_weakref_slot(self):
        self.assertFalse(hasattr(self.base_types_interface, "__weakref__"))

    def test_base_type_interface_has_no_dict(self):
        self.assertEqual(hasattr(self.base_types_interface, "__dict__"), False)

    def test_base_type_interface_repr(self):
        print(self.base_types_interface.__slots__)
        self.assertEqual(repr(self.base_types_interface), "BaseTypesExample(integer=<class 'int'>, floating_point=<class 'float'>, boolean=<class 'bool'>, string=<class 'str'>, bytes_=<class 'bytes'>)")


class TestBaseValueTypes(unittest.TestCase):
    def setUp(self):
        self.base_value_types = BaseValueTypes()

    def test_init_with_str(self):
        self.assertEqual(self.base_value_types.integer, int)
        self.assertEqual(self.base_value_types.floating_point, float)
        self.assertEqual(self.base_value_types.boolean, bool)
        self.assertEqual(self.base_value_types.string, str)
        self.assertEqual(self.base_value_types.bytes_, bytes)
        self.assertEqual(self.base_value_types.number, int | float)
        self.assertEqual(self.base_value_types.text, str | bytes | bool | None)
        # self.assertEqual(self.base_value_types._all, int | float | str | bytes | bool | None)

    def test_base_value_type_has_slots(self):
        for slot in self.base_value_types.__slots__:
            self.assertTrue(hasattr(self.base_value_types, slot))

    def test_base_value_type_has_all_slots(self):
        self.assertEqual(
            self.base_value_types.__slots__, (
                "integer", "floating_point", "boolean", "string", "bytes_", "number", "text", # "_all"
            )
        )

    def test_base_value_type_has_no_weakref_slot(self):
        self.assertFalse(hasattr(self.base_value_types, "__weakref__"))

    def test_base_value_type_has_no_dict(self):
        self.assertFalse(hasattr(self.base_value_types, "__dict__"))

    def test_base_value_type_repr(self):
        self.maxDiff = None
        self.assertEqual(
            repr(self.base_value_types), "BaseValueTypes(integer=<class 'int'>, floating_point=<class 'float'>, boolean=<class 'bool'>, string=<class 'str'>, bytes_=<class 'bytes'>, number=int | float, text=str | bytes | bool | None)"
        )

    def _test_base_value_type_all_property(self):
        self.assertEqual(self.base_value_types.all, int | float | str | bytes | bool | None)



class TestBaseContainerTypes(unittest.TestCase):
    def setUp(self):
        self.base_container_types = BaseContainerTypes()
        
