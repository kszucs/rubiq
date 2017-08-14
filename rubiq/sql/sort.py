"""SQL sorting"""

from __future__ import absolute_import
from .base import SQL
from enum import Enum

class Sorting(SQL):
    """Sorting order on an expression

    Sorting orders are no longer expressions, as they are not allowed in
    operations, only in ORDER BY clauses.
    """

    class DIR(Enum):
        """Sort direction"""
        ASC = ' ASC'
        DESC = ' DESC'

    class NULLS(Enum):
        """NULL ordering"""
        FIRST = ' NULLS FIRST'
        LAST = ' NULLS LAST'

    def __init__(self, expr, direction=None, nulls=None):
        self.expr = expr
        self.direction = direction
        self.nulls = nulls
        assert self.direction is None or self.direction in self.DIR, 'Invalid sorting direction: {dir}'.format(dir=self.direction)
        assert self.nulls is None or self.nulls in self.NULLS, 'Invalid sorting of nulls: {nulls}'.format(nulls=self.nulls)

    def _as_sql(self, connection, context):
        sql, args = SQL.wrap(self.expr)._as_sql(connection, context)
        sql = u'{expr}{dir}{nulls}'.format(
            expr=sql,
            dir='' if self.direction is None else self.direction.value,
            nulls='' if self.nulls is None else self.nulls.value,
        )
        return sql, args

    @property
    def NULLS_FIRST(self):
        self.nulls = self.NULLS.FIRST
        return self

    @property
    def NULLS_LAST(self):
        self.nulls = self.NULLS.LAST
        return self

def ASC(expr): return Sorting(expr, direction=Sorting.DIR.ASC)
def DESC(expr): return Sorting(expr, direction=Sorting.DIR.DESC)
