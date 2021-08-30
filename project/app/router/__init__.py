from fastapi import APIRouter

from project.app.router.hero import router as hero_router
from project.app.router.team import router as team_router

router = APIRouter()

router.include_router(hero_router, prefix="/hero", tags=["heros"])
router.include_router(team_router, prefix="/team", tags=["team"])