import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from info import password, login, name_base

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publishers"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Book(Base):
    __tablename__ = "books"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publishers.id"), nullable=False)

    publisher = relationship('Publisher', backref="books")


class Shop(Base):
    __tablename__ = "shops"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    
    stock = relationship('Stock', backref='shops')
    

class Stock(Base):
    __tablename__ = "stocks"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("books.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shops.id"), nullable=False)
    count = sq.Column(sq.Integer)

    books = relationship('Book', backref="stock")


class Sale(Base):
    __tablename__ = "sales"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stocks.id"), nullable=False)
    count = sq.Column(sq.Integer)

    stocks = relationship('Stock', backref="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = 'postgresql://{0}:{1}@localhost:5432/{2}'.format(login, password, name_base)

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

author1 = Publisher(name="Dostoevsky")
author2 = Publisher(name="Gogol")
author3 = Publisher(name="Pushkin")

book1 = Book(title="Captain's daughter", publisher=author3)
book2 = Book(title="Eugene Onegin", publisher=author3)
book3 = Book(title="Crime and punishment", publisher=author1)
book4 = Book(title="Idiot", publisher=author1)
book5 = Book(title="Auditor", publisher=author2)
book6 = Book(title="Dead souls", publisher=author2)

shop1 = Shop(name='Labirint')
shop2 = Shop(name='Ozon')
shop3 = Shop(name='Wildberries')

stock1 = Stock(books=book5, shops=shop1, count=2)
stock2 = Stock(books=book2, shops=shop1, count=1)
stock3 = Stock(books=book1, shops=shop3, count=3)
stock4 = Stock(books=book6, shops=shop2, count=2)
stock5 = Stock(books=book4, shops=shop1, count=1)
stock6 = Stock(books=book3, shops=shop3, count=3)

sale1 = Sale(price=500, date_sale='2020-05-19', stocks=stock1, count=1)
sale2 = Sale(price=700, date_sale='2020-08-09', stocks=stock1, count=2)
sale3 = Sale(price=800, date_sale='2020-10-15', stocks=stock2, count=1)
sale4 = Sale(price=600, date_sale='2020-11-09', stocks=stock3, count=2)
sale5 = Sale(price=600, date_sale='2020-12-04', stocks=stock6, count=3)
sale6 = Sale(price=900, date_sale='2021-01-14', stocks=stock4, count=2)
sale7 = Sale(price=600, date_sale='2021-06-24', stocks=stock5, count=3)

session.add_all([author1, author2, author3])
session.add_all([book1, book2, book3, book4, book5, book6])
session.add_all([shop1, shop2, shop3])
session.add_all([stock1, stock2, stock3, stock4, stock5, stock6])
session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7])
session.commit()  


if __name__ == '__main__':
    while True:
        name = input('Enter name publisher: ')
        if name in ['Pushkin', 'Dostoevsky', 'Gogol']:
            break
        else:
            print("This publisher is not in our stores!")
    q = session.query(Publisher).filter(Publisher.name == name)
    for p in q.all():
        for b in p.books:
            for st in b.stock:
                for sl in st.sale:
                    print(b.title, '|', st.shops.name, '|', sl.date_sale, '|', sl.price)


    

        
