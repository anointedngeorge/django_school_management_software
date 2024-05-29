from ninja.pagination import paginate, PaginationBase
from ninja import Schema
from typing import List, Any, Optional, Union


class InternalPagination(PaginationBase):
    # only `limit` param, defaults to 5 per page
    class Input(Schema):
        limit: int

    class Output(Schema):
        items: List[Any]  # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        limit = pagination.limit
        limit = limit if limit > 1 else 1
        limit = limit if limit <= queryset.count() else queryset.count()
        return {
            "items": queryset[0:limit],
            "total": queryset.count(),
            "per_page": limit,
        }


class InternalPaginationOffset(PaginationBase):
    # only `limit` param, defaults to 5 per page
    class Input(Schema):
        start: int
        end: int

    class Output(Schema):
        items: List[Any]  # `items` is a default attribute
        total: int
        per_page: int
        start: int = 1
        end: int = 2

    def paginate_queryset(self, queryset, pagination: Input, **params):
        try:
            queryset_checker = True
            start = pagination.start - 1
            start = start if start > 0 else 0
            end = pagination.end - 1 if pagination.end > 1 else pagination.end
            total_count = len(queryset)
            end = end + 1 if end == start else end
            end = end if end <= total_count else total_count

            if isinstance(queryset,tuple):
                if len(queryset[1]) > 0:
                    queryset_checker  = True
                else:
                    queryset_checker = False

            elif isinstance(queryset, list):

                if len(queryset) > 0:
                    queryset_checker  = True
                else:
                    queryset_checker = False
        
            return {
                "items": queryset[start:end] if queryset_checker else [],
                "total": total_count,
                "per_page": end - start,
                "start": pagination.start if pagination.start > 0 else 1,
                "end": pagination.end,
            }
        except Exception as e:
            return str(e)