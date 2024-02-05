from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/{id}")
def get_order(id: int):
    return {"message": id}


