from fastapi import Depends, FastAPI
from models import Product
import database_models
from  database import session,engine
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello fast api server"


products = [
    Product(name="phone",description="Phone description",price=10.12,quantity=2),
    Product(name="car",description="car description",price=1000.12,quantity=1)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

##get all products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    products = db.query(database_models.Product).all()
    return products

# add items manually to database 

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    print(count)
    if(count==0):
        for product in products:
            db_product = database_models.Product(
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity
            )
            db.add(db_product)
        db.commit()

init_db()
##get products by id
@app.get("/product/{id}")
def get_all_by_id(id:int,db:Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if product:
        return product
    return "Not found"

##posting the product
@app.post("/product")
def add_product(product:Product, db:Session= Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())
        
    db.add(db_product)
    db.commit()
    
    

@app.put("/product")
def update_product(id:int , Lproduct:Product,db:Session= Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    print (Lproduct)
    print(product)
    if product:
        product.name= Lproduct.name
        product.description = Lproduct.description
        product.price = Lproduct.price
        product.quantity = Lproduct.quantity
        db.commit()
        return 
    else:
        return "No product found"

@app.delete("/product")
def delete_product(id:int,Lproduct:Product,db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if product:
        db.delete(product)
        db.commit()
        return [product,"Is deleted Successfully"]
    else:
        return "Product Not found"