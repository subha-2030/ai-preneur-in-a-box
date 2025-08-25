import asyncio
from app.db.client_repository import get_clients_for_user
from app.services.agent_service import AgentService
from app.db.database import connect_to_mongo, close_mongo_connection
from app.models.user import User
from app.db.repository import UserRepository

async def main():
    await connect_to_mongo()
    user_repo = UserRepository()
    user = await user_repo.get_user_by_email("test@example.com")
    if not user:
        print("User not found.")
        return

    clients = await get_clients_for_user(str(user.id))
    agent_service = AgentService()

    for client in clients:
        print(f"Generating briefing for client: {client.name}")
        await agent_service.generate_briefing(
            user_id=str(user.id),
            client_name=client.name,
            meeting_date="2025-08-21T10:00:00"
        )

    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())