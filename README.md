# BitAware

Bitwise Toolbox

[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![ruff](https://github.com/wnowicki/bitaware/workflows/Ruff/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![pytest](https://github.com/wnowicki/bitaware/workflows/Pytest/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![markdown](https://github.com/wnowicki/bitaware/workflows/Markdown%20Lint/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![License: GPLv3](https://img.shields.io/badge/License-MIT-blue.svg)](https://license.md/licenses/mit-license/)

## Usage

### Define

```python
from bitaware import BitFlag, BitAware

class PermissionTypes(BitFlag):
    READ = 1
    CREATE = 2
    EDIT = 4
    ADMIN = 8


class UserPermission(BitAware[PermissionTypes]):
    def __init__(self, value: int):
        super().__init__(value, PermissionTypes)

    pass

    # "User Roles" Named sets can be used interchangeably
    READER = PermissionTypes.READ
    CREATOR = PermissionTypes.CREATE | PermissionTypes.READ
    EDITOR = PermissionTypes.EDIT | PermissionTypes.READ
```

### Simple Use

Standalone:

```python
permission = UserPermission(PermissionTypes.ADMIN | PermissionTypes.READ)

print(permission.has(PermissionTypes.ADMIN))  # True
print(permission.has(PermissionTypes.CREATE))  # False
```

### Pydantic

As Pydantic field:

```python
class User(BaseModel):
    name: str
    permissions: UserPermission
```

Usage

```python
user = User(name="test_user", permissions=UserPermission.READER)
admin = User(name="admin_user", permissions=PermissionTypes.READ | PermissionTypes.ADMIN)

print(user.model_dump_json(indent=2))
```

Above code will print:

```json
{
  "name": "test_user",
  "permissions": 1
}
```

### Misc

```python
x = UserPermission(12)

print(str(x)) # EDIT|ADMIN [EDIT, ADMIN]
print(repr(x)) # UserPermission(PermissionTypes.EDIT | PermissionTypes.ADMIN)
print(list(x)) # [<PermissionTypes.EDIT: 4>, <PermissionTypes.ADMIN: 8>]
```

For predefined named flag set:

```python
x = UserPermission(UserPermission.CREATOR)

print(str(x)) # CREATOR [READ, CREATE]
print(repr(x)) # UserPermission(PermissionTypes.READ | PermissionTypes.CREATE)
print(list(x)) # [<PermissionTypes.READ: 1>, <PermissionTypes.CREATE: 2>]
```

Predefined named flag sets:

```python
print(UserPermission.properties()) # {<PermissionTypes.READ|CREATE: 3>: 'CREATOR', <PermissionTypes.READ|EDIT: 5>: 'EDITOR', <PermissionTypes.READ: 1>: 'READER'}
```

## Test

```shell
uv run pytest
```

## Security

If you discover any security-related issues, please email [email](mailto:wnowicki@me.com) instead of using the issue tracker.

---
Copyright (c) 2025 Wojciech Nowicki
