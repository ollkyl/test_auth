from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base


class BusinessElement(Base):
    __tablename__ = "business_elements"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    rules = relationship("AccessRule", back_populates="element")


class AccessRule(Base):
    __tablename__ = "access_rules"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    element_id = Column(Integer, ForeignKey("business_elements.id"))

    can_read = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

    role = relationship("Role", back_populates="rules")
    element = relationship("BusinessElement", back_populates="rules")
