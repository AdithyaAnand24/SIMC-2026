---
tags:
  - simc
---

# Python Type Hints

## What it is

Type hints (a.k.a. **annotations**, added in Python 3.5, [PEP 484](https://peps.python.org/pep-0484/)) let you write the **expected types** of function parameters and return values directly in the function signature. They are ==pure documentation== — Python does not enforce them at runtime.

```python
def simulate_die_rolls(n: int) -> np.ndarray:
    ...
```

Reads as: *"function `simulate_die_rolls` takes parameter `n`, which should be an `int`, and returns a `np.ndarray`."*

| Part | Meaning |
|------|---------|
| `n: int` | parameter `n` should be an `int` |
| `-> np.ndarray` | function returns a `np.ndarray` |
| `:` at end of `def` line | the regular Python colon that opens the function body (NOT a type hint) |

## Java analogy

You already know this pattern from CSA — Java requires types everywhere:

```java
public int[] simulateDieRolls(int n) { ... }
```

Same intent. The critical difference:

| | Java | Python |
|---|---|---|
| Required? | **Yes** | **No** — optional |
| Enforced at runtime? | **Yes** — won't compile | **No** — interpreter ignores them |
| Without types? | Won't compile | Works identically |

These two Python functions behave **exactly the same** at runtime:

```python
def simulate_die_rolls(n: int) -> np.ndarray:
    return np.random.randint(1, 7, size=n)

def simulate_die_rolls(n):
    return np.random.randint(1, 7, size=n)
```

> [!warning] Type hints are not checked at runtime
> ```python
> simulate_die_rolls("hello")   # Python does NOT complain here
> ```
> The interpreter happily passes `"hello"` in. The crash (if any) happens **inside** the function when something downstream chokes on a string. To catch type errors *before* running, use a separate tool like `mypy` or `pyright`.

## Why bother?

1. **Self-documenting code.** Future-you reading `def cluster(data, k)` has no idea what `data` is. `def cluster(data: np.ndarray, k: int) -> np.ndarray` is unambiguous.
2. **IDE autocomplete.** VS Code, PyCharm, etc. use type hints to suggest methods and catch typos in real time.
3. **Static checkers** (`mypy`, `pyright`) verify type correctness before you run, catching whole classes of bugs.
4. **Team work.** When Vishnu or Adithya read your SIMC code, they shouldn't have to step through the body to figure out what a function returns.

## Common patterns

### Built-in scalar types

```python
n: int                # integer
prob: float           # float
name: str             # string
flag: bool            # boolean
nothing: None         # the None value (rarely annotated; usually return type)
```

### Containers

```python
items: list[int]              # list of ints
names: list[str]              # list of strings
data: dict[str, float]        # dict: str keys → float values
pair: tuple[int, int]         # 2-tuple of ints
record: tuple[str, int, float]  # heterogeneous tuple
flexible: set[int]            # set of ints
```

> [!info] Pre-3.9 syntax (you may see in older code)
> Older Python used `List[int]`, `Dict[str, float]`, etc. from the `typing` module. Python ≥ 3.9 lets you use the lowercase built-in names directly. Prefer the lowercase form.

### NumPy & pandas

```python
arr: np.ndarray                 # NumPy array (no shape/dtype info)
df: pd.DataFrame                # pandas DataFrame
series: pd.Series               # pandas Series
```

For more precision (rarely needed at SIMC level) you can use `numpy.typing.NDArray[np.float64]`.

### Return types

```python
def is_even(x: int) -> bool: ...
def make_array() -> np.ndarray: ...
def log_result(msg: str) -> None: ...      # returns nothing
def split(s: str) -> tuple[str, str]: ...   # returns a 2-tuple
```

### Optional and union

```python
def lookup(key: str) -> int | None:
    """Return the int for this key, or None if not found."""

def parse(value: int | float | str) -> float:
    """Accepts any of three types."""
```

`int | None` is the modern syntax (Python 3.10+) for "int or None." Older codebases write `Optional[int]` from the `typing` module — same thing.

### Callables (functions as parameters)

```python
from typing import Callable

def apply(
    func: Callable[[int], bool],   # func takes an int, returns a bool
    items: list[int],
) -> list[bool]:
    return [func(x) for x in items]
```

## Why this matters for SIMC

Even though SIMC code is short and self-contained, type hints save real time:

- **Reading teammate code.** Vishnu writes a function, you read its signature, you know the contract immediately — no need to ask or step through it.
- **Debugging.** When a NumPy crash blames "shape mismatch" three calls deep, type hints help you spot the wrong-thing-in-wrong-slot upstream.
- **Final report.** If you include code excerpts in the report, annotated signatures are vastly more readable for judges than bare `def f(x, y, z):`.

## Common mistakes

> [!warning] Don't treat hints as enforcement
> Python WILL let you pass the wrong type. If you absolutely need runtime checking, write an explicit `isinstance` check inside the function — the annotation alone won't save you.

> [!warning] Don't over-annotate trivial code
> A 3-line throwaway function doesn't need `Callable[[int, int], int]`. Reserve type hints for functions other people (including future-you) will call.

> [!warning] Don't confuse `:` (annotation) with `:` (block opener)
> ```python
> def f(x: int) -> int:    # first ':' is annotation, second is block opener
>     return x + 1
> ```
> Two roles, same character. Easy to mix up when you're new to the syntax.

## Sources

- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/) — the original proposal
- [Python docs: typing module](https://docs.python.org/3/library/typing.html)
- [mypy documentation — Python Type Checker](https://mypy.readthedocs.io/)
