"""GraphQL per-request context — injects a DB session into `info.context`
so resolvers can use the same repository classes as the REST layer."""
from strawberry.fastapi import BaseContext

from app.infrastructure.db.session import AsyncSessionLocal


class GraphQLContext(BaseContext):
    def __init__(self):
        super().__init__()
        self.db = None


async def get_graphql_context():
    async with AsyncSessionLocal() as session:
        yield {"db": session}
