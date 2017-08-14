import pytest
from rubiq.query import *


def test_empty_column():
    assert SELECT() == ('SELECT *', ())


def test_wildcard_column():
    assert SELECT(C) == ('SELECT *', ())


def test_table_wildcard():
    assert SELECT(T.table()) == ('SELECT table.*', ())


def test_literal_columns():
    sql = 'SELECT %s, %s, %s, %s, %s'
    args = ('foo', 123, True, False, None)
    assert SELECT('foo', 123, True, False, None) == (sql, args)


def test_literal_alias():
    sql = 'SELECT %s AS literal_alias'
    args = ('literal',)
    assert SELECT(A.literal_alias('literal')) == (sql, args)


def test_column():
    sql = 'SELECT foo, bar.baz, table.xyzzy'
    assert SELECT(C.foo, C.bar.baz, T.table().xyzzy) == (sql, ())


def test_column_alias():
    assert SELECT(A.foo_alias(C.foo)) == ('SELECT foo AS foo_alias', ())


def test_expression():
    sql = 'SELECT ((sum(qty) * avg(price)) * %s)'
    args = (1.2,)
    assert SELECT(F.sum(C.qty) * F.avg(C.price) * 1.2) == (sql, args)


def test_expression_alias():
    sql = 'SELECT ((sum(qty) * avg(price)) * %s) AS average'
    args = (1.2,)
    assert SELECT(A.average(F.sum(C.qty) * F.avg(C.price) * 1.2)) == (sql, args)


def test_subquery():
    sql = 'SELECT (SELECT avg(price)) AS average'
    assert SELECT(A.average(SELECT(F.avg(C.price)))) == (sql, ())


def test_simple_function():
    assert SELECT(F.func_name()) == ('SELECT func_name()', ())


def test_alias_function():
    sql = 'SELECT func_name() AS func_alias'
    assert SELECT(A.func_alias(F.func_name())) == (sql, ())


def test_literal_function():
    assert SELECT(F.abs(-1)) == ('SELECT abs(%s)', (-1,))


def test_column_function():
    assert SELECT(F.count(C.id)) == ('SELECT count(id)', ())


def test_wildcard_function():
    assert SELECT(F.count(C)) == ('SELECT count(*)', ())


def test_distinct_function():
    assert SELECT(F.count(C.id).DISTINCT) == ('SELECT count(DISTINCT id)', ())


def test_all_function():
    assert SELECT(F.count(C.id).ALL) == ('SELECT count(ALL id)', ())


def test_window_function():
    sql = 'SELECT count(id) OVER window'
    assert SELECT(F.count(C.id).OVER(C.window)) == (sql, ())


def test_lt():
    assert SELECT(C.foo < C.bar) == ('SELECT (foo < bar)', ())


def test_le():
    assert SELECT(C.foo <= C.bar) == ('SELECT (foo <= bar)', ())


def test_eq():
    assert SELECT(C.foo == C.bar) == ('SELECT (foo = bar)', ())


def test_ne():
    assert SELECT(C.foo != C.bar) == ('SELECT (foo <> bar)', ())


def test_gt():
    assert SELECT(C.foo > C.bar) == ('SELECT (foo > bar)', ())


def test_ge():
    assert SELECT(C.foo >= C.bar) == ('SELECT (foo >= bar)', ())


def test_add():
    assert SELECT(C.foo + C.bar) == ('SELECT (foo + bar)', ())


def test_sub():
    assert SELECT(C.foo - C.bar) == ('SELECT (foo - bar)', ())


def test_mul():
    assert SELECT(C.foo * C.bar) == ('SELECT (foo * bar)', ())


def test_div():
    assert SELECT(C.foo / C.bar) == ('SELECT (foo / bar)', ())


