from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(datetime, default=datetime.utcnow)

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# crear usuarios:

UserDB1 = UserDB(name= "Alice", email= "alice@gmail.com")
UserDB2 = UserDB(name= "Bob", email= "bob@gmail.com")
session.add_all([UserDB1, UserDB2])
session.commit()

# Queries

all_UserDBs = session.query(UserDB).all()
print(all_UserDBs)

alice = session.query(UserDB).filter(UserDB.name=="Alice").first()
print(alice)

UserDBs_with_a = session.query(UserDB).filter(UserDB.name.like("%a%")).all()
print(UserDBs_with_a)

filtered_users = session.query(UserDB).filter(
    UserDB.name == "Alice",
    UserDB.email == "alice@gmail.com"
).all()
print(filtered_users)

ordered_users = session.query(UserDB).order_by(UserDB.name.desc()).all()
print(ordered_users)

limited_users = session.query(UserDB).limit(1).all()
print(limited_users)

user_count = session.query(UserDB).count()
print(user_count)

session.query(UserDB).filter(UserDB.name == "Alice").update({"email": "newemailforalice@gmail.com"})
session.commit()

session.query(UserDB).filter(UserDB.name=="Bob").delete()
session.commit()

from sqlalchemy import func

user_count = session.query(func.count(UserDB.id)).scalar()
print(user_count)

from sqlalchemy import or_, and_


