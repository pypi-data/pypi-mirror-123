from typing import Any

class Field:
    repeated: bool
    mcls_data: Any
    parent: Any
    number: Any
    proto_type: Any
    message: Any
    enum: Any
    json_name: Any
    optional: Any
    oneof: Any
    def __init__(
        self,
        proto_type,
        number: int,
        *,
        message: Any | None = ...,
        enum: Any | None = ...,
        oneof: str = ...,
        json_name: str = ...,
        optional: bool = ...
    ) -> None: ...
    @property
    def descriptor(self): ...
    @property
    def name(self) -> str: ...
    @property
    def package(self) -> str: ...
    @property
    def pb_type(self): ...

class RepeatedField(Field):
    repeated: bool

class MapField(Field):
    map_key_type: Any
    def __init__(
        self,
        key_type,
        value_type,
        number: int,
        *,
        message: Any | None = ...,
        enum: Any | None = ...
    ) -> None: ...
