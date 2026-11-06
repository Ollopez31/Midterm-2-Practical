from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class CommentBase(SQLModel):
    autor: str
    texto: str

class Comment(CommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: int = Field(foreign_key="videos.id")
    video: Optional["Videos"] = Relationship(back_populates="comentarios")

class CommentCreate(CommentBase):
    pass

class VideosBase(SQLModel):
    titulo: str
    source: str
    es_publico: bool
    categoria: str
    miniatura: str
    vistas: int = Field(default=0)
    creador: str = Field(default="Oliver Lopez")

class Videos(VideosBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comentarios: List[Comment] = Relationship(back_populates="video")

class VideosCreate(VideosBase):
    pass