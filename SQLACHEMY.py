from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///customer_orders.db', echo=True)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Customers'

    CustomerID = Column('CustomerID', Integer, primary_key=True)
    Name = Column('Name', String)
    Email = Column('Email', String)
    Phone = Column('Phone', String)
    Address = Column('Address', String)

    orders = relationship('Order', back_populates='customer')

    def __init__(self, Name, Email, Phone, Address):
        self.Name = Name
        self.Email = Email
        self.Phone = Phone
        self.Address = Address

    def __repr__(self):
        return f"Customer(CustomerID={self.CustomerID}, Name='{self.Name}', Email='{self.Email}', Phone='{self.Phone}', Address='{self.Address}')"

class Order(Base):
    __tablename__ = 'Orders'

    OrderID = Column('OrderID', Integer, primary_key=True)
    CustomerID = Column('CustomerID', Integer, ForeignKey('Customers.CustomerID'))
    Product = Column('Product', String)
    Quantity = Column('Quantity', Integer)
    OrderDate = Column('OrderDate', Date)

    customer = relationship('Customer', back_populates='orders')

    def __init__(self, CustomerID, Product, Quantity, OrderDate):
        self.CustomerID = CustomerID
        self.Product = Product
        self.Quantity = Quantity
        self.OrderDate = OrderDate

    def __repr__(self):
        return f"Order(OrderID={self.OrderID}, CustomerID={self.CustomerID}, Product='{self.Product}', Quantity={self.Quantity}, OrderDate='{self.OrderDate}')"

Base.metadata.create_all(engine)

customer1 = Customer(Name='John Doe', Email='john@example.com', Phone='123456789', Address='123 Main St')
customer2 = Customer(Name='Jane Smith', Email='jane@example.com', Phone='987654321', Address='456 Elm St')

session.add_all([customer1, customer2])

session.commit()

order1 = Order(CustomerID=customer1.CustomerID, Product='Widget', Quantity=5, OrderDate=datetime.strptime('2023-01-01', '%Y-%m-%d').date())
order2 = Order(CustomerID=customer1.CustomerID, Product='Gadget', Quantity=3, OrderDate=datetime.strptime('2023-02-15', '%Y-%m-%d').date())
order3 = Order(CustomerID=customer2.CustomerID, Product='Widget', Quantity=10, OrderDate=datetime.strptime('2023-03-10', '%Y-%m-%d').date())

session.add_all([order1, order2, order3])

session.commit()

customers = session.query(Customer).all()
for customer in customers:
    print(customer)

orders = session.query(Order).all()
for order in orders:
    print(order)

customer_orders = session.query(Order).filter(Order.CustomerID == customer1.CustomerID).all()
for order in customer_orders:
    print(order)
