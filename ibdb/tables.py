import hashlib

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.sql import select

from . import utils


class BaseTable:
    def __init__(self, engine, tablename):
        self.metadata = MetaData(bind=engine)
        self.tablename = tablename

    def create_table(self):
        self.metadata.create_all()

    def insert_table(self, data, key):
        target = select([self.table.c.get(key)]).execute().fetchall()
        source = utils.make_difference_list_from_key(target, data, key)
        if source:
            self.table.insert().values(source).execute()


class Fills(BaseTable):
    def __init__(self, engine, tablename):
        super().__init__(engine, tablename)
        self.table = Table(
            self.tablename,
            self.metadata,
            Column("execId", String(30), unique=True),
            Column("time", DateTime),
            Column("acctNumber", String(30)),
            Column("exchange", String(30)),
            Column("side", String(30)),
            Column("shares", Float),
            Column("price", Float),
            Column("permId", Integer),
            Column("clientId", Integer),
            Column("orderId", Integer),
            Column("liquidation", Integer),
            Column("cumQty", Float),
            Column("avgPrice", Float),
            Column("orderRef", String(30)),
            Column("evRule", String(30)),
            Column("evMultiplier", Float),
            Column("modelCode", String(30)),
            Column("lastLiquidity", Integer),
            Column("secType", String(30)),
            Column("conId", Integer),
            Column("symbol", String(30)),
            Column("lastTradeDateOrContractMonth", String(30)),
            Column("strike", Float),
            Column("right", String(30)),
            Column("multiplier", String(30)),
            Column("primaryExchange", String(30)),
            Column("currency", String(30)),
            Column("localSymbol", String(30)),
            Column("tradingClass", String(30)),
            Column("includeExpired", Boolean),
            Column("secIdType", String(30)),
            Column("secId", String(30)),
            Column("comboLegsDescrip", String(30)),
            Column("comboLegs", String(30)),
            Column("deltaNeutralContract", String(30)),
            Column("commission", Float),
            Column("realizedPNL", Float),
            Column("yield_", Float),
            Column("yieldRedemptionDate", Float),
        )

    def insert(self, fills):
        def merge_dict(Fill):
            execution = Fill.execution.dict()
            contract = Fill.contract.dict()
            commission_report = Fill.commissionReport.dict()
            for x in set(execution.keys()) & set(contract.keys()):
                contract.pop(x)

            for x in set(execution.keys()) & set(commission_report.keys()):
                commission_report.pop(x)

            for x in set(contract.keys()) & set(commission_report.keys()):
                commission_report.pop(x)

            execution.update(contract)
            execution.update(commission_report)
            return execution

        self.data = [merge_dict(x) for x in fills]
        self.insert_table(self.data, "execId")


class Ticks(BaseTable):
    def __init__(self, engine, tablename):
        super().__init__(engine, tablename)
        self.table = Table(
            self.tablename,
            self.metadata,
            Column("id", String(64)),
            Column("time", DateTime),
            Column("priceBid", Float),
            Column("priceAsk", Float),
            Column("sizeBid", Float),
            Column("sizeAsk", Float),
        )

    def insert(self, ticks):
        def to_dict(obj):
            attrs = ("time", "priceAsk", "priceBid", "sizeAsk", "sizeBid")
            prices = "".join([str(getattr(obj, attr)) for attr in attrs[1:]])
            id_ = f"{obj.time:%y%m%d%H%M%S}{prices}"
            id_md5 = hashlib.md5(id_.encode("utf8")).hexdigest()
            ret = {attr: getattr(obj, attr) for attr in attrs}
            ret["id"] = id_md5
            return ret

        self.data = [to_dict(t) for t in ticks]
        self.insert_table(self.data, "time")
