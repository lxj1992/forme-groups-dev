import itertools
import hashlib
from abc import ABCMeta, abstractmethod, ABC
from attrs import define, field, validators, converters
from typing import TypeAlias, Optional, Any
from .types import number, text, named_container, linear_container, containers, object_, unit_value_types, key_value, unit_types, type_set, type_container, type_containers_dict, schema
from .converters import _convert_container_to_value, _convert_container_to_type, _convert_container_to_default


def hash_sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


@define(slots=True, weakref_slot=False)
class BaseInterface(ABC):
    """
    Base interface for all classes
    """
    def _get_slots(self):
        for slot in self.__slots__:
            yield slot

    def __iter__(self):
        yield from self._get_slots()


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue(BaseInterface):
    """
    Base class for all classes
    """
    
    _value: unit_value_types = field(validator=validators.instance_of(unit_types), converter=_convert_container_to_value)

    @property
    def value(self) -> unit_value_types:
        return self._value

    def __str__(self) -> str:
        return str(self._value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.__str__()})"
        

@define(slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    """
    Base class for all classes
    """
    _items: tuple[BaseValue] = field(validator=validators.deep_iterable(validators.instance_of(unit_types)))
    _type: Optional[type] = field(validator=validators.optional(validators.instance_of(unit_types)), default=None, init=False)

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        self._type = _convert_container_to_type(args[0])
        self._items = self._convert_container_to_base_values(args[0])

    @property
    def items(self) -> tuple[BaseValue]:
        return self._items
    
    @property
    def type(self) -> TypeAlias | type:
        return self._type
    
    @staticmethod
    def _extract_base_values(item: unit_types) -> tuple[BaseValue]:
        """
        Converts container to base values
        """
        items_to_return: tuple[BaseValue]
        if isinstance(item, linear_container):
            print(Exception("Passed a container of values, but expected a container of base values, a tuple of BaseValue will be returned"))

            if isinstance(item, list | tuple):
                items_to_return = tuple([BaseValue(value) for value in item])

            elif isinstance(item, set):
                items_to_return = tuple([BaseValue(item.pop()) for _ in range(len(item))])

            elif isinstance(item, frozenset):
                items = set(item)
                items_to_return = tuple([BaseValue(items.pop()) for _ in range(len(items))])

        elif isinstance(item, named_container):
            keys: tuple[unit_value_types] = tuple(item.keys())
            values: tuple[unit_value_types] = tuple(item.values())
            items_to_return = tuple([BaseValue(value) for value in itertools.chain(keys, values)])

        return items_to_return

    
    def _package(self) -> unit_types:
        return _convert_container_to_default(self._items, self._type)
    
    def __iter__(self):
        yield from self._items
    
    def __str__(self) -> str:
        return str(self._package())
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={[item for item in iter(self)]}, type={self._type})"

    
@define(slots=True, weakref_slot=False)
class BaseSchema(BaseInterface):
    """
    Describes the data structure of a container
    Data Schemas can be nested

    Example Schema:
    ```python
    address_schema = {
        "street": "string",
        "city": "string",
        "state": "string",
        "zip": "string"
    }
    person_schema = {
        "name": "string",
        "age": "number",
        "address": "schema:address_schema"
    }
    ```
    """
    _schema: dict[str, Any] = field(validator=validators.instance_of(dict))

    def _sub_schema(self) -> list[schema]:
        sub_schemas: list['BaseSchema' | str] = []
        for key, value in self._schema.items():
            if isinstance(value, BaseSchema):
                sub_schemas.append({key: value})
            elif isinstance(value, str):
                if value.startswith("schema:"):
                    sub_schemas.append({key: value})

        return sub_schemas

    def _sub_containers(self) -> list[type_containers_dict]:
        sub_units: list[str] = []
        for key, value in self._schema.items():
            if isinstance(value, BaseContainer):
                sub_units.append({key: value})
            if isinstance(value, str):
                if value.startswith("list") or value.startswith("tuple") or value.startswith("set") or value.startswith("frozenset") or value.startswith("dict") or isinstance(value, containers):
                    sub_units.append({key: value})

        return sub_units
    
    def _get_key_types_from_schema(self) -> type_set:
        key_types: tuple[key_value] = ()
        for dict_ in iter(self):
            for key, value in dict_.items():
                if isinstance(value, type(self).__class__):
                    unpacked = self._unpack_schema(value)
                    key_types = key_types + ((item, ) for item in unpacked)
                else:
                    key_types = key_types + (value, )
            # print(key_types)
        return set(key_types)

    def _unpack_schema(self, schema: 'BaseSchema') -> schema:
        schema_unpacked: dict[str, Any] = {}
        for item in iter(schema):
            for key, value in item.items():
                schema[key] = value
        return schema_unpacked
    
    def _unpack_type_containers(self, type_container_: text | containers):
        # unpacked: type_set = []
        # for type_container in self._sub_containers(type_container_):
        # for type_container in self._sub_containers():
        #     key, key_type = type_container.popitem()

        itnermediate_type: list[text] = []
        key_types: type_container = []
        key_types.append(type_container_)
        for key_type in key_types:
            if isinstance(type_container_, text):
                print(key_type)
                if key_type.startswith("schema:"):
                    return key_type
                if key_type.startswith("list["):
                    key_type = key_type[:-1].replace("list[", "")
                elif key_type.startswith("tuple[") or key_type.startswith("tuple("):
                    key_type = key_type[:-1].replace("tuple[", "") or key_type[:-1].replace("tuple(", "")
                elif key_type.startswith("set[") or key_type[:-1].startswith("set{") or key_type[:-1].startswith("set("):
                    key_type = key_type[:-1].replace("set{", "") or key_type[:-1].replace("set[", "") or key_type[:-1].replace("set(", "")
                elif key_type.startswith("frozenset({") or key_type.startswith("frozenset(") or key_type.startswith("frozenset["):
                    key_type = key_type[:-1].replace("frozenset({", "").replace("})", "") or key_type[:-1].replace("frozenset[", "") or key_type[:-1].replace("frozenset(", "")

                elif key_type.startswith("dict{") or key_type.startswith("dict["):
                    # print(key_type)
                    key_type = key_type[5:-1]
                    print(key_type)
                if "[" in key_type or "{" in key_type or "(" in key_type:
                    return self._unpack_type_containers(key_type)
                else:
                    values = key_type.split(", ")
                    print(f"key_type: {key_type}")
                    return self._unpack_type_containers(values)

            elif isinstance(key_type, containers):
                return self._unpack_type_containers(str(key_type))

            verified, err_msg = self._verify_base_types(key_type)
            if verified is False:
                if self._unpack_type_containers(key_type) not in key_types:
                    return self._unpack_type_containers(key_types)

        return key_types
    
    def _unpack_nested_type_strings(self, nested_key_types: type_set) -> type_set:
        unpacked: type_set = []
        for key_type in nested_key_types:
            unpacked.append(self._unpack_type_containers(key_type))
        
        return unpacked

    def _verify_base_types(self, base_types: type_set) -> (bool, text | None):
        verified: bool = True
        err_msg: text | None = ""

        for key_type in base_types:
            match (key_type):
                case("schema" | "schema:"):
                    continue
                case("bool" | "boolean"):
                    continue
                case("int" | "integer"):
                    continue
                case("float" | "number"):
                    continue
                case("str" | "string"):
                    continue
                case("bytes" | "byte"):
                    continue
                case(_):
                    verified = False
                    err_msg += f"Key type '{key_type}' is not valid. "
        
        return verified, err_msg

            
    def _verify_schema(self) -> (bool, str | None):
        """
        Verifies that the schema is valid
        """
        invalid_types: list[text] = []
        valid_types: list[text] = []
        verified: bool = True
        err_msg: str | None = ""

        key_types: type_set = self._get_key_types_from_schema()
        key_types = self._unpack_nested_type_strings(key_types)
        # print(key_types)

        # key_types.add(set(self._unpack_nested_types(key_types)))
        verified, err_msg = self._verify_base_types(key_types)

        # if verifies is False:
        #     verified = False
        #     err_msg += err_msg

        
            
            
                    


                    # if key_type.startswith("schema:") or key_type.startswith("schema"):
                    #     continue

                    # elif key_type.startswith("list") or key_type.startswith("tuple") or key_type.startswith("set") or key_type.startswith("frozenset") or key_type.startswith("dict") or isinstance(key_type, containers):
                    #     if key_type.startswith("list"):
                    #         key_type = key_type.replace("list[", "")
                    #     elif key_type.startswith("tuple"):
                    #         key_type = key_type.replace("tuple[", "")
                    #     elif key_type.startswith("set"):
                    #         key_type = key_type.replace("set{", "").replace("}", "")
                    #     elif key_type.startswith("frozenset"):
                    #         key_type = key_type.replace("frozenset({", "").replace("})", "")
                    #     elif key_type.startswith("dict"):
                    #         key_type = key_type.replace("dict{", "").replace("}", "")
                    #     elif isinstance(key_type, containers):
                    #         key_type = type(key_type)

                    #     print(str(key_type))
                    #     if eval(str(key_type)) is not None:
                    #         continue
                    #     else:
                    #         verified = False
                    #         err_msg += f"Key type '{key_type}' is not valid. "
                    #         # return False, f"Key type '{key_type}' is not valid"
                        
                    # elif (key_type == "bool") or (key_type == "boolean"):
                    #     key_type = bool
                    
                    # elif (key_type == "int") or (key_type == "integer"):
                    #     key_type = int

                    # elif (key_type == "float") or (key_type == "number"):
                    #     key_type = float

                    # elif (key_type == "str") or (key_type == "string"):
                    #     key_type = str

                    # elif (key_type == "bytes") or (key_type == "byte"):
                    #     key_type = bytes
                    # else:
                    #     verified = False
                    #     err_msg += f"Key type '{key_type}' is not valid. "
                    #     # return False, f"Key type '{key_type}' is not valid"          
            #     except Exception:
            #         verified = False
            #         err_msg += f"Key type '{key_type}' is not valid. "
            #         # return False, f"Key type '{key_type}' is not valid"

            # elif isinstance(key_type, type):
            #     continue
            
        return verified, err_msg

    def __iter__(self):
        for key, value in self._schema.items():
            if isinstance(value, BaseSchema):
                yield {key: "schema"}
                yield from [item for item in iter(value)]
            else:
                yield {key: value}

