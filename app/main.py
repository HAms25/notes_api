from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
import uuid

app = FastAPI(
    title = "API de Notas",
    description = "Una API para gestionar notas usando FastAPI",
    version="1.0.0"
)

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
@app.get("/notes", summary = "Obtener todas las notas")
def get_notes(title: str = None):
    if title:
        filtered_notes = [note for note in notes_db if title.lower() in note.title.lower()]
        return filtered_notes
    return notes_db

#Crear notas
@app.post("/notes", summary = "Crear nota")
def create_note(note_data: NoteCreate):
    for n in notes_db:
        if n.title == note_data.title:
            raise HTTPException(status_code=400, detail="Ya existe una nota con este titulo")
        
    new_note = Note(id=str(uuid.uuid4()), **note_data.dict())
    notes_db.append(new_note)
    return {"message": "Nota creada", "note": new_note}

#Actualizar nota
@app.put("/notes/{note_id}", summary = "Actualizar notas")
def update_note(note_id: str, update_data: NoteCreate):
    for note in notes_db:
        if note.id == note_id:
            note.title = update_data.title
            note.content = update_data.content
            return {"message": "Nota actualizada", "note": note}
    
    raise HTTPException(status_code=404, detail="Nota no encontrada")

#Eliminar nota
@app.delete("/notes/{note_id}", summary = "Eliminar nota")
def delete_note(note_id: str):
    global notes_db
    if not any(note.id == note_id for note in notes_db):
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    notes_db = [note for note in notes_db if note.id != note_id]
    return {"message": "Nota eliminada"}
