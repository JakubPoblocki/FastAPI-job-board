from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def test():
    return {"message": "Hello"}
