from sqlalchemy.orm import Session
from models import Note
import schemas

def get_notes(db: Session, user_id: int):
    return db.query(Note).filter(Note.owner_id == user_id).all()

def get_note(db: Session, note_id: int, user_id: int):
    return db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note: schemas.NoteUpdate, user_id: int):
    db_note = get_note(db, note_id, user_id)
    if db_note:
        for key, value in note.dict().items():
            setattr(db_note, key, value)
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    db_note = get_note(db, note_id, user_id)
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note
