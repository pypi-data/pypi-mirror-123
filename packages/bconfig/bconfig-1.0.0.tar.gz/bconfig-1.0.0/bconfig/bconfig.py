import typing

T = typing.TypeVar('T')
C = typing.TypeVar('C')

Unspecified = object()

class Field(typing.Generic[T]):
    parse:typing.Callable[[T], typing.Any]

    def __init__(self,
        expected_type:typing.Type[T],
        parse:typing.Callable[[T], typing.Any],
        required=False,
        default=Unspecified
    ):
        self.expected_type = expected_type
        self.parse = parse
        self.required = required
        self.default = default

class Blueprint(
    Field[typing.Dict[str, typing.Any]],
    typing.Dict[str, Field]
):
    expected_type:typing.Type[typing.Dict[str, typing.Any]] = dict

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))
        self.default = dict()

        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = Blueprint(value)
    
    class MissingValue(Exception):
        def __init__(self, 
            path:typing.List[str],
            field:Field
        ):
            super().__init__(path, field)

            self.path = path
            self.field = field

    class UnexpectedValue(Exception):
        def __init__(self, 
            path:typing.List[str],
            field:Field,
            provided_value:typing.Any
        ):
            super().__init__(path, field, provided_value)

            self.path = path
            self.field = field
            self.provided_value = provided_value

    def parse(self, config:typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        result = dict()

        for key, field in self.items():
            parsed = self.__parse_item(config, key, field)

            if parsed is Unspecified:
                continue
            
            result[key] = parsed
        
        return result
    
    def __parse_item(self, config:typing.Dict[str, typing.Any], key:str, field:Field):
        if key in config:
            provided_value = config[key]

            if isinstance(provided_value, field.expected_type):
                try:
                    parsed_value = field.parse(provided_value)
                except (Blueprint.MissingValue, Blueprint.UnexpectedValue) as exc:
                    if isinstance(exc, Blueprint.MissingValue):
                        raise Blueprint.MissingValue(
                            [key] + exc.path, 
                            exc.field
                        ) from exc
                    elif isinstance(exc, Blueprint.UnexpectedValue):
                        raise Blueprint.UnexpectedValue(
                            [key] + exc.path, 
                            exc.field, 
                            exc.provided_value
                        ) from exc
            else:
                raise Blueprint.UnexpectedValue([key], field, provided_value)
        else:
            if field.required:
                raise Blueprint.MissingValue([key], field)
            else:
                parsed_value = field.default
        
        return parsed_value
    
    @property
    def required(self) -> bool:
        for spec in self.values():
            if spec.required:
                return True
        
        return False

class NamespaceSpec(type):
    def __call__(spec, config:typing.Dict[str, typing.Any]):
        return Namespace(spec).parse(config)

class Namespace(Field[typing.Dict[str, typing.Any]]):
    expected_type:typing.Type[typing.Dict[str, typing.Any]] = dict

    def __init__(self, spec:NamespaceSpec):
        self.spec = spec
        self.bp = Blueprint()

        declared_attributes = set(dir(spec))

        for key in declared_attributes:
            field = getattr(spec, key)

            if isinstance(field, Field):
                self.bp[key] = field
            elif isinstance(field, NamespaceSpec):
                self.bp[key] = Namespace(field)
        
        self.required = self.bp.required
    
    def parse(self, config:typing.Dict[str, typing.Any]):
        namespace = self.spec.__bases__[0]()

        for key, value in self.bp.parse(config).items():
            setattr(namespace, key, value)

        return namespace

L = typing.TypeVar('L', bound=type)

# A helper function with "lying" type hints
def ns(cls:L) -> L:
    class spec(cls, metaclass=NamespaceSpec): ...
    return spec