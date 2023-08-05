import operator
import sys
from abc import ABC
from datetime import datetime
from typing import Any, Callable, Dict, Generic, Iterator, Mapping, Optional, Sequence, TypeVar

from psutil import virtual_memory

# noinspection PyProtectedMember
from pocketutils.core._internal import nicesize

K = TypeVar("K", covariant=True)
V = TypeVar("V", contravariant=True)


class MemCachePolicy(Generic[K, V]):
    def should_archive(self) -> bool:
        raise NotImplementedError()

    def can_archive(self) -> bool:
        raise NotImplementedError()

    def reindex(self, items: Mapping[K, V]) -> None:
        raise NotImplementedError()

    def items(self) -> Iterator[K]:
        # TODO this is not overloaded!!
        raise NotImplementedError()

    def accessed(self, key: K) -> None:
        pass

    def added(self, key: K, value: V) -> None:
        pass

    def removed(self, key: K) -> None:
        pass


class MemoryLimitingPolicy(MemCachePolicy, ABC):
    def __init__(
        self,
        max_memory_bytes: Optional[int] = None,
        max_fraction_available_bytes: Optional[float] = None,
    ):
        self._max_memory_bytes = max_memory_bytes
        self._max_fraction_available_bytes = max_fraction_available_bytes
        self._total_memory_bytes = 0
        self._usage_bytes = {}  # type: Dict[K, int]
        self._last_accessed = {}  # type: Dict[K, datetime]
        self._created = {}  # type: Dict[K, datetime]

    def can_archive(self) -> bool:
        return len(self._last_accessed) > 0

    def should_archive(self) -> bool:
        return (
            self._max_memory_bytes is not None and self._total_memory_bytes > self._max_memory_bytes
        ) or (
            self._max_fraction_available_bytes is not None
            and self._total_memory_bytes
            > virtual_memory().available * self._max_fraction_available_bytes
        )

    def reindex(self, items: Mapping[K, V]) -> None:
        for key in set(self._last_accessed.keys()) - set(items.keys()):
            if key not in items.keys():
                self.removed(key)
        for key, value in items.items():
            self._usage_bytes[key] = sys.getsizeof(value)
        self._total_memory_bytes = sum(self._usage_bytes.values())

    def accessed(self, key: K) -> None:
        self._last_accessed[key] = datetime.now()

    def added(self, key: K, value: V) -> None:
        now = datetime.now()
        self._created[key] = now
        self._last_accessed[key] = now
        self._usage_bytes[key] = sys.getsizeof(value)
        self._total_memory_bytes += self._usage_bytes[key]

    def removed(self, key: K) -> None:
        self._total_memory_bytes -= self._usage_bytes[key]
        del self._last_accessed[key]
        del self._created[key]
        del self._usage_bytes[key]

    def __str__(self):
        available = virtual_memory().available
        name = self.__class__.__name__
        n_items = len(self._usage_bytes)
        real = nicesize(self._total_memory_bytes)
        cap_raw = "-" if self._max_memory_bytes is None else nicesize(self._max_memory_bytes)
        cap_percent = (
            "-"
            if self._max_fraction_available_bytes is None
            else nicesize(available * self._max_fraction_available_bytes)
        )
        percent = (
            "-"
            if self._max_fraction_available_bytes is None
            else round(
                100 * self._total_memory_bytes / (available * self._max_fraction_available_bytes),
                3,
            )
        )
        return f"{name}(n={n_items}, {real}/{cap_raw}, {real}/{cap_percent}={percent}%"

    def __repr__(self):
        ordered = list(self.items())
        ss = []
        current_day = None
        for k in ordered:
            dt = self._last_accessed[k]
            if current_day is None or current_day.date() != dt.date():
                current_day = dt
                ss.append("#" + current_day.strftime("%Y-%m-%d") + "...")
            nice = nicesize(self._usage_bytes[k])
            access = self._last_accessed[k].strftime("%H:%M:%S")
            ss.append(f"{k}:{nice}@{access}")
        return f"{str(self)}@{hex(id(self))}: [{', '.join(ss)}]"


class MemoryLruPolicy(MemoryLimitingPolicy):
    def items(self) -> Iterator[K]:
        return iter([k for k, v in sorted(self._last_accessed.items(), key=operator.itemgetter(1))])


class MemoryMruPolicy(MemoryLimitingPolicy):
    def items(self) -> Iterator[K]:
        rev = reversed(sorted(self._last_accessed.items(), key=operator.itemgetter(1)))
        return iter([k for k, v in rev])


class MemCache(Generic[K, V]):
    def __init__(
        self, loader: Callable[[K], V], policy: MemCachePolicy, *, log: Callable[[str], Any]
    ):
        self._loader = loader
        self._items = {}  # type: Dict[K, V]
        self._policy = policy
        self._log = lambda _: None if log is None else log

    def __getitem__(self, key: K) -> V:
        self._policy.accessed(key)
        if key in self._items:
            return self._items[key]
        else:
            value = self._loader(key)
            self._log(f"Loaded {key}")
            self._items[key] = value
            self._policy.added(key, value)
            self.archive()
            return value

    def __call__(self, key: K) -> V:
        return self[key]

    def archive(self, at_least: Optional[int] = None) -> Sequence[K]:
        it = self._policy.items()
        archived = []
        while self._policy.can_archive() and (
            at_least is not None and len(archived) < at_least or self._policy.should_archive()
        ):
            key = next(it)
            self._policy.removed(key)
            del self._items[key]
            archived.append(key)
            self._log(f"Archived {len(archived)} items: {archived}")
        return archived

    def clear(self) -> None:
        it = self._policy.items()
        cleared = []
        while self._policy.can_archive():
            key = next(it)
            self._policy.removed(key)
            del self._items[key]
            cleared.append(key)
        self._log(f"Cleared {len(cleared)} items: {cleared}")

    def remove(self, key: K) -> None:
        if key in self:
            self._policy.removed(key)
            del self._items[key]

    def __contains__(self, key: K):
        return key in self._items

    def __delitem__(self, key):
        self.remove(key)

    def __repr__(self):
        return str(self) + "@" + hex(id(self))

    def __str__(self):
        return f"{self.__class__.__name__}({repr(self._policy)})"


__all__ = [
    "MemCachePolicy",
    "MemCache",
    "MemoryLimitingPolicy",
    "MemoryLruPolicy",
    "MemoryMruPolicy",
]
