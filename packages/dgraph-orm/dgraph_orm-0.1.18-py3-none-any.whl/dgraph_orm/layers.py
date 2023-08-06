import typing as T
import dgraph_orm

NodeType = T.TypeVar("NodeType", bound=dgraph_orm.Node)
ResolverType = T.TypeVar("ResolverType", bound=dgraph_orm.Resolver)
StrawType = T.TypeVar("StrawType")


class Display(T.Generic[NodeType]):
    id: str

    @classmethod
    def from_node(
        cls: T.Type[StrawType], node: T.Optional[NodeType]
    ) -> T.Optional[StrawType]:
        if node is None:
            return None
        fields_to_use = set(cls.__dataclass_fields__.keys()) & set(
            node.__fields__.keys()
        )
        straw = cls(**node.dict(include=fields_to_use))
        straw._node = node
        return straw

    @classmethod
    def from_node_lst(
        cls: T.Type[StrawType], nodes: T.List[NodeType]
    ) -> T.List[StrawType]:
        return [cls.from_node(node) for node in nodes]

    @property
    def node(self) -> NodeType:
        if not getattr(self, "_node", None):
            self._node = self.Dgraph.node.resolver._get({"id": self.id})
        return self._node

    class Dgraph:
        node: T.Type[NodeType]


DBType = T.TypeVar("DBType", bound=dgraph_orm.Node)
MainType = T.TypeVar("MainType", bound=dgraph_orm.Node)


class Node(T.Generic[DBType]):
    @classmethod
    def from_db(
        cls: T.Type[MainType], db_model: T.Optional[DBType]
    ) -> T.Optional[MainType]:
        if not db_model:
            return None
        return cls(**db_model.dict())

    @classmethod
    def from_db_lst(
        cls: T.Type[MainType], db_models: T.List[DBType]
    ) -> T.List[MainType]:
        return [cls.from_db(db_model) for db_model in db_models]
