from sqlalchemy.orm import Session
from . import models


def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.company_id == company_id).first()

def get_company_by_ticker(db: Session, ticker: str):
    return db.query(models.Company).filter(models.Company.ticker == ticker).first()

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, name: str, ticker: str):
    db_company = models.Company(name=name, ticker=ticker)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.article_id == article_id).first()

def get_article_by_href(db: Session, href: int):
    return db.query(models.Article).filter(models.Article.href == href).first()

def get_articles_by_date(db: Session, date: str, skip: int = 0, limit: int = 100):
    return db.query(models.Article).filter(models.Article.date == date).offset(skip).limit(limit).all()

def create_article(db: Session, title: str, text: str, href: str, date: str):
    db_article = models.Article(title=title, text=text, href=href, date=date)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article 

def update_article(db: Session, db_article: models.Article, db_company: models.Company):
    if db_company in db_article.companies:
        return db_article
    db_article.companies.append(db_company)
    db.commit()
    db.refresh(db_article)
    return db_article
