from sqlalchemy import create_engine

from parser.utils.database.models import metadata

engine = create_engine('postgresql://oleg:oleg2000@localhost:5432/parser_avito')
metadata.create_all(engine)
