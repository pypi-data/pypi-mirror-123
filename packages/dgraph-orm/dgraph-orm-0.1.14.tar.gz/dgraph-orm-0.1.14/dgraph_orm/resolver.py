from __future__ import annotations
import typing as T
import json
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from .execute import execute, execute_async
from .gql import GQLException
from .node import Node, Params


NodeType = T.TypeVar("NodeType", bound=Node)
ResolverType = T.TypeVar("ResolverType")


GetParamsType = T.TypeVar("GetParamsType", bound=Params)
QueryParamsType = T.TypeVar("QueryParamsType", bound=Params)
EdgesType = T.TypeVar("EdgesType", bound=BaseModel)


class Resolver(BaseModel):
    node: T.Type[NodeType]

    edges: EdgesType
    get_params: GetParamsType
    query_params: QueryParamsType

    @classmethod
    def from_node(
        cls: T.Type[ResolverType], node_cls: T.Type[NodeType]
    ) -> ResolverType:
        cls(
            node=node_cls,
            edges=node_cls.GQL.Edges(),
            get_params=node_cls.GQL.GetParams(),
            query_params=node_cls.GQL.QueryParams(),
        )
        return cls

    def gql_fields_str(self) -> str:
        """This does not include the top level..."""
        fields = [*self.node.__fields__.keys(), "__typename"]
        for resolver_name in self.edges.__fields__.keys():
            resolver: T.Optional[Resolver] = getattr(self.edges, resolver_name, None)
            if resolver:
                child_gql_str = resolver.params_and_fields()
                fields.append(f"{resolver_name} {child_gql_str}")
        return f'{{ {",".join(fields)} }}'

    def params_and_fields(self) -> str:
        return f"{self.query_params.to_str()}{self.gql_fields_str()}"

    def make_get_query_str(self, kwargs_d: dict) -> str:
        kwargs = {k: v for k, v in kwargs_d.items() if v is not None}
        if not kwargs:
            raise GQLException(
                f".get requires one field to be given of {list(kwargs_d.keys())}"
            )
        inner_params = ",".join(
            [
                f"{field_name}: {json.dumps(jsonable_encoder(val))}"
                for field_name, val in kwargs.items()
            ]
        )
        s = f"{{ {self.get_query_name()}({inner_params}){self.gql_fields_str()} }}"
        print(s)
        return s

    @classmethod
    def get_query_name(cls) -> str:
        return f"get{cls.node.GQL.typename}"

    @classmethod
    def query_query_name(cls) -> str:
        return f"query{cls.node.GQL.typename}"

    def make_query_query_str(self) -> str:
        s = f"{{ {self.query_query_name()}{self.params_and_fields()} }}"
        print(s)
        return s

    async def query_async(self) -> T.List[NodeType]:
        s = self.make_query_query_str()
        lst: T.List[dict] = (await execute_async(query_str=s))["data"][
            self.query_query_name()
        ]
        return [self.parse_obj_nested(d) for d in lst]

    def query(self) -> T.List[NodeType]:
        s = self.make_query_query_str()
        lst: T.List[dict] = execute(query_str=s)["data"][self.query_query_name()]
        return [self.parse_obj_nested(d) for d in lst]

    def parse_obj_nested(self, gql_d: dict) -> NodeType:
        node: NodeType = self.node.parse_obj(gql_d)
        other_fields = set(gql_d.keys()) - set(node.__fields__.keys()) - {"__typename"}
        for field in other_fields:
            resolver = getattr(self.edges, field, None)
            if not resolver:
                raise GQLException(f"No resolver {field} found!")
            nested_d = gql_d[field]
            value_to_save = nested_d
            if nested_d:
                val = (
                    [resolver.parse_obj_nested(d) for d in nested_d]
                    if type(nested_d) == list
                    else resolver.parse_obj_nested(nested_d)
                )
                value_to_save = val
            node.cache.add(key=field, resolver=resolver, val=value_to_save, gql_d=gql_d)
        return node

    def _get(self, kwargs_d: dict) -> T.Optional[NodeType]:
        s = self.make_get_query_str(kwargs_d=kwargs_d)
        obj = execute(query_str=s)["data"][self.get_query_name()]
        if obj:
            return self.parse_obj_nested(obj)
        return None

    async def _get_async(self, kwargs_d: dict) -> T.Optional[NodeType]:
        s = self.make_get_query_str(kwargs_d=kwargs_d)
        obj = (await execute_async(query_str=s))["data"][self.get_query_name()]
        if obj:
            return self.parse_obj_nested(obj)
        return None

    """
    def get(self, get_params: GetParamsType) -> T.Optional[NodeType]:
        return self._get(kwargs_d=get_params.dict())

    async def get_async(self, get_params: GetParamsType) -> T.Optional[NodeType]:
        return await self._get_async(kwargs_d=get_params.dict())

    def gerror(self, get_params: GetParamsType) -> NodeType:
        node = self.get(get_params=get_params)
        if not node:
            raise GQLException(f"Node with {get_params=} was None")
        return node
    """

    @staticmethod
    def resolvers_by_typename() -> T.Dict[str, T.Type[Resolver]]:
        d = {}
        subs = Resolver.__subclasses__()
        for sub in subs:
            typename = sub.node.GQL.typename
            if typename in d:
                raise GQLException(
                    f"Two Resolvers share the typename {typename}: ({sub.__name__}, {d[typename].__name__})"
                )
            d[typename] = sub
        return d
