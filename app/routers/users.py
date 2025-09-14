from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def test():
    return {"message": "Hello"}
