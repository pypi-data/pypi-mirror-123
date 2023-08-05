# **bconfig** (Blueprint Configuration)

## Typical usage
```python
from bconfig import Blueprint, Field

bp = Blueprint({
    'mykey': Field(str, int),
    'subconf': {
        'foo': Field(str, float)
    }
})

mc = bp.parse({
    'mykey': '123',
    'subconf': {
        'foo': '1.23'
    }
})

print(mc['mykey'] + 1) # 124
print(mc['subconf']['foo'] + 0.01) # 1.24
```

## Usage with `ns`
```python
from bconfig import ns, Field

@ns
class MyConf:
    mykey:int = Field(str, int)

    @ns
    class subconf:
        foo:float = Field(str, float)

mc = MyConf({
    'mykey': '123',
    'subconf': {
        'foo': '1.23'
    }
})

print(mc.mykey + 1) # 124
print(mc.subconf.foo + 0.01) # 1.24
```