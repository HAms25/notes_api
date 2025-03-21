from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
import uuid

app = FastAPI()

class NoteCreate(BaseModel):
    title: str
    content: str

#Definir modelo de datos
class Note(NoteCreate):
    id:str

#Base de datos
notes_db: List[Note] = []

#Endpoint para obtener todas las notas

#Obtener notas
@app.get("/notes")
def get_notes():
    return notes_db

#Crear notas
@app.post("/notes")
def create_note(note_data: NoteCreate):
    for n in notes_db:
        if n.title == note_data.title:
            raise HTTPException(status_code=400, detail="Ya existe una nota con este titulo")
        
    new_note = Note(id=str(uuid.uuid4()), **note_data.dict())
    notes_db.append(new_note)
    return {"message": "Nota creada", "note": new_note}

#Actualizar nota
@app.put("/notes/{note_id}")
def update_note(note_id: str, update_data: NoteCreate):
    for note in notes_db:
        if note.id == note_id:
            note.title = update_data.title
            note.content = update_data.content
            return {"message": "Nota actualizada", "note": note}
    
    raise HTTPException(status_code=404, detail="Nota no encontrada")

#Eliminar nota
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for i, n in enumerate(notes_db):
        if n.id == note_id:
            del notes_db[i]
            return {"message": "Nota eliminada"}
        
    raise HTTPException(status_code=404, detail="Nota no encontrada")
        
    
