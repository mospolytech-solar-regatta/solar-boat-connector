from typing import Annotated

from fastapi import Depends

from app.client import redis, postgres
from app.context import Context, ContextFactory

context_factory = ContextFactory(redis, postgres)

context_dep = Annotated[Context, Depends(context_factory)]
