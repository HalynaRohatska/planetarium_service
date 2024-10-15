from typing import Callable
import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter
)


def astronomy_show_list_schema() -> Callable:
    def decorator(func: Callable):
        return extend_schema(
            parameters=[
                OpenApiParameter(
                    "show theme",
                    type={"type": "list", "items": {"type": "number"}},
                    description="Filter by show theme id (ex. ?show_theme=2,3)",
                ),
                OpenApiParameter(
                    "title",
                    type=OpenApiTypes.STR,
                    description="Filter by astronomy show title (ex. ?title=sun)"
                ),
            ]
        )(func)
    return decorator


def show_session_list_schema() -> Callable:
    def decorator(func: Callable):
        return extend_schema(
            parameters=[
                OpenApiParameter(
                    "astronomy show",
                    type=OpenApiTypes.INT,
                    description="Filter by astronomy show id (ex. ?astronomy_show=1)",
                ),
                OpenApiParameter(
                    "date",
                    type=OpenApiTypes.DATE,
                    description="Filter by datetime of Show Session (ex. ?date=2024-11-25)"
                )
            ]
        )(func)
    return decorator
