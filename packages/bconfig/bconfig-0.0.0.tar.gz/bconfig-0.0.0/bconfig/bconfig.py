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
            super().__init__(path, field.expected_type.__name__)

            self.path = path
            self.field = field

    class UnexpectedValue(Exception):
        def __init__(self, 
            path:typing.List[str],
            field:Field,
            provided_value:typing.Any
        ):
            super().__init__(path, field.expected_type.__name__, str(provided_value))

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
                if isinstance(field, Blueprint):
                    try:
                        parsed_value = field.parse(provided_value)
                    except (Blueprint.MissingValue, Blueprint.UnexpectedValue) as exc:
                        exc.path = [key] + exc.path
                        raise
                else:
                    parsed_value = field.parse(provided_value)
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

class Namespace(typing.Generic[C], Field[typing.Dict[str, typing.Any]]):
    expected_type:typing.Type[typing.Dict[str, typing.Any]] = dict

    def __init__(self, spec:typing.Type[C]):
        self.spec = spec
        self.bp = Blueprint()

        declared_attributes = set(dir(spec))

        for key in declared_attributes:
            field = getattr(spec, key)

            if isinstance(field, Field):
                self.bp[key] = field
    
    def parse(self, config:typing.Dict[str, typing.Any]) -> C:
        namespace = self.spec()

        for key, value in self.bp.parse(config).items():
            setattr(namespace, key, value)

        return namespace

class CallableNamespace(Namespace):
    __call__ = Namespace.parse

# A helper function with "lying" type hints
def ns(cls:C) -> C:
    return CallableNamespace(cls)