def test_floordiv():
    assert SELECT(C.foo // C.bar) == ('SELECT (foo / bar)', ())


def test_mod():
    assert SELECT(C.foo % C.bar) == ('SELECT mod(foo, bar)', ())


def test_pow():
    assert SELECT(C.foo ** C.bar) == ('SELECT power(foo, bar)', ())


def test_lshift():
    assert SELECT(C.foo << C.bar) == ('SELECT (foo << bar)', ())


def test_rshift():
    assert SELECT(C.foo >> C.bar) == ('SELECT (foo >> bar)', ())


def test_and():
    assert SELECT(C.foo & C.bar) == ('SELECT (foo & bar)', ())


def test_xor():
    assert SELECT(C.foo ^ C.bar) == ('SELECT (foo ^ bar)', ())


def test_or():
    assert SELECT(C.foo | C.bar) == ('SELECT (foo | bar)', ())


def test_neg():
    assert SELECT(-C.foo) == ('SELECT (- foo)', ())


def test_pos():
    assert SELECT(+C.foo) == ('SELECT (+ foo)', ())


def test_abs():
    assert SELECT(abs(C.foo)) == ('SELECT abs(foo)', ())


def test_invert():
    assert SELECT(~C.foo) == ('SELECT (~ foo)', ())


def test_bool_and():
    assert SELECT(AND(C.foo, C.bar)) == ('SELECT (foo AND bar)', ())


def test_bool_xor():
    assert SELECT(XOR(C.foo, C.bar)) == ('SELECT (foo XOR bar)', ())


def test_bool_or():
    assert SELECT(OR(C.foo, C.bar)) == ('SELECT (foo OR bar)', ())


def test_bool_not():
    assert SELECT(NOT(C.foo)) == ('SELECT (NOT foo)', ())


def test_like():
    sql = 'SELECT (foo LIKE %s)'
    args = ('foobar',)
    assert SELECT(LIKE(C.foo, 'foobar')) == (sql, args)


def test_not_like():
    sql = 'SELECT (foo NOT LIKE %s)'
    args = ('foobar',)
    assert SELECT(NOT_LIKE(C.foo, 'foobar')) == (sql, args)


def test_ilike():
    sql = 'SELECT (foo ILIKE %s)'
    args = ('foobar',)
    assert SELECT(ILIKE(C.foo, 'foobar')) == (sql, args)


def test_not_ilike():
    sql = 'SELECT (foo NOT ILIKE %s)'
    args = ('foobar',)
    assert SELECT(NOT_ILIKE(C.foo, 'foobar')) == (sql, args)


def test_rlike():
    sql = 'SELECT (foo RLIKE %s)'
    args = ('foobar',)
    assert SELECT(RLIKE(C.foo, 'foobar')) == (sql, args)


def test_not_rlike():
    sql = 'SELECT (foo NOT RLIKE %s)'
    args = ('foobar',)
    assert SELECT(NOT_RLIKE(C.foo, 'foobar')) == (sql, args)


def test_in():
    sql = 'SELECT (foo IN (%s, %s, %s))'
    args = (1, 2, 3)
    assert SELECT(IN(C.foo, (1, 2, 3))) == (sql, args)

def test_not_in():
    sql = 'SELECT (foo NOT IN (%s, %s, %s))'
    args = (1, 2, 3)
    assert SELECT(NOT_IN(C.foo, (1, 2, 3))) == (sql, args)

def test_is_null():
    assert SELECT(IS_NULL(C.foo)) == ('SELECT (foo IS NULL)', ())


def test_is_not_null():
    assert SELECT(IS_NOT_NULL(C.foo)) == ('SELECT (foo IS NOT NULL)', ())


def test_precedence():
    assert SELECT(C.foo + C.bar * C.baz) == ('SELECT (foo + (bar * baz))', ())


def test_parens():
    assert SELECT((C.foo + C.bar) * C.baz) == ('SELECT ((foo + bar) * baz)', ())


def test_distinct():
    assert SELECT().DISTINCT() == ('SELECT DISTINCT *', ())


def test_distinct_columns():
    sql = 'SELECT DISTINCT ON (foo, bar) *'
    assert SELECT().DISTINCT(C.foo, C.bar) == (sql, ())


def test_all_asterisk():
    assert SELECT().ALL() == ('SELECT ALL *', ())


def test_all_columns():
    assert SELECT().ALL(C.foo, C.bar) == ('SELECT ALL ON (foo, bar) *', ())


def test_single_with():
    sql = 'WITH foo AS (SELECT *) SELECT *'
    assert SELECT().WITH(C.foo, SELECT()) == (sql, ())


def test_multi_with():
    sql = ('WITH foo AS (SELECT * FROM table_foo), '
           'bar AS (SELECT * FROM table_bar) SELECT *')

    select = (SELECT().WITH(C.foo, SELECT().FROM(T.table_foo))
                      .WITH(C.bar, SELECT().FROM(T.table_bar)))

    assert select == (sql, ())


def test_recursive_with():
    select = SELECT().WITH(C.foo(C.bar, C.baz),
                           SELECT(C.bar, C.baz) |
                           SELECT(C.bar, C.baz).FROM(C.foo), RECURSIVE=True)
    sql = ('WITH RECURSIVE foo(bar, baz) AS '
           '(SELECT bar, baz UNION SELECT bar, baz FROM foo) SELECT *')

    assert select == (sql, ())


def test_table_from():
    assert SELECT().FROM(T.table) == ('SELECT * FROM table', ())


def test_table_alias():
    sql = 'SELECT * FROM table AS table_alias'
    assert SELECT().FROM(A.table_alias(T.table)) == (sql, ())


def test_table_alias_columns():
    sql = 'SELECT * FROM table AS table_alias(foo, bar)'
    select = SELECT().FROM(A.table_alias(T.table, columns=(C.foo, C.bar)))
    assert select == (sql, ())


def test_from_subquery():
    sql = 'SELECT * FROM (SELECT sum(qty), avg(price)) AS subquery'
    select = SELECT().FROM(A.subquery(SELECT(F.sum(F.qty), F.avg(C.price))))
    assert select == (sql, ())


def test_from_subquery_columns():
    sql = ('SELECT * FROM (SELECT sum(qty), avg(price)) '
           'AS subquery(qty, average)')
    subselect = SELECT(F.sum(F.qty), F.avg(C.price))
    select = SELECT().FROM(A.subquery(subselect, columns=(C.qty, C.average)))

    assert select == (sql, ())


def test_from_values():
    sql = 'SELECT * FROM (VALUES (%s, %s, %s), (%s, %s, %s)) AS val_alias'
    args = (1, 2, 3, 4, 5, 6)
    select = SELECT().FROM(A.val_alias(VALUES(1, 2, 3)(4, 5, 6)))
    assert select == (sql, args)


def test_from_values_columns():
    sql = ('SELECT * FROM (VALUES (%s, %s, %s), (%s, %s, %s)) '
           'AS val_alias(foo, bar, baz)')
    args = (1, 2, 3, 4, 5, 6)
    values = VALUES(1, 2, 3)(4, 5, 6)
    select = SELECT().FROM(A.val_alias(values, columns=(C.foo, C.bar, C.baz)))
    assert select == (sql, args)


def test_order_empty():
    assert SELECT().ORDER_BY() == ('SELECT *', ())


def test_order_column():
    sql = 'SELECT * ORDER BY foo, bar'
    assert SELECT().ORDER_BY(C.foo, C.bar) == (sql, ())


def test_order_dir():
    sql = 'SELECT * ORDER BY foo ASC, bar DESC'
    assert SELECT().ORDER_BY(ASC(C.foo), DESC(C.bar)) == (sql, ())


def test_order_nulls():
    select = SELECT().ORDER_BY(ASC(C.foo).NULLS_FIRST, DESC(C.bar).NULLS_LAST)
    sql = 'SELECT * ORDER BY foo ASC NULLS FIRST, bar DESC NULLS LAST'
    assert select == (sql, ())


def test_limit():
    assert SELECT().LIMIT(10) == ('SELECT * LIMIT %s', (10,))


def test_limit_offset():
    assert SELECT().LIMIT(10, 20) == ('SELECT * LIMIT %s OFFSET %s', (10, 20))


def test_offset():
    sql = 'SELECT * LIMIT %s OFFSET %s'
    assert SELECT().LIMIT(10).OFFSET(20) == (sql, (10, 20))


def test_cross_join():
    expected = 'SELECT * FROM foo CROSS JOIN bar', ()
    assert SELECT().FROM(T.foo).CROSS_JOIN(T.bar) == expected


def test_left_natural_join():
    expected = 'SELECT * FROM foo NATURAL LEFT OUTER JOIN bar', ()
    assert SELECT().FROM(T.foo).LEFT_JOIN(T.bar, NATURAL=True) == expected


def test_left_join_using_one():
    expected = 'SELECT * FROM foo LEFT OUTER JOIN bar USING (baz)', ()
    assert SELECT().FROM(T.foo).LEFT_JOIN(T.bar, USING=C.baz) == expected


def test_left_join_using_multi():
    expected = 'SELECT * FROM foo LEFT OUTER JOIN bar USING (baz, xyzzy)', ()
    select = SELECT().FROM(T.foo).LEFT_JOIN(T.bar, USING=(C.baz, C.xyzzy))
    assert select == expected


def test_left_join_on():
    expected = 'SELECT * FROM foo LEFT OUTER JOIN bar ON (baz > %s)', (100,)
    assert SELECT().FROM(T.foo).LEFT_JOIN(T.bar, ON=(C.baz > 100)) == expected


def test_right_natural_join():
    expected = 'SELECT * FROM foo NATURAL RIGHT OUTER JOIN bar', ()
    assert SELECT().FROM(T.foo).RIGHT_JOIN(T.bar, NATURAL=True) == expected


def test_right_join_using_one():
    expected = 'SELECT * FROM foo RIGHT OUTER JOIN bar USING (baz)', ()
    assert SELECT().FROM(T.foo).RIGHT_JOIN(T.bar, USING=C.baz) == expected


def test_right_join_using_multi():
    expected = 'SELECT * FROM foo RIGHT OUTER JOIN bar USING (baz, xyzzy)', ()
    select = SELECT().FROM(T.foo).RIGHT_JOIN(T.bar, USING=(C.baz, C.xyzzy))
    assert select == expected


def test_right_join_on():
    expected = 'SELECT * FROM foo RIGHT OUTER JOIN bar ON (baz > %s)', (100,)
    assert SELECT().FROM(T.foo).RIGHT_JOIN(T.bar, ON=(C.baz > 100)) == expected


def test_full_natural_join():
    expected = 'SELECT * FROM foo NATURAL FULL OUTER JOIN bar', ()
    assert SELECT().FROM(T.foo).FULL_JOIN(T.bar, NATURAL=True) == expected


def test_full_join_using_one():
    expected = 'SELECT * FROM foo FULL OUTER JOIN bar USING (baz)', ()
    assert SELECT().FROM(T.foo).FULL_JOIN(T.bar, USING=C.baz) == expected


def test_full_join_using_multi():
    expected = 'SELECT * FROM foo FULL OUTER JOIN bar USING (baz, xyzzy)', ()
    select = SELECT().FROM(T.foo).FULL_JOIN(T.bar, USING=(C.baz, C.xyzzy))
    assert select == expected


def test_full_join_on():
    expected = 'SELECT * FROM foo FULL OUTER JOIN bar ON (baz > %s)', (100,)
    assert SELECT().FROM(T.foo).FULL_JOIN(T.bar, ON=(C.baz > 100)) == expected


def test_inner_natural_join():
    expected = 'SELECT * FROM foo NATURAL INNER JOIN bar', ()
    assert SELECT().FROM(T.foo).INNER_JOIN(T.bar, NATURAL=True) == expected


def test_inner_join_using_one():
    expected = 'SELECT * FROM foo INNER JOIN bar USING (baz)', ()
    assert SELECT().FROM(T.foo).INNER_JOIN(T.bar, USING=C.baz) == expected


def test_inner_join_using_multi():
    expected = 'SELECT * FROM foo INNER JOIN bar USING (baz, xyzzy)', ()
    select = SELECT().FROM(T.foo).INNER_JOIN(T.bar, USING=(C.baz, C.xyzzy))
    assert select == expected


def test_inner_join_on():
    expected = 'SELECT * FROM foo INNER JOIN bar ON (baz > %s)', (100,)
    assert SELECT().FROM(T.foo).INNER_JOIN(T.bar, ON=(C.baz > 100)) == expected


def test_where_no_from():
    with pytest.raises(TypeError):
        SELECT().WHERE(C.foo > 100)


def test_where():
    sql = 'SELECT * FROM table WHERE (foo > %s)'
    assert SELECT().FROM(T.table).WHERE(C.foo > 100) == (sql, (100,))


def test_group_no_from():
    with pytest.raises(TypeError):
        SELECT().GROUP_BY(C.foo)


def test_group():
    sql = 'SELECT * FROM table GROUP BY foo, count(bar)'
    assert SELECT().FROM(T.table).GROUP_BY(C.foo, F.count(C.bar)) == (sql, ())


def test_having_no_from():
    with pytest.raises(TypeError):
        SELECT().HAVING(C.foo > 100)


def test_having():
    sql = 'SELECT * FROM table HAVING (foo > %s)'
    assert SELECT().FROM(T.table).HAVING(C.foo > 100) == (sql, (100,))


# class WindowTest(TestCase):

#     def test_empty():
#         assert SELECT().WINDOW(C.name),
#                     ('SELECT * WINDOW name AS ()', ()))

#     def test_named():
#         assert SELECT().WINDOW(C.name, C.window_ref),
#                     ('SELECT * WINDOW name AS (window_ref)', ()))

#     def test_partition_single():
#         assert SELECT().WINDOW(C.name, PARTITION_BY=C.foo),
#                     ('SELECT * WINDOW name AS (PARTITION BY foo)', ()))

#     def test_partition_multi():
#         assert SELECT().WINDOW(C.name, PARTITION_BY=(C.foo, C.bar)),
#                     ('SELECT * WINDOW name AS (PARTITION BY foo, bar)', ()))

#     def test_order_single():
#         assert SELECT().WINDOW(C.name, ORDER_BY=C.foo),
#                     ('SELECT * WINDOW name AS (ORDER BY foo)', ()))

#     def test_order_dir():
#         assert SELECT().WINDOW(C.name, ORDER_BY=ASC(C.foo)),
#                     ('SELECT * WINDOW name AS (ORDER BY foo ASC)', ()))

#     def test_order_dir_nulls():
#         assert SELECT().WINDOW(C.name, ORDER_BY=ASC(C.foo).NULLS_FIRST),
#                     ('SELECT * WINDOW name AS (ORDER BY foo ASC NULLS FIRST)', ()))

#     def test_order_multi():
#         assert SELECT().WINDOW(C.name, ORDER_BY=(C.foo, ASC(C.bar), DESC(C.baz).NULLS_LAST)),
#                     ('SELECT * WINDOW name AS (ORDER BY foo, bar ASC, baz DESC NULLS LAST)', ()))

#     def test_range_negative():
#         assert SELECT().WINDOW(C.name, RANGE=-1),
#                     ('SELECT * WINDOW name AS (RANGE %s PRECEDING)', (1,)))

#     def test_range_zero():
#         assert SELECT().WINDOW(C.name, RANGE=0),
#                     ('SELECT * WINDOW name AS (RANGE CURRENT ROW)', ()))

#     def test_range_positive():
#         assert SELECT().WINDOW(C.name, RANGE=1),
#                     ('SELECT * WINDOW name AS (RANGE %s FOLLOWING)', (1,)))

#     def test_range_negative_to_end():
#         assert SELECT().WINDOW(C.name, RANGE=(-1, None)),
#                     ('SELECT * WINDOW name AS (RANGE BETWEEN %s PRECEDING AND UNBOUNDED FOLLOWING)', (1,)))

#     def test_range_negative_to_zero():
#         assert SELECT().WINDOW(C.name, RANGE=(-1, 0)),
#                     ('SELECT * WINDOW name AS (RANGE BETWEEN %s PRECEDING AND CURRENT ROW)', (1,)))

#     def test_range_start_to_zero():
#         assert SELECT().WINDOW(C.name, RANGE=(None, 0)),
#                     ('SELECT * WINDOW name AS (RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)', ()))

#     def test_range_zero_to_end():
#         assert SELECT().WINDOW(C.name, RANGE=(0, None)),
#                     ('SELECT * WINDOW name AS (RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)', ()))

#     def test_range_zero_to_positive():
#         assert SELECT().WINDOW(C.name, RANGE=(0, 1)),
#                     ('SELECT * WINDOW name AS (RANGE BETWEEN CURRENT ROW AND %s FOLLOWING)', (1,)))

#     def test_range_start_to_positive():
#         assert SELECT().WINDOW(C.name, RANGE=(None, 1)),
#                     ('SELECT * WINDOW name AS (RANGE BETWEEN UNBOUNDED PRECEDING AND %s FOLLOWING)', (1,)))

#     def test_rows_negative():
#         assert SELECT().WINDOW(C.name, ROWS=-1),
#                     ('SELECT * WINDOW name AS (ROWS %s PRECEDING)', (1,)))

#     def test_rows_zero():
#         assert SELECT().WINDOW(C.name, ROWS=0),
#                     ('SELECT * WINDOW name AS (ROWS CURRENT ROW)', ()))

#     def test_rows_positive():
#         assert SELECT().WINDOW(C.name, ROWS=1),
#                     ('SELECT * WINDOW name AS (ROWS %s FOLLOWING)', (1,)))

#     def test_rows_negative_to_positive():
#         assert SELECT().WINDOW(C.name, ROWS=(-1, 1)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN %s PRECEDING AND %s FOLLOWING)', (1, 1)))

#     def test_rows_negative_to_end():
#         assert SELECT().WINDOW(C.name, ROWS=(-1, None)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN %s PRECEDING AND UNBOUNDED FOLLOWING)', (1,)))

#     def test_rows_negative_to_zero():
#         assert SELECT().WINDOW(C.name, ROWS=(-1, 0)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN %s PRECEDING AND CURRENT ROW)', (1,)))

#     def test_rows_start_to_zero():
#         assert SELECT().WINDOW(C.name, ROWS=(None, 0)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)', ()))

#     def test_rows_zero_to_end():
#         assert SELECT().WINDOW(C.name, ROWS=(0, None)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)', ()))

#     def test_rows_zero_to_positive():
#         assert SELECT().WINDOW(C.name, ROWS=(0, 1)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN CURRENT ROW AND %s FOLLOWING)', (1,)))

#     def test_rows_start_to_positive():
#         assert SELECT().WINDOW(C.name, ROWS=(None, 1)),
#                     ('SELECT * WINDOW name AS (ROWS BETWEEN UNBOUNDED PRECEDING AND %s FOLLOWING)', (1,)))

#     def test_complex():
#         assert SELECT().WINDOW(C.name, C.window_ref, PARTITION_BY=(C.foo, C.bar), ORDER_BY=(ASC(C.foo), DESC(C.bar)), RANGE=(-1, 1)),
#                     ('SELECT * WINDOW name AS (window_ref PARTITION BY foo, bar ORDER BY foo ASC, bar DESC RANGE BETWEEN %s PRECEDING AND %s FOLLOWING)', (1, 1)))
