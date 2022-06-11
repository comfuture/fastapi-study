from fastapi import APIRouter, Depends, HTTPException, Path, Response, Body
from fastapi_study.day2.db import Session, use_db, SQLAlchemyError
from fastapi_study.day2 import model, schema

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
def list_users(db: Session = Depends(use_db)):
    """모든 사용자를 나열합니다"""
    users = db.query(model.User).all()
    return {
        'users': users
    }

@router.post('/', status_code=201)
def create_user(db: Session = Depends(use_db),
                user: schema.UserBase = Body(...)):
    """사용자를 생성합니다"""
    user_model = model.User(**user.dict())
    db.add(user_model)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return HTTPException(status_code=400, detail=str(e))
    return {'message': 'user added', 'item_id': user_model.id, 'user': user}


@router.get('/{user_id}', response_model=schema.UserBase)
def get_user(db: Session = Depends(use_db), user_id: int = Path(...)):
    """`user_id`로 사용자를 가져옵니다"""
    try:
        user = db.query(model.User).filter(model.User.id == user_id).one()
        return schema.UserBase(user)
    except SQLAlchemyError as e:
        return HTTPException(status_code=400, detail=str(e))


@router.put('/{user_id}')
def modify_user(db: Session = Depends(use_db),
                user_id: int = Path(...),
                changes: schema.UserBase = Body(...)):
    """사용자 속성을 수정합니다"""
    db.query(model.User).filter(model.User.id == user_id).update(changes.dict())
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return HTTPException(status_code=400, detail=str(e))
    return {'message': 'user modified', 'changes': changes}


@router.delete('/{user_id}', status_code=204)
def delete_user(db: Session = Depends(use_db),
                user_id: int = Path(...)):
    """사용자를 삭제합니다"""
    db.query(model.User).filter(model.User.id == user_id)\
                        .delete(synchronize_session='evaluate')
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return HTTPException(status_code=400, detail=str(e))
    return Response(status_code=204)
