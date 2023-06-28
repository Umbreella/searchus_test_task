from fastapi import APIRouter

from . import ListDocRouter, SingleDocRouter

router = APIRouter()

router.include_router(ListDocRouter.router)
router.include_router(SingleDocRouter.router)
