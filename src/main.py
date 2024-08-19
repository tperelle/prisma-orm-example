from prisma import Prisma
import asyncio

async def queries() -> None:
    db = Prisma()
    await db.connect()

    # Execute queries on our schema managed by Prisma
    users = await db.user.find_many(
        include={
            'group': True,
            'posts': {
                'include': {
                    'comments': True
                }
            }
        },
    )

    print(f'List of users:')
    for user in users:
        print(user.model_dump_json(indent=2))

    await db.disconnect()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(queries())
