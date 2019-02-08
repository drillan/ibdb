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
            Column("execId", String, unique=True),
            Column("time", DateTime),
            Column("acctNumber", String),
            Column("exchange", String),
            Column("side", String),
            Column("shares", Float),
            Column("price", Float),
            Column("permId", Integer),
            Column("clientId", Integer),
            Column("orderId", Integer),
            Column("liquidation", Integer),
            Column("cumQty", Float),
            Column("avgPrice", Float),
            Column("orderRef", String),
            Column("evRule", String),
            Column("evMultiplier", Float),
            Column("modelCode", String),
            Column("lastLiquidity", Integer),
            Column("secType", String),
            Column("conId", Integer),
            Column("symbol", String),
            Column("lastTradeDateOrContractMonth", String),
            Column("strike", Float),
            Column("right", String),
            Column("multiplier", String),
            Column("primaryExchange", String),
            Column("currency", String),
            Column("localSymbol", String),
            Column("tradingClass", String),
            Column("includeExpired", Boolean),
            Column("secIdType", String),
            Column("secId", String),
            Column("comboLegsDescrip", String),
            Column("comboLegs", String),
            Column("deltaNeutralContract", String),
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
