from __future__ import annotations
import typing as T
import json
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from .execute import execute, execute_async
from .gql import GQLException
from .dgraph_model import DGraphModel
from .node import Node


def parse_filter(filter: DGraphModel) -> str:
    print(f"{filter=}")
    return filter.to_gql_str()


def parse_nested_q(field_name: str, nested_q: BaseModel):
    if isinstance(nested_q, DGraphModel):
        filter_s = parse_filter(nested_q)
        return f"{field_name}: {{ {filter_s} }}"
    outer_lst: T.List[str] = []
    for key, val in nested_q:
        if val is None:
            continue
        # for order, not filter
        if not isinstance(val, BaseModel):
            outer_lst.append(f"{key}: {val}")
            continue
        val: BaseModel
        inner_lst: T.List[str] = []
        for inner_key, inner_val in val.dict(exclude_none=True).items():
            inner_str = f"{inner_key}: {json.dumps(jsonable_encoder(inner_val))}"
            inner_lst.append(inner_str)
        outer_lst.append(f'{key}: {{ {",".join(inner_lst)} }}')
    return f'{field_name}: {{ {",".join(outer_lst)} }}'


class Params(BaseModel):
    def to_str(self) -> str:
        field_names = self.dict(exclude_none=True).keys()
        inner_params: T.List[str] = []
        for field_name in field_names:
            val = getattr(self, field_name)
            if isinstance(val, BaseModel):
                inner_params.append(parse_nested_q(field_name=field_name, nested_q=val))
            else:
                inner_params.append(
                    f"{field_name}: {json.dumps(jsonable_encoder(val))}"
                )
        if inner_params:
            return f'({",".join(inner_params)})'
        return ""


NodeType = T.TypeVar("NodeType", bound=Node)
GetParamsType = T.TypeVar("GetParamsType", bound=Params)
QueryParamsType = T.TypeVar("QueryParamsType", bound=Params)
EdgesType = T.TypeVar("EdgesType", bound=BaseModel)


class Resolver(
    BaseModel, T.Generic[NodeType, GetParamsType, QueryParamsType, EdgesType]
):
    def __init__(
        self,
        query_params: T.Optional[QueryParamsType] = None,
        edges: T.Optional[EdgesType] = None,
    ):
        get_params = self.model.GQL.GetParams()
        query_params = query_params or self.model.GQL.QueryParams()
        edges = edges or self.model.GQL.Edges()
        super().__init__(get_params=get_params, query_params=query_params, edges=edges)

    model: T.ClassVar[T.Type[NodeType]]

    edges: EdgesType = Field(default_factory=Node.GQL.Edges)
    get_params: GetParamsType = Field(default_factory=Node.GQL.GetParams)
    query_params: QueryParamsType = Field(default_factory=Node.GQL.QueryParams)

    def gql_fields_str(self) -> str:
        """This does not include the top level..."""
        fields = [*self.model.__fields__.keys(), "__typename"]
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
        return f"get{cls.model.GQL.typename}"

    @classmethod
    def query_query_name(cls) -> str:
        return f"query{cls.model.GQL.typename}"

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
        node: NodeType = self.model.parse_obj(gql_d)
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
            typename = sub.model.GQL.typename
            if typename in d:
                raise GQLException(
                    f"Two Resolvers share the typename {typename}: ({sub.__name__}, {d[typename].__name__})"
                )
            d[typename] = sub
        return d
