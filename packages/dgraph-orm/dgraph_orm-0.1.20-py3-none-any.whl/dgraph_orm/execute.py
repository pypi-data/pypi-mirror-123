import typing as T
import os
import time
import httpx
from httpx import Response
from . import GQLException

URL = os.environ["DGRAPH_URL"]


def check_for_errors(j: dict) -> None:
    if errors := j.get("errors"):
        error_strs: T.List[str] = []
        for error in errors:
            error_strs.append(error["message"])
        raise GQLException(error_strs)


def finish(
    *, response: Response, query_str: str, should_print: bool, start_time: float
) -> dict:
    j = response.json()
    print(
        f"took: {(time.time() - start_time) * 1000}, "
        f'took internal: {int(j["extensions"]["tracing"]["duration"]) / (10 ** 6)}'
    )
    if should_print:
        print(f"{query_str=}, {j=}")
    check_for_errors(j)
    if "data" not in j:
        raise GQLException(f"data not in j!, {j=}, {query_str=}")
    return j


def gql_sync(
    query_str: str, variables: dict = None, should_print: bool = False
) -> dict:
    start = time.time()
    response = httpx.post(URL, json={"query": query_str, "variables": variables or {}})
    return finish(
        response=response,
        query_str=query_str,
        should_print=should_print,
        start_time=start,
    )


async def gql(
    query_str: str, variables: dict = None, should_print: bool = False
) -> dict:
    start = time.time()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            URL, json={"query": query_str, "variables": variables or {}}
        )
    return finish(
        response=response,
        query_str=query_str,
        should_print=should_print,
        start_time=start,
    )
