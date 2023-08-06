from __future__ import annotations
import typing as T
import json
import time
from pydantic import BaseModel, PrivateAttr
from fastapi.encoders import jsonable_encoder
from .gql import GQLException


def d_rez(refresh: bool = False, use_stale: bool = False, returns: T.Type = None):
    """The problem w this is it does not do types"""

    def outer(f: T.Callable):
        def inner(
            *args, refresh: bool = refresh, use_stale: bool = use_stale, **kwargs
        ) -> returns:
            resolver = f(*args, **kwargs)
            return args[0].resolve(
                name=f.__name__, resolver=resolver, refresh=refresh, use_stale=use_stale
            )

        return inner

    return outer


class Cache(BaseModel):
    val: T.Union[Node, T.List[Node], None]
    resolver: Resolver
    timestamp: float
    raw_gql: str


class CacheManager(BaseModel):
    cache: T.Dict[str, Cache] = {}

    def remove(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

    def add(self, *, key: str, resolver: Resolver, val: T.Any, gql_d: dict) -> None:
        self.cache[key] = Cache(
            val=val,
            resolver=resolver,
            timestamp=time.time(),
            raw_gql=json.dumps(jsonable_encoder(gql_d)),
        )

    def replace(self, key: str, cache: Cache) -> None:
        self.cache[key] = cache

    def get(self, key: str) -> T.Optional[Cache]:
        if key not in self.cache:
            return None
        return self.cache[key]

    def exists(self, key: str) -> bool:
        return key in self.cache

    def get_val(self, key: str) -> T.Optional[T.Union[Node, T.List[Node]]]:
        if c := self.cache[key]:
            return c.val

    def clear(self) -> None:
        self.cache = {}

    def is_empty(self) -> bool:
        return len(self.cache) == 0


NodeModel = T.TypeVar("NodeModel", bound="Node")


class Node(BaseModel):
    _cache: CacheManager = PrivateAttr(default_factory=CacheManager)

    id: str

    # TODO make equality and hashing

    @property
    def cache(self) -> CacheManager:
        return self._cache

    @staticmethod
    def nodes_by_typename() -> T.Dict[str, T.Type[Node]]:
        d = {}
        subs = Node.__subclasses__()
        for sub in subs:
            typename = sub.GQL.typename
            if typename in d:
                raise GQLException(
                    f"Two Nodes share the typename {typename}: ({sub.__name__}, {d[typename].__name__})"
                )
            d[typename] = sub
        return d

    def __repr__(self) -> str:
        r = super().__repr__()
        r = f"{r}, cache: {repr(self.cache)}" if not self.cache.is_empty() else r
        return r

    def get_root_resolver(self) -> T.Type[Resolver]:
        return Resolver.resolvers_by_typename()[self.GQL.typename]

    @staticmethod
    def should_use_new_resolver(
        old_r: Resolver, new_r: Resolver, strict: bool = False
    ) -> bool:
        old_r_j = old_r.json()
        new_r_j = new_r.json()
        if old_r_j == new_r_j:
            return False
        if strict:
            return True
        if old_r.json(exclude={"edges"}) != new_r.json(exclude={"edges"}):
            print(
                f'excluding children resolvers here..., {old_r.json(exclude={"edges"})=}, {new_r.json(exclude={"edges"})=}'
            )
            return True
        # now do the same for children
        for child_resolver_name in new_r.edges.__fields__.keys():
            new_child_resolver = getattr(new_r.edges, child_resolver_name)
            if new_child_resolver:
                old_child_resolver = getattr(old_r.edges, child_resolver_name)
                if not old_child_resolver:
                    return True
                if Node.should_use_new_resolver(
                    old_r=old_child_resolver,
                    new_r=new_child_resolver,
                    strict=strict,
                ):
                    return True
        return False

    def resolve(
        self,
        name: str,
        resolver: Resolver,
        refresh: bool = False,
        strict: bool = False,
        use_stale: bool = False,
    ) -> T.Optional[T.Union[NodeModel, T.List[NodeModel]]]:
        if refresh:
            self.cache.remove(name)
        # see if the resolvers do not match
        if cache := self.cache.get(name):
            if use_stale:
                return cache.val
            if self.should_use_new_resolver(
                old_r=cache.resolver, new_r=resolver, strict=strict
            ):
                print(
                    f"resolvers are different, removing {name} from cache, old: {cache.resolver=}, new: {resolver=}"
                )
                self.cache.remove(name)
        if not self.cache.exists(name):
            root_resolver = self.get_root_resolver()
            get_params = self.GQL.GetParams(id=self.id)
            edge_params = self.GQL.Edges.parse_obj({name: resolver})
            obj = root_resolver(edges=edge_params).get(get_params)
            self.cache.replace(key=name, cache=obj.cache.get(name))
        return self.cache.get_val(name)

    class GQL:
        typename: T.ClassVar[str]

        class GetParams(BaseModel):
            id: T.Optional[str] = None  # TODO this should be no None right?

        class QueryParams(BaseModel):
            pass

        class Edges(BaseModel):
            pass

        resolver: Resolver = None


from .resolver import Resolver

Cache.update_forward_refs()
