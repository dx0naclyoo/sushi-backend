from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/{id}")
def sign_in(id: int):
    return {"message": id}


