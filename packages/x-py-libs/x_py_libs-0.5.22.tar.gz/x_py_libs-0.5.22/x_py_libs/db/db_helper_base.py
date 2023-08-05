# -*- coding=utf-8 -*-

from enum import Enum


class DBOperatorEnum(Enum):
    EQUAL_TO = '='
    NOT_EQUAL_TO = '!='
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT LIKE'
    IN = 'IN'
    GREATER_THAN = '>'
    LESS_THAN = '>'
    GREATER_THAN_OR_EQUAL_TO = '>='
    LESS_THAN_OR_EQUAL_TO = '>='
    POSIX = '~'


class DBAndOrEnum(Enum):
    AND = 'AND'
    OR = 'OR'


class DBConditionParamsTypeEnum(Enum):
    P = 0
    C = 1


__db_expression = {
    'field': {
        'concat': {
            'comma_lr': """CONCAT(',', %s, ',')"""
        },
        'cast': {
            'varchar': """CAST(%s AS VARCHAR)"""
        }
    },
    'params': {
        'like': {
            'lr': '%%%s%%',
            'comma_lr': '%%,%s,%%'
        },
        'in': ' (%s) '
    }
}

DBExpression = __db_expression


class DBConditionModel(object):

    field = ''
    field_expression = ''
    operator = DBOperatorEnum.EQUAL_TO
    params = None
    params_expression = ''
    params_type = DBConditionParamsTypeEnum.P
    params_brackets = False
    and_or = DBAndOrEnum.AND
    use_and_or = True
    inner_and_or = DBAndOrEnum.AND

    def __init__(self):
        pass

    def __init__(self, field='', field_expression='', operator=DBOperatorEnum.EQUAL_TO, params=None, params_expression='', params_type=DBConditionParamsTypeEnum.P, params_brackets=False, and_or=DBAndOrEnum.AND, use_and_or=True, inner_and_or=DBAndOrEnum.AND, use_inner_and_or=False):

        self.field = field
        self.field_expression = field_expression
        self.operator = operator
        # print('operator:', operator, type(operator), operator.value, type(operator.value))
        # print('self.operator:', self.operator, type(self.operator), self.operator.value, type(self.operator.value))
        self.params = params
        self.params_expression = params_expression
        self.params_type = params_type
        self.params_brackets = params_brackets
        self.and_or = and_or
        self.use_and_or = use_and_or
        self.use_inner_and_or = use_inner_and_or
        self.inner_and_or = inner_and_or


class DBConditionHelper(object):

    @staticmethod
    def get_in_condition(field, params, **kwargs):
        return DBConditionModel(
            field=field,
            params=params,
            params_brackets=True,
            operator=DBOperatorEnum.IN,
            **kwargs
        )

    @staticmethod
    def get_equal_condition(field, params):
        return DBConditionModel(
            field=field,
            params=params,
        )

    @staticmethod
    def get_like_lr_condition(field, params, has_comma=True, **kwargs):
        field_expression = ''
        params_expression = DBExpression['params']['like']['lr']
        if has_comma:
            field_expression = DBExpression['field']['concat']['comma_lr']
            params_expression = DBExpression['params']['like']['comma_lr']

        return DBConditionModel(
            field=field,
            field_expression=field_expression,
            operator=DBOperatorEnum.LIKE,
            params=params,
            params_expression=params_expression,
            **kwargs
        )

    @staticmethod
    def get_posix_condition(field, params, has_field_cast_varchar_exp=True, **kwargs):
        field_expression = ''
        if has_field_cast_varchar_exp:
            field_expression = DBExpression['field']['cast']['varchar']
        return DBConditionModel(
            field=field,
            field_expression=field_expression,
            operator=DBOperatorEnum.POSIX,
            params=params,
            **kwargs
        )



