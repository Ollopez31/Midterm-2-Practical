import random
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status
from db import SessionDep
from models import Videos, VideosCreate, Comment, CommentCreate

router = APIRouter(prefix="/videos")

@router.get("/")
def get_videos(session: SessionDep):
    return session.exec(select(Videos)).all()

@router.get("/{video_id}")
def get_video_by_id(video_id: int, session: SessionDep):
    video_db = session.get(Videos, video_id)
    if not video_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video no encontrado"
        )
    return video_db

@router.post("/")
def create_video(video_data: VideosCreate, session: SessionDep):
    video = Videos.model_validate(video_data.model_dump())
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

@router.get("/{video_id}/recomendaciones")
def get_recomendaciones(video_id: int, session: SessionDep):
    video_actual = session.get(Videos, video_id)
    if not video_actual:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    
    statement = select(Videos).where(Videos.categoria == video_actual.categoria).where(Videos.id != video_id)
    videos_relacionados = session.exec(statement).all()
    
    recomendaciones = random.sample(videos_relacionados, min(len(videos_relacionados), 10))
    return recomendaciones

@router.post("/{video_id}/comentarios")
def crear_comentario(video_id: int, comentario: CommentCreate, session: SessionDep):
    video = session.get(Videos, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    
    db_comment = Comment(texto=comentario.texto, autor=comentario.autor, video_id=video_id)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment

@router.get("/{video_id}/comentarios")
def get_comentarios(video_id: int, session: SessionDep):
    statement = select(Comment).where(Comment.video_id == video_id)
    return session.exec(statement).all()