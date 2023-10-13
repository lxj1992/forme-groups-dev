from attrs import define, field, validators
from typing import Optional, TypeAlias, Type, override

from .interface import BaseInterface
from .types import BaseValueTypes, BaseContainerTypes
from .value import BaseValue
from .exceptions import GroupBaseContainerException
from ..utils.crypto import MerkleTree


def _contains_sub_container(item: BaseContainerTypes().all) -> bool:
    """
    Checks if container contains a sub container
    """
    if isinstance(item, BaseContainerTypes().linear):
        for value in item:
            if isinstance(value, BaseContainerTypes().all):
                return True

    elif isinstance(item, BaseContainerTypes().named):
        for value in item.values():
            if isinstance(value, BaseContainerTypes().all):
                return True

    return False


def _base_container_converter(item: BaseContainerTypes().all) -> tuple[BaseValue]:
    """
    Converter function for _items field
    """
    base_values: tuple = tuple()
    exc_message = f"Expected a non-container, but received {type(item)}"
    # __UNIT__ = type(item)

    if _contains_sub_container(item):
        raise GroupBaseContainerException(exc_message)

    if isinstance(item, BaseContainerTypes().linear):
        for item_ in item:
            if isinstance(item_, BaseContainerTypes().all):
                raise GroupBaseContainerException(exc_message)
            
            if isinstance(item_, BaseValue):
                base_values += tuple([item_], )
            else:
                base_values += tuple([BaseValue(item_)])

    elif isinstance(item, BaseContainerTypes().named):
        for key, value in item.items():
            if isinstance(value, BaseContainerTypes().all):
                raise GroupBaseContainerException(exc_message)

            if isinstance(value, BaseValue):
                base_values += tuple([BaseValue(key), value])
            else:
                base_values += tuple([BaseValue(key), BaseValue(value)])
    else:
        raise GroupBaseContainerException(f"Expected a container, but received a non-container {type(item)}")
    
    return base_values


def _base_container_type_converter(item: BaseContainerTypes().all | str) -> BaseContainerTypes().all:
    """
    Converter function for _type field
    """
    base_container_types = BaseContainerTypes()
    type_from_alias: TypeAlias | type = None
    if isinstance(item, str) and len(item) > 0:
        type_from_alias = base_container_types._get_type_from_alias(item)
    elif isinstance(item, type):
        type_from_alias = item

    return type_from_alias


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer[T: BaseContainerTypes().all](BaseInterface):

    _items: tuple[BaseValue] = field(
        validator=validators.deep_iterable(validators.instance_of(BaseValue | BaseValueTypes().all), iterable_validator=validators.instance_of(tuple)),
        converter=_base_container_converter
    )
    _type: Optional[Type[BaseContainerTypes().all] | str] = field(
        validator=validators.instance_of(type | str),
        converter=_base_container_type_converter,
        default=tuple
    )

    @property
    def items(self) -> tuple[BaseValue]:
        """The items held by the BaseContainer Class

        Returns:
            tuple[BaseValue]: The items held by the BaseContainer Class

        Examples:
            >>> container = BaseContainer((1, 2, 3))
            >>> container.items
            (BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int))
        """
        return self._items

    @property
    def type(self) -> Type[BaseContainerTypes().all | str]:
        """The type of the BaseContainer

        Returns:
            Type[BaseContainerTypes]: The type of the BaseContainer

        Examples:
            >>> container = BaseContainer((1, 2, 3))
            >>> container.type
            tuple
        """
        return self._type.__name__ if isinstance(self._type, type) else self._type

    @staticmethod
    def _unpack(item: BaseContainerTypes().all, type_: TypeAlias | type) -> BaseContainerTypes().all:
        """
        Repackages the container
        """
        base_container_types = BaseContainerTypes()
        type_from_alias: TypeAlias | type = base_container_types._get_type_from_alias(type_)
        match (str(type_from_alias)):
            case("<class 'list'>"):
                return [value.value for value in item]
            case("<class 'tuple'>"):
                return tuple([value.value for value in item])
            case("<class 'set'>"):
                return {value.value for value in item}
            case("<class 'frozenset'>"):
                return frozenset({value.value for value in item})
            case("<class 'dict'>"):
                keys: tuple[BaseValueTypes().all] = item[::2]
                values: tuple[BaseValueTypes().all] = item[1::2]
                return {key.value: value.value for key, value in zip(keys, values)}

    @override
    def __repr__(self) -> str:
        return f"BaseContainer(items={self.items}, type={self.type})"

    @override
    def __str__(self) -> str:
        return str(self._unpack(item=self.items, type_=self.type))
    
    def __iter_items__(self, slot_name: str = "_items"):
        """Returns an iterator over all slots.

        Returns:
            Iterator[str]: An iterator over all slots.
        """
        items: tuple = getattr(self, slot_name)

        # if isinstance(items, BaseValue | BaseValueTypes().all):
        #     yield items

        if isinstance(items, BaseContainerTypes().linear | BaseContainer):
            for value in items:
                yield value

        elif isinstance(items, BaseContainerTypes().named):
            for key, value in items.items():
                yield value
                yield key

    @override
    def __iter__(self):
        yield from self.__iter_items__()
    
    def _hash(self) -> MerkleTree:
        hashed_items: tuple[str] = ()
        for item in self.__iter_items__():
            hashed_items = hashed_items + (item._hash().root(), )

        hashed_items = hashed_items + (MerkleTree.hash_func(repr(self.type)), )

        return MerkleTree(hashed_items)

    def _verify_item(self, item: BaseValue) -> bool:
        # leaf_hash: str = MerkleTree.hash_func(repr(item))
        leaf_hash: str = item._hash().root()
        print(leaf_hash)
        tree = self._hash()
        print(tree.levels)

        return tree.verify(leaf_hash)