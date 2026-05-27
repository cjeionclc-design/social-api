from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Like, Post, User
from app.schemas import LikeOut

router = APIRouter(prefix="/api/posts", tags=["点赞"])


@router.post("/{post_id}/like", response_model=LikeOut)
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="帖子不存在")

    existing = db.query(Like).filter(Like.user_id == current_user.id, Like.post_id == post_id).first()

    if existing:
        db.delete(existing)
        db.commit()
        liked = False
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.add(like)
        db.commit()
        liked = True

    like_count = db.query(Like).filter(Like.post_id == post_id).count()
    return LikeOut(liked=liked, like_count=like_count)
