# Python-Type-Check
> 由于python是动态语言的原因，类型检查是不被提供的。但是平时大多时候还是需要确保参数类型的。

## 目前功能
- 对于str,int,list,tuple等一般传统类型和一般的_GenericAlias类型检查自动支持
- 支持typing.Union类型的自动类型检查

## 目前问题
- 对于typing.AnyStr,typing.SupportsInt等类型不支持

## 快速上手
直接引入,作需要提供类型检查的装饰器即可。

```python
import type_check
import typing

@type_check
def foo(a:int,b:typing.List)->typing.Tuple:
    return a, b
```
