from prisma import Prisma
import asyncio

async def seed() -> None:
    db = Prisma()
    await db.connect()

    group1 = await db.group.create({
        'name': 'Group 1'
    })
    user1 = await db.user.create({
        'name': 'User 1',
        'email': 'user1@gravitek.io',
        'group': {
            'connect': {
                'id': group1.id
            }
        }
    })
    post1 = await db.post.create({
        'title': 'Post 1',
        'content': 'My great paragraph',
        'author': {
            'connect': {
                'id': user1.id
            }
        }
    })
    comment1 = await db.comment.create({
        'content': 'Comment 1',
        'post': {
            'connect': {
                'id': post1.id
            }
        }
    })

    await db.disconnect()


if __name__ == '__main__':
    asyncio.run(seed())