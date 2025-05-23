from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean, default=False)  
    role_id = Column(Integer(), ForeignKey('roles.id'))

    role = relationship("Role", back_populates="auditions")
      
    def call_back(self):
        self.hired = True

    def __repr__(self):
        return f"<Audition(actor='{self.actor}', location='{self.location}', hired={self.hired})>"

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())

    auditions = relationship("Audition", back_populates="role", cascade="all, delete-orphan") 

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    @property
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "no actor has been hired for this role"
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role"

    def __repr__(self):
        return f"<Role(character_name='{self.character_name}')>"