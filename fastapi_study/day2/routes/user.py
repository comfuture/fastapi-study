from fastapi import APIRouter, Depends, HTTPException, Path, Response, Body
from fastapi_study.day2.db import AsyncSession, use_db, SQLAlchemyError, op
from fastapi_study.day2 import model, schema

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/', response_model=schema.UserEntryList)
async def list_users(session: AsyncSession = Depends(use_db)):
    """모든 사용자를 나열합니다"""
    try:
        result = await session.execute(op.select(model.User))
        users = [schema.UserEntry.from_orm(user) for user in result.scalars()]
        return schema.UserEntryList(items=users)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post('/', status_code=201)
async def create_user(session: AsyncSession = Depends(use_db),
                      user: schema.UserBase = Body(...)):
    """사용자를 생성합니다"""
    async with session.begin():
        user_model = model.User(**user.dict())
        session.add(user_model)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e)) from e
        return {'message': 'user added', 'item_id': user_model.id, 'user': user}


@router.get('/{user_id}', response_model=schema.UserEntry)
async def get_user(session: AsyncSession = Depends(use_db), user_id: int = Path(...)):
    """`user_id`로 사용자를 가져옵니다"""
    try:
        stmt = op.select(model.User).filter(model.User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one()
        return schema.UserEntry.from_orm(user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put('/{user_id}')
async def modify_user(session: AsyncSession = Depends(use_db),
                      user_id: int = Path(...),
                      changes: schema.UserBase = Body(...)):
    """사용자 속성을 수정합니다"""
    async with session.begin():
        await session.execute(op.update(model.User)
                                .where(model.User.id == user_id)
                                .values(changes.dict()))
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e)) from e
        return {'message': 'user modified', 'changes': changes}


@router.delete('/{user_id}', status_code=204)
async def delete_user(session: AsyncSession = Depends(use_db),
                      user_id: int = Path(...)):
    """사용자를 삭제합니다"""
    async with session.begin():
        stmt = op.delete(model.User).where(model.User.id == user_id)
        await session.execute(stmt)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e)) from e
        return Response(status_code=204)
