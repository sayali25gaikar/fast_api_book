import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./book_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy models
class Book(Base):
	__tablename__ = "books"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	description = Column(String, index=True)


Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()


# CRUD operations
# Create (Create)
@app.post("/books/")
async def create_item(name: str, description: str):
	db = SessionLocal()
	db_item = Book(name=name, description=description)
	db.add(db_item)
	db.commit()
	db.refresh(db_item)
	return db_item


# Read (GET)
@app.get("/books/{book_id}")
async def read_item(book_id: int):
	db = SessionLocal()
	item = db.query(Book).filter(Book.id == book_id).first()
	if not item:
		raise HTTPException(status_code=404, detail="Book not found")
	return item


# Update (PUT)
@app.put("/books/{book_id}")
async def update_book(book_id: int, name: str, description: str):
	db = SessionLocal()
	db_item = db.query(Book).filter(Book.id == book_id).first()
	if not db_item:
		raise HTTPException(status_code=404, detail="Book not found")
	db_item.name = name
	db_item.description = description
	db.commit()
	return db_item


# Delete (DELETE)
@app.delete("/books/{book_id}")
async def delete_item(book_id: int):
	db = SessionLocal()
	db_item = db.query(Book).filter(Book.id == book_id).first()
	if not db_item:
		raise HTTPException(status_code=404, detail="Book not found")
	db.delete(db_item)
	db.commit()
	return {"message": "Item deleted successfully"}


if __name__ == "__main__":
	uvicorn.run(app)
