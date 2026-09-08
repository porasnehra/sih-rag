import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class StandardRecord(Base):
    __tablename__ = 'standard_records'

    id = Column(Integer, primary_key=True)
    is_number = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    scope = Column(Text, nullable=True)
    product_category = Column(String, nullable=True)
    certification_scheme = Column(String, nullable=True)
    testing_requirements = Column(Text, nullable=True)
    lab_info = Column(Text, nullable=True)
    url = Column(String, nullable=True)
    last_updated = Column(Date, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "is_number": self.is_number,
            "title": self.title,
            "scope": self.scope,
            "product_category": self.product_category,
            "certification_scheme": self.certification_scheme,
            "testing_requirements": self.testing_requirements,
            "lab_info": self.lab_info,
            "url": self.url,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }

# Database setup
db_path = os.path.join(os.path.dirname(__file__), 'bis_standards.db')
engine = create_engine(f'sqlite:///{db_path}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
