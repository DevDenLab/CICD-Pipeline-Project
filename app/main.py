"""
Tiny FastAPI service for the CI/CD POC.

Endpoints:
  GET    /health        -> liveness check (the pipeline & orchestrators poll this)
  GET    /items         -> list all items
  POST   /items         -> create an item
  GET    /items/{id}    -> fetch one item
  DELETE /items/{id}    -> delete one item

Storage is a plain in-memory dict. It resets every time the container restarts.
That is intentional for a POC -- it keeps the focus on the pipeline, not a database.
(Persisting data across deploys is its own topic: volumes / managed databases.)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import this_module_does_not_exist

app = FastAPI(title="CICD POC API", version="1.0.0")

# --- "database": a dict that lives in memory for the container's lifetime ---
items: dict[int, dict] = {}
_next_id = 1


class ItemIn(BaseModel):
    """Shape of the JSON body a client sends when creating an item."""
    name: str
    price: float


@app.get("/health")
def health():
    """
    Liveness endpoint. Returns 200 when the app is up.
    CI/CD deploy steps and reverse proxies hit this to decide 'is it ready?'
    """
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return list(items.values())


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    global _next_id
    record = {"id": _next_id, "name": item.name, "price": item.price}
    items[_next_id] = record
    _next_id += 1
    return record


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return None
