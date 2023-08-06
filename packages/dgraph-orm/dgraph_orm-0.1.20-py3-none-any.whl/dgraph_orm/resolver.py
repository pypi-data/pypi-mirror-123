from __future__ import annotations
import typing as T
import json
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from . import execute
from .gql import GQLException
from .node import Node, Params


NodeType = T.TypeVar("NodeType", bound=Node)

GetParamsType = T.TypeVar("GetParamsType", bound=Params)
QueryParamsType = T.TypeVar("QueryParamsType", bound=Params)
EdgesType = T.TypeVar("EdgesType", bound=BaseModel)


class Resolver(BaseModel, T.Generic[NodeType]):
    node: T.ClassVar[T.Type[NodeType]]

    get_params: GetParamsType
    query_params: QueryParamsType
    edges: EdgesType

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
        return f"get{cls.node.Dgraph.typename}"

    @classmethod
    def query_query_name(cls) -> str:
        return f"query{cls.node.Dgraph.typename}"

    def make_query_query_str(self) -> str:
        s = f"{{ {self.query_query_name()}{self.params_and_fields()} }}"
        print(s)
        return s

    def make_add_query_str(self) -> str:
        s = f"{{ {self.node.Dgraph.payload_node_name}{self.params_and_fields()} }}"
        return s

    def make_add_mutation_str(self) -> str:
        typename = self.node.Dgraph.typename
        s = f"""
            mutation Add{typename}($input: [Add{typename}Input!]!, $upsert: Boolean) {{
                add{typename}(input: $input, upsert: $upsert) {self.make_add_query_str()}
            }}
        """
        return s

    def make_update_mutation_str(self) -> str:
        typename = self.node.Dgraph.typename
        s = f"""
            mutation Update{typename}($set: {typename}Patch, $remove: {typename}Patch, $filter: {typename}Filter!) {{
                update{typename}(input: {{filter: $filter, set: $set, remove: $remove}}) {self.make_add_query_str()}
            }}
        """
        return s

    async def query(self) -> T.List[NodeType]:
        s = self.make_query_query_str()
        lst: T.List[dict] = (await execute.gql(query_str=s))["data"][
            self.query_query_name()
        ]
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
        node._used_resolver = self
        node._original_dict = node.dict()
        return node

    async def _get(self, kwargs_d: dict) -> T.Optional[NodeType]:
        s = self.make_get_query_str(kwargs_d=kwargs_d)
        obj = (await execute.gql(query_str=s))["data"][self.get_query_name()]
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
            typename = sub.node.Dgraph.typename
            if typename in d:
                raise GQLException(
                    f"Two Resolvers share the typename {typename}: ({sub.__name__}, {d[typename].__name__})"
                )
            d[typename] = sub
        return d
