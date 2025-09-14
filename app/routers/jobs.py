from fastapi import APIRouter

router = APIRouter()

@router.get("/jobs")
def test():
    return {"message": "Hello"}
