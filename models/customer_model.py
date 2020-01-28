
from cerberus import Validator


CREATE_SCHEMA = {
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
}


UPDATE_SCHEMA = {
    'currency_type_id': {'type': 'integer', 'required': True},
}


class CustomerModel:
    @classmethod
    async def create(cls, data):
        v = Validator(CREATE_SCHEMA)

        if v.validate(data) and data.get('password') == data.get('repeat_password'):
            sql = "insert into currency.customer(email, password) values(%(email)s, %(password)s) returning id"
            cursor = await cls.db.execute(sql)

            data['id'] = cursor.fetchone().get('id')

            return data, None

        else:
            return data, v.errors

    @classmethod
    async def get(cls, customer_id):
        sql = "select * from currency.customer where id = %s"
        cursor = await cls.db.execute(sql, (customer_id,))

        return cursor.fetchone()

    @classmethod
    async def check(cls, data):
        sql = "select * from currency.customer where email = %(email)s and password = %(password)s"
        cursor = await cls.db.execute(sql, data)

        return cursor.fetchone()
