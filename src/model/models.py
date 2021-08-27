from sqlalchemy import Column, Integer, Text, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship

from .database import Base

article_company = Table(
    "article_company",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.article_id")),
    Column("company_id", Integer, ForeignKey("company.company_id")),
)

class Article(Base):
    __tablename__ = "article"

    article_id = Column(Integer, primary_key=True)
    title = Column(Text)
    text = Column(Text)
    href = Column(Text)
    date = Column(Text)
    companies = relationship(
        "Company", secondary=article_company, back_populates="articles"
    )

class Company(Base):
    __tablename__ = "company"

    company_id = Column(Integer, primary_key=True)
    name = Column(Text)
    ticker = Column(Text)
    articles = relationship(
        "Article", secondary=article_company, back_populates="companies"
    )
