from fastapi import APIRouter

router = APIRouter(
    prefix="/forecast",
    tags=["forecast"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_data():
    return {"success": True}
