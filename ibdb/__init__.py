from . import tables


def save_fills(ib, engine, tablename="fills"):
    fills = tables.Fills(engine, tablename)
    if not engine.has_table(tablename):
        fills.create_table()
    fills.insert(ib.fills())