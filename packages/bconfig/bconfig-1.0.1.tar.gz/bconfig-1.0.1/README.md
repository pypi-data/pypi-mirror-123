# **bconfig** (Blueprint Configuration)

## Usage
```python
import bconfig

bp = bconfig.Blueprint({
    'mykey': bconfig.Field(str, int),
    'subconf': {
        'foo': bconfig.Field(str, float)
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

## Usage with namespaces
```python
import bconfig

@bconfig
class MyConf:
    mykey:int = bconfig.Field(str, int)

    @bconfig
    class subconf:
        foo:float = bconfig.Field(str, float)

mc = MyConf({
    'mykey': '123',
    'subconf': {
        'foo': '1.23'
    }
})

print(mc.mykey + 1) # 124
print(mc.subconf.foo + 0.01) # 1.24
```