"""SQL syntax"""

from __future__ import absolute_import
from .base import SQL
from .name import C, F
from .expression import CASE, AND, XOR, OR, NOT, LIKE, NOT_LIKE, ILIKE, NOT_ILIKE, RLIKE, NOT_RLIKE, IN, NOT_IN, IS_NULL, IS_NOT_NULL
from .sort import ASC, DESC
from .table import VALUES
from .alias import A

from .expression import V
from .table import T, ONLY

L = SQL.wrap
