from sqlalchemy.orm import Session

from .models import ShoppingItem


def get_items(db: Session):
    return db.query(ShoppingItem).all()


def add_item(db: Session, item_name: str) -> ShoppingItem:
    new_item = ShoppingItem(name=item_name)
    db.add(new_item)
    db.commit()
    return new_item


def remove_item(db: Session, item_id: int):
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()


def update_item(db, item_id: int, new_name: str):
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if item:
        item.name = new_name
        db.commit()
        db.refresh(item)
