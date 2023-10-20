from attrs import define, field, validators
from typing import Optional

from .unit import GroupUnit, Credential, Data, Owner, Nonce
from .pool import Pool


@define(slots=True, weakref_slot=False)
class Controller:
    """The Manage class holds the Group Manage data
    """
    pool: Optional[Pool] = field(
        default=None,
        validator=validators.optional(validators.instance_of(Pool)))
    
    _active: Optional[GroupUnit] = field(
        default=None,
        validator=validators.optional(validators.instance_of(GroupUnit)))

    def __init__(self, pool: Optional[Pool] = None):
        if pool is not None:
            self.pool = pool

        self._active = pool.group_units[-1][1]

    @property
    def active(self) -> GroupUnit | None:
        return self._active
    
    @active.setter
    def active(self, value: GroupUnit):
        self._active = value
