from .auth import router as auth_router
from .projects import router as projects_router
from .step1 import router as step1_router
from .step2 import router as step2_router
from .step3 import router as step3_router
from .step4 import router as step4_router

__all__ = [
    "auth_router",
    "projects_router",
    "step1_router",
    "step2_router",
    "step3_router",
    "step4_router"
]
