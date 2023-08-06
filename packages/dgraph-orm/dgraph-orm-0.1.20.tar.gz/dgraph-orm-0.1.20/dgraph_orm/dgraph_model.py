import typing as T
from enum import Enum
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from .gql import GQLException


class DGraphModel(BaseModel):
    def dict(self, *args, **kwargs) -> dict:
        d = super().dict(*args, **kwargs)
        for key in list(d.keys()):
            if key[-1] == "_":
                d[key[:-1]] = d[key]
                del d[key]
        return d

    def to_gql_str(self) -> str:
        str_lst: T.List[str] = []
        for field_name in self.dict(exclude_none=True):
            val = getattr(self, field_name, None)
            if val is None:
                val = getattr(self, f"{field_name}_")
            if type(val) is list:
                if len(val) == 0:
                    raise GQLException(f"List in filter cannot be empty, {self=}")
                if isinstance(val[0], Enum):
                    v_str = ",".join(f"{v.value}" for v in val)
                    s = f"{field_name}: [{v_str}]"
                    str_lst.append(s)
                elif isinstance(val[0], DGraphModel):
                    s = f'{field_name}: {{ {",".join([v.to_gql_str() for v in val])} }}'
                    str_lst.append(s)
                else:
                    s = f"{field_name}: {jsonable_encoder(val)}"
                    str_lst.append(s)
            else:
                if isinstance(val, DGraphModel):
                    val = val.to_gql_str()
                    s = f"{field_name}: {{ {val} }}"
                    str_lst.append(s)
                elif isinstance(val, Enum):
                    s = f"{field_name}: {val.value}"
                    str_lst.append(s)
                elif type(val) is str:
                    s = f'{field_name}: "{val}"'
                    str_lst.append(s)
                else:
                    s = f"{field_name}: {val}"
                    str_lst.append(s)
        final_s = ",".join(str_lst)
        final_s = final_s.replace("'", '"')
        return final_s
