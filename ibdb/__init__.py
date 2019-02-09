from . import tables


def save_fills(ib, engine, tablename="fills"):
    fills = tables.Fills(engine, tablename)
    if not engine.has_table(tablename):
        fills.create_table()
    fills.insert(ib.fills())


def save_ticks(ib, engine, tablename="ticks"):
    ticks = tables.Ticks(engine, tablename)
    if not engine.has_table(tablename):
        ticks.create_table()
    ticks.insert(ib.fills())