from rest_framework.pagination import CursorPagination, LimitOffsetPagination


class SmallLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 10


class IdCursorPagination(CursorPagination):
    ordering = "-id"
