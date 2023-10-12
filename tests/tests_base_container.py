import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.container import BaseContainer
from app.src.base.value import BaseValue
from app.src.base.exceptions import GroupBaseContainerException


class TestBaseContainer(unittest.TestCase):
    def test_init_with_tuple(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))
        self.assertEqual(container.type, "tuple")

    def test_init_with_dict(self):
        container = BaseContainer({"a": 1, "b": 2, "c": 3}, "dictionary")
        self.assertEqual(container.items, (BaseValue("a"), BaseValue(1), BaseValue("b"), BaseValue(2), BaseValue("c"), BaseValue(3)))

    def test_init_with_list(self):
        container = BaseContainer([1, 2, 3], "list")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_init_with_set(self):
        container = BaseContainer({1, 2, 3}, "set")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_init_with_frozenset(self):
        container = BaseContainer(frozenset({1, 2, 3}), "frozenset")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_iter(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual([item for item in iter(container)], [BaseValue(1), BaseValue(2), BaseValue(3)])

    def test_str(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(str(container), "(1, 2, 3)")

    def test_repr(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(repr(container), "BaseContainer(items=(BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int)), type=tuple)")

    def test_type(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(container.type, "tuple")


    def test_has_slots(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(container.__slots__, ('_items', '_type'))

    def test_create_large_container(self):
        container = BaseContainer([i for i in range(10000)])
        self.assertEqual(len(container.items), 10000)
    
    def test_init_with_multiple_containers(self):
        self.assertRaises(TypeError, BaseContainer, (1, 2, 3), [1, 2, 3])

    def test_init_with_improper_type(self):
        self.assertRaises(TypeError, BaseContainer, (1, 2, 3), 1)

    def test_init_with_improper_type2(self):
        self.assertRaises(TypeError, BaseContainer, (1, 2, 3), "int")

    def test_str_with_dict(self):
        container = BaseContainer({"a": 1, "b": 2, "c": 3}, "dictionary")
        self.assertEqual(str(container), "{'a': 1, 'b': 2, 'c': 3}")

    def test_init_with_mismatched_types_will_work(self):
        contaienr = BaseContainer((1, 2, 3), "set")
        self.assertEqual(contaienr.items, (BaseValue(1), BaseValue(2), BaseValue(3)))
