from fastapi import APIRouter

router = APIRouter()

@router.get("/applications")
def test():
    return {"message": "Hello"}