class BaseDBHelper(object):

    connect_string = ''
    cur = None
    params = None

    def __init__(self, connect_string, **params):
        self.connect_string = connect_string
        self.params = params

    def connect(self):
        pass

    def analyze_condition(self, condition):
        __params = []
        __condition = ''
        __conditions = []

        operator = condition.operator.value
        params_type = condition.params_type

        use_and_or = condition.use_and_or
        and_or = condition.and_or.value
        if not use_and_or:
            and_or = ''

        use_inner_and_or = condition.use_inner_and_or
        inner_and_or = condition.inner_and_or.value

        # use_and_or = condition.use_and_or
        # and_or = condition.and_or.value
        # if not use_and_or:
        #     and_or = ''

        field = condition.field
        field_expression = condition.field_expression
        if field_expression != '':
            field = field_expression % field

        __c = ' ' + field + ' ' + operator + ' '
        # __c = (inner_and_or if use_inner_and_or else and_or) + ' ' + field + ' ' + operator + ' '
        # print('o:', o, type(o))
        # print('and_or:', and_or, type(and_or))
        # print('f:', f, type(f))
        # print('fe:', fe, type(fe))
        # print('__c:', __c)

        params = condition.params
        params_expression = condition.params_expression
        new_params = []

        if type(params) is not list:
            params = [params]

        # if pe != '':
            # p = pe % p
        new_params = [param if params_expression == '' else (params_expression % param) for param in params]

        # print('pe:', pe)
        # print('new_params:', new_params)

        for param in new_params:
            nc = __c
            if params_type == DBConditionParamsTypeEnum.P:
  
                if operator == 'IN':
                    param = tuple(param.split(','))
                    
                nc += ' %s ' # if not condition.params_brackets else ' (%s) '
                __params.append(param)
            else:
                nc += param

            # __condition += nc + ' '
            __conditions.append(nc)

        __condition = (inner_and_or if use_inner_and_or else and_or).join(__conditions)

        if use_inner_and_or:
            __condition = ' (' + __condition + ') '

        __condition = and_or + __condition

        # print('__params:', __params)
        # print('__condition:', __condition)

        return __params, __condition

    def get_simple_list(self, table_name, fields, conditions=None, raw_conditions='', order_field='id', order_type='DESC', join_statements=None):
        return self.get_list(table_name, fields, conditions=conditions, raw_conditions=raw_conditions, order_field=order_field, order_type=order_type, pagination=False, join_statements=join_statements)

    def get_list(self, table_name, fields, conditions=None, raw_conditions='', order_field='id', order_type='DESC', page_index=0, page_size=10, pagination=True, join_statements=None, count_with_join=False):
        params = []
        condition = ''
        rst = None
        cnt = 0

        if conditions is not None:

            for c in conditions:
                __cc = ''
                template = ''
                t = type(c)

                if t is not list:
                    c = [c]
                    template = '%s'
                else:
                    template = ' AND (%s) '

                for c2 in c:
                    __params, __condition = self.analyze_condition(c2)
                    params.extend(__params)
                    __cc += __condition
                # print('__cc:', __cc)

                condition += template % __cc
        
        if raw_conditions != '':
            condition += raw_conditions

        rst, cnt = self.get_list_base(table_name, fields, condition, params, order_field=order_field, order_type=order_type, page_index=page_index, page_size=page_size, pagination=pagination, join_statements=join_statements, count_with_join=count_with_join)
        return rst, cnt

    def get_list_base(self, table_name, fields, condition='', params=None, order_field='id', order_type='DESC', page_index=0, page_size=10, pagination=True, pagination_with_limit=True, join_statements=None, count_with_join=False):
        cnt = 0

        if pagination:
            # cnt = self.get_count(table_name, condition, params, join_statements=join_statements)
            cnt_sql = """SELECT COUNT(1) AS cnt FROM """ + table_name + (join_statements if count_with_join and join_statements is not None else '') + ' WHERE 1 = 1 ' + condition + """;"""
            rst = self.fetch_one(cnt_sql, params)
            cnt = rst['cnt']
            # return cnt

        page_size = int(page_size)
        page_index = int(page_index)

        order_by_sql = ''

        if order_field is not None and order_type is not None:
            order_field = [order_field] if type(order_field) is str else order_field
            order_type = [order_type] if type(order_type) is str else order_type

            if len(order_type) != len(order_field):
                order_type = list(map(lambda x: order_type[0], range(len(order_field))))

            sort_list = list(map(lambda f, t: """ %s %s """ % (f, t), order_field, order_type))

            order_by_sql = """ ORDER BY """ + ','.join(sort_list)
        
        sql = ''
        if pagination_with_limit:
            sql = """SELECT """ + fields + """ FROM """ + table_name
            sql += '' if join_statements is None else join_statements
            sql += """ WHERE 1 = 1 """
            sql += condition
            sql += order_by_sql

            if pagination:
                if page_size > 0:
                    sql += """ LIMIT %s OFFSET %s """
                    params.append(page_size)
                    params.append(page_size*page_index)

            sql += """;"""

        rst = self.fetch_all(sql, params)
        return rst, cnt

    # def get_count(self, table_name, condition, params, join_statements=None):
    #     cnt_sql = """SELECT COUNT(1) AS cnt FROM """ + table_name + ('' if join_statements is None else join_statements) + ' WHERE 1 = 1 ' + condition + """;"""
    #     rst = self.fetch_one(cnt_sql, params)
    #     cnt = rst['cnt']
    #     return cnt
    
    def fetch_returning_id(self, sql, *params, **kw):
        pass

    def fetch_rowcount(self, sql, *params, **kw):
        def callback(cur):
            # print('cur:',cur)
            return cur.rowcount

        return self.execute_sql(sql, callback, *params, **kw)

    def fetch_many_rowcount(self, sql, *params, **kw):
        def callback(cur):
            return cur.rowcount

        return self.execute_many(sql, callback, *params, **kw)

    def fetch_one(self, sql, *params, **kw):
        def callback(cur):
            return cur.fetchone()

        return self.execute_sql(sql, callback, *params, **kw)

    def fetch_all(self, sql, *params, **kw):
        def callback(cur):
            return cur.fetchall()

        return self.execute_sql(sql, callback, *params, **kw)

    def execute_sql(self, sql, callback, *params, **kw):
        pass

    def execute_many(self, sql, callback, *params, **kw):
        pass

    def callproc(self, proc_name, *params):
        pass
