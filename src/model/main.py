from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_company(name: str, ticker: str, db: Session = next(get_db())):
    db_company = crud.get_company_by_ticker(db, ticker=ticker)
    if db_company:
        return f"Company with ticker: '{ticker}' already exists in database"
    return crud.create_company(db=db, name=name, ticker=ticker)

def add_article(ticker: str, title: str, text: str, href: str, date: str, db: Session = next(get_db())):
    db_article = crud.get_article_by_href(db, href=href)
    if not db_article:
        db_article = crud.create_article(db=db, title=title, text=text, href=href, date=date)
    db_company = crud.get_company_by_ticker(db, ticker=ticker)
    return crud.update_article(db=db, db_article=db_article, db_company=db_company)
