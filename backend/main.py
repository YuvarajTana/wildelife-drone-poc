from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"} 


@app.get("/items")
def read_items():
    return {"message": "Items!"}


@app.post("/items")
def create_item():
    return {"message": "Item created!"}

@app.put("/items/{item_id}")
def update_item(item_id: int ):  
    return {"message": "Item updated!"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "Item deleted!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"message": "Item!", "item_id": item_id}