# BitAware

Bitwise Toolbox

[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![ruff](https://github.com/wnowicki/bitaware/workflows/Ruff/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![pytest](https://github.com/wnowicki/bitaware/workflows/Pytest/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![pylint](https://github.com/wnowicki/bitaware/workflows/Pylint/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![markdown](https://github.com/wnowicki/bitaware/workflows/Markdown%20Lint/badge.svg)](https://github.com/wnowicki/bitaware/actions?query=branch%3Amain)
[![License: GPLv3](https://img.shields.io/badge/License-MIT-blue.svg)](https://license.md/licenses/mit-license/)

## Usage

### Define

```python
from bitaware import BitFlag, BitwiseAware

class PermissionTypes(BitFlag):
    ADMIN = 1
    USER = 2
    GUEST = 4
    MODERATOR = 8

class UserPermission(BitwiseAware[PermissionTypes]):
    def __init__(self, value: int):
        super().__init__(value, PermissionTypes)
    pass
```

### Use

Standalone:

```python
permission = UserPermission(Types.ADMIN | Types.USER)

print(perm.has(Types.ADMIN))  # True
print(perm.has(Types.GUEST))  # False
```

As Pydantic field:

```python
class User(BaseModel):
    permissions: UserPermission
```

## Test

```shell
uv run pytest
```

## Security

If you discover any security-related issues, please email [email](mailto:wnowicki@me.com) instead of using the issue tracker.

---
Copyright (c) 2025 Wojciech Nowicki
