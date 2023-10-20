from attrs import define, field, validators
from typing import Optional

from ..base.interface import BaseInterface
from ..base.container import BaseContainer


@define(frozen=True, slots=True, weakref_slot=False)
class Owner(BaseInterface):
    """The Owner class holds the owner of the Group Unit
    """

    _owner: Optional[BaseContainer] = field(
        validator=validators.optional(validators.instance_of(BaseContainer)),
        default=None)

    @property
    def owner(self) -> BaseContainer:
        return self._owner

