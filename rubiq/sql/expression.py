"""SQL expressions"""

from __future__ import absolute_import
from .base import SQL, SQLIterator
# from ..utils import Const


class Expression(SQL):
    """Wrapper for an expression"""

    def __lt__(self, other): return BinaryOperator(self, '<', other)
    def __le__(self, other): return BinaryOperator(self, '<=', other)
    def __eq__(self, other): return BinaryOperator(self, '=', other)
    def __ne__(self, other): return BinaryOperator(self, '<>', other)
    def __gt__(self, other): return BinaryOperator(self, '>', other)
    def __ge__(self, other): return BinaryOperator(self, '>=', other)

    def __add__(self, other): return BinaryOperator(self, '+', other)
    def __sub__(self, other): return BinaryOperator(self, '-', other)
    def __mul__(self, other): return BinaryOperator(self, '*', other)
    def __div__(self, other): return BinaryOperator(self, '/', other)
    def __truediv__(self, other): return BinaryOperator(self, '/', other)
    def __floordiv__(self, other): return BinaryOperator(self, '/', other)
    def __mod__(self, other): return FunctionCall('mod', self, other)
    def __pow__(self, other): return FunctionCall('power', self, other)
    def __lshift__(self, other): return BinaryOperator(self, '<<', other)
    def __rshift__(self, other): return BinaryOperator(self, '>>', other)
    def __and__(self, other): return BinaryOperator(self, '&', other)
    def __xor__(self, other): return BinaryOperator(self, '^', other)
    def __or__(self, other): return BinaryOperator(self, '|', other)

    def __radd__(self, other): return BinaryOperator(other, '+', self)
    def __rsub__(self, other): return BinaryOperator(other, '-', self)
    def __rmul__(self, other): return BinaryOperator(other, '*', self)
    def __rdiv__(self, other): return BinaryOperator(other, '/', self)
    def __rtruediv__(self, other): return BinaryOperator(other, '/', self)
    def __rfloordiv__(self, other): return BinaryOperator(other, '/', self)
    def __rmod__(self, other): return FunctionCall('mod', other, self)
    def __rpow__(self, other): return FunctionCall('power', other, self)
    def __rlshift__(self, other): return BinaryOperator(other, '<<', self)
    def __rrshift__(self, other): return BinaryOperator(other, '>>', self)
    def __rand__(self, other): return BinaryOperator(other, '&', self)
    def __rxor__(self, other): return BinaryOperator(other, '^', self)
    def __ror__(self, other): return BinaryOperator(other, '|', self)

    def __neg__(self): return UnaryOperator('-', self)
    def __pos__(self): return UnaryOperator('+', self)
    def __abs__(self): return FunctionCall('abs', self)
    def __invert__(self): return UnaryOperator('~', self)


# boolean operators
def AND(*exprs): return ChainOperator(exprs, 'AND')
def XOR(*exprs): return ChainOperator(exprs, 'XOR')
def OR(*exprs): return ChainOperator(exprs, 'OR')
def NOT(expr): return UnaryOperator('NOT', expr)


# common SQL operators
def LIKE(left, right): return BinaryOperator(left, 'LIKE', right)
def NOT_LIKE(left, right): return BinaryOperator(left, 'NOT LIKE', right)
def ILIKE(left, right): return BinaryOperator(left, 'ILIKE', right)
def NOT_ILIKE(left, right): return BinaryOperator(left, 'NOT ILIKE', right)
def RLIKE(left, right): return BinaryOperator(left, 'RLIKE', right)
def NOT_RLIKE(left, right): return BinaryOperator(left, 'NOT RLIKE', right)
def IN(left, right): return InOperator(left, right)
def NOT_IN(left, right): return InOperator(left, right, invert=True)
def IS_NULL(expr): return UnaryPostfixOperator(expr, 'IS NULL')
def IS_NOT_NULL(expr): return UnaryPostfixOperator(expr, 'IS NOT NULL')


class Value(Expression):
    """Plain value"""

    def __init__(self, value):
        self.value = value

    def _as_sql(self, connection, context):
        """Return SQL for this instance"""
        return '%s', ( self.value, )

    def __repr__(self):
        return '<Value {value!r}>'.format(value=self.value)


class Variable(Expression):
    """Variable placeholder"""

    def __init__(self, name):
        self.name = name
        assert isinstance(self.name, str), 'Variable name must be a string'

    def _as_sql(self, connection, context):
        return SQL.wrap(context[self.name])._as_sql(connection, context)

    def __repr__(self):
        return '<Variable {name!r}>'.format(name=self.name)


class Identifier(Expression):
    """
    Raw name — can be a column reference or a function call
    """

    def __init__(self, name):
        object.__setattr__(self, '_name', name)
        assert isinstance(self._name, str), 'Identifier name must be a string'

    def _as_sql(self, connection, context):
        """
        Render name as identifier
        """
        return connection.quote_identifier(self._name), ()

    def __repr__(self):
        return '<Identifier {name!r}>'.format(name=self._name)

    def __getattr__(self, name):
        return Identifier('{name}.{subname}'.format(
            name=self._name,
            subname=name,
        ))

    def __setattr__(self, name, value):
        raise AttributeError('Names are not assignable')

    def __call__(self, *args, **kwargs):
        """
        Wrap name in a function call wrapper
        """
        return FunctionCall(self._name, *args, **kwargs)



