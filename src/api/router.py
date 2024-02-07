from fastapi import APIRouter

from api.trees import router as trees_router

router = APIRouter()

router.include_router(trees_router)
