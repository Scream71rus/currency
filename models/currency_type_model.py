
from models.base_model import BaseModel


class CurrencyTypeModel(BaseModel):

    @classmethod
    async def get_list(cls):
        sql = "select * from currency.currency_type"
        cursor = await cls.db.execute(sql)

        return cursor.fetchall()

    @classmethod
    async def update_rate(cls, data):
        sql = "update from currency.currency_type set rate_in_rub = %(rate_in_rub)s where id = %(id)s"
        await cls.db.execute(sql, data)