class FunctionCall(Expression):
    """Function call wrapper"""

    class DUP:
        ALL = 'ALL '
        DISTINCT = 'DISTINCT '


    def __init__(self, name, *params):
        self.name = name
        self.params = params
        self.dup = None
        assert isinstance(self.name, str), 'Function name must be a string'

    def _as_sql(self, connection, context):
        sql, args = SQLIterator(self.params)._as_sql(connection, context)
        sql = '{name}({dup}{params})'.format(
            name=connection.quote_function_name(self.name),
            dup=self.dup or '',
            params=sql,
        )
        return sql, args

    @property
    def ALL(self):
        self.dup = self.DUP.ALL
        return self

    @property
    def DISTINCT(self):
        self.dup = self.DUP.DISTINCT
        return self

    def OVER(self, *args, **kwargs):
        return WindowFunctionCall(self, *args, **kwargs)


class WindowFunctionCall(FunctionCall):
    """Window function call wrapper"""

    def __init__(self, call, *args, **kwargs):
        self.call = call
        self.window = Window(*args, **kwargs) if (len(args) != 1) or kwargs else SQL.wrap(args[0], id=True)

    def _as_sql(self, connection, context):
        call_sql, call_args = self.call._as_sql(connection, context)
        window_sql, window_args = self.window._as_sql(connection, context)
        sql = '{call} OVER {window}'.format(
            call=call_sql,
            window=window_sql,
        )
        return sql, call_args + window_args


class ChainOperator(Expression):
    """
    Chain of similar operations (e.g. `a OP b OP c OP d ...`)
    """

    def __init__(self, expressions, op):
        op = ' {op} '.format(op=op)
        self.sqliter = SQLIterator(expressions, sep=op)

    def _as_sql(self, connection, context):
        sql, args = self.sqliter._as_sql(connection, context)
        sql = '({sql})'.format(sql=sql)
        return sql, args


class BinaryOperator(Expression):
    """
    Wrapper for a generic binary operator
    """

    def __init__(self, left, op, right, invert=False):
        if invert:
            op = 'NOT ' + op
        self.left = left
        self.op = op
        self.right = right

    def _as_sql(self, connection, context):
        override = connection.operator_to_sql(self.op, self.left, self.right, context=context)
        if override and (override != NotImplemented):
            # database driver overrides this operator
            return override
        left_sql, left_args = self.left_to_sql(connection, context)
        right_sql, right_args = self.right_to_sql(connection, context)
        try:
            sql = '({left} {op} {right})'.format(
                left=left_sql,
                op=self.op,
                right=right_sql,
            )
        except Exception:
            raise Exception(map(type, (left_sql, self.op, right_sql)))
        return sql, left_args + right_args

    def left_to_sql(self, connection, context):
        return SQL.wrap(self.left)._as_sql(connection, context)

    def right_to_sql(self, connection, context):
        return SQL.wrap(self.right)._as_sql(connection, context)


class UnaryOperator(Expression):
    """Wrapper for a generic unary operation """

    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def _as_sql(self, connection, context):
        override = connection.operator_to_sql(self.op, self.operand, context=context)
        if override and (override != NotImplemented):
            # database driver overrides this operator
            return override
        sql, args = SQL.wrap(self.operand)._as_sql(connection, context)
        sql = '({op} {operand})'.format(
            op=self.op,
            operand=sql,
        )
        return sql, args


class UnaryPostfixOperator(UnaryOperator):
    """Wrapper for a generic unary postfix operation (e.g. `a IS NULL`)"""

    def __init__(self, operand, op, invert=False):
        if invert:
            op = 'NOT ' + op
        super(UnaryPostfixOperator, self).__init__(op, operand)

    def _as_sql(self, connection, context):
        override = connection.operator_to_sql(self.op, self.operand, context=context)
        if override and (override != NotImplemented):
            # database driver overrides this operator
            return override
        sql, args = SQL.wrap(self.operand)._as_sql(connection, context)
        sql = '({operand} {op})'.format(
            op=self.op,
            operand=sql,
        )
        return sql, args


class InOperator(BinaryOperator):
    """
    Wrapper for IN operator
    """

    def __init__(self, left, right, invert=False):
        super(InOperator, self).__init__(left, 'IN', right, invert=invert)

    def right_to_sql(self, connection, context):
        sql, args = SQLIterator(self.right)._as_sql(connection, context)
        sql = '({items})'.format(items=sql)
        return sql, args


class CASE(Expression):
    """
    CASE operator
    """

    def __init__(self):
        self.cases = []
        self.else_ = None

    def WHEN(self, condition, value):
        self.cases.append((condition, value))
        return self

    def ELSE(self, value):
        self.else_ = value
        return self

    def case_to_sql(self, cond, value, connection, context):
        """
        Render a single case to SQL
        """
        assert self.cases, 'CASE operator must have at least one WHEN clause'
        cond_sql, cond_args = SQL.wrap(cond)._as_sql(connection, context)
        value_sql, value_args = SQL.wrap(value)._as_sql(connection, context)
        sql = 'WHEN {condition} THEN {value}'.format(
            condition=cond_sql,
            value=value_sql,
        )
        return sql, cond_args + value_args

    def _as_sql(self, connection, context):
        cases_sql, cases_args = SQL.merge(self.case_to_sql(cond, value, connection, context) for cond, value in self.cases)
        if self.else_ is not None:
            else_sql, else_args = SQL.wrap(self.else_)._as_sql(connection, context)
            else_sql = ' ELSE {value}'.format(value=else_sql)
        else:
            else_sql = ''
            else_args = ()
        sql = 'CASE {cases}{else_} END'.format(
            cases=cases_sql,
            else_=else_sql,
        )
        return sql, cases_args + else_args


from .window import Window
