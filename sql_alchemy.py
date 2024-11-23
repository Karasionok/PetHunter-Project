from sqlalchemy import create_engine
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker

from models import User

"""
Для автоматической генерации модели можно использовать утилиту sqlacodegen.
sqlacodegen sqlite:///DB/DataBase.sqlite > models.py
"""

engine = create_engine('sqlite:///DB/DataBase.sqlite')

Session = sessionmaker(bind=engine)
session = Session()

results = session.query(User).all()
for result in results:
    print(result.full_name, result.phone)