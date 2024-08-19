![python](https://img.shields.io/badge/python-3.12-blue)

# Prisma ORM example

This is a simple example of how to use [Prisma ORM](https://www.prisma.io/) with a PostgreSQL database.
Our example is a Python app, so we will also use the [Prisma Client Python](https://prisma-client-py.readthedocs.io/en/stable/) to interact with the database.

## Table of contents

- [Setup the environment](#setup-the-environment)
- [Create a schema](#create-a-schema)
- [Create a migration](#create-a-migration)

## Setup the environment

I use [Poetry](https://python-poetry.org/) to manage the dependencies of the project. You can initialize it with the following command:

```bash
poetry init
```

Then, we will install the prisma dependency and initialize the project:

```bash
poetry add prisma
primsa init
```

The `init` command will create the `prisma/schema.prisma` file, where we will define the database schema. You can 
specify a different location if needed with the parameter `--schema` as explained [here](https://www.prisma.io/docs/orm/prisma-schema/overview/location).
The `init` command will also generate a `.env` file to store the database connection string for the current environment.

If you are using the PostgreSQL database provided by the docker-compose file, you can set the connection string in 
the `.env` file like this:

```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres?schema=public"
```

As we are testing Prisma with a Python backend, we have to change the default generator in the generated `schema.prisma` file to the Python one:

```bash
generator client {
  provider = "prisma-client-py"
  recursive_type_depth = 5
}
```

Even if we currently have no models in our Prisma schema nor entities in the database, we can use the `prisma db pull` 
command to check our setup:

```bash
prisma db pull

# Output for a good setup
Prisma schema loaded from prisma/schema.prisma
Environment variables loaded from .env
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

✖ Introspecting based on datasource defined in prisma/schema.prisma
Error: 
P4001 The introspected database was empty:

prisma db pull could not create any models in your schema.prisma file and you will not be able to generate Prisma Client with the prisma generate command.

To fix this, you have two options:

- manually create a table in your database.
- make sure the database connection URL inside the datasource block in schema.prisma points to a database that is not empty (it must contain at least one table).

Then you can run prisma db pull again. 

# Output for a bad setup
Prisma schema loaded from prisma/schema.prisma
Environment variables loaded from .env
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

✖ Introspecting based on datasource defined in prisma/schema.prisma

Error: P1000

Authentication failed against database server at `localhost`, the provided database credentials for `test` are not valid.

Please make sure to provide valid database credentials for the database server at `localhost`.
```

Our project is now ready to play with Prisma! 🎉

## Create a schema

We will begin by creating a simple schema with a `User` model. We will define the model in the `schema.prisma` file:

```prisma
model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
}
```

> Tips: We can check that the `schema.prisma` file is valid by running the `prisma validate` command.

No we can use the `prisma db push` to synchronize the database with our schema:

```bash
prisma db push 
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

🚀  Your database is now in sync with your Prisma schema. Done in 64ms

Running generate... - Prisma Client Python (v0.15.0)

✔ Generated Prisma Client Python (v0.15.0) to ./../../../../../Library/Caches/pypoetry/virtualenvs/prisma-orm-example-2L4QBR3R-py3.12/lib/python3.12/site-packages/prisma in 71ms
```

If we check in the database, we can see that the `User` table has been created as expected:

![User table](./docs/images/db_first_push.png)

We have created our first model with Prisma! 🎉

## Create a migration

Now we will complete a little bit our schema:

```prisma
model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
  posts     Post[]
}

model Post {
  id        Int       @id @default(autoincrement())
  title     String
  content   String
  published Boolean   @default(false)
  author    User?     @relation(fields: [authorId], references: [id])
  authorId  Int?
  createdAt DateTime  @default(now())
  comments  Comment[]
}

model Comment {
  id        Int      @id @default(autoincrement())
  content   String
  post      Post     @relation(fields: [postId], references: [id])
  postId    Int
  createdAt DateTime @default(now())
}
```

And apply the changes to the database using `prisma db push`.

Now, if we want to version this schema in Git, we can generate a migration with the `prisma migrate dev` command:

```bash
prisma migrate dev
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

Drift detected: Your database schema is not in sync with your migration history.

The following is a summary of the differences between the expected database schema given your migrations files, and the actual schema of the database.

It should be understood as the set of changes to get from the expected schema to the actual schema.

If you are running this the first time on an existing database, please make sure to read this documentation page:
https://www.prisma.io/docs/guides/database/developing-with-prisma-migrate/troubleshooting-development

[+] Added tables
  - Comment
  - Post
  - User

[*] Changed the `Comment` table
  [+] Added foreign key on columns (postId)

[*] Changed the `Post` table
  [+] Added foreign key on columns (authorId)

[*] Changed the `User` table
  [+] Added unique index on columns (email)

✔ We need to reset the "public" schema at "localhost:5432"
Do you want to continue? All data will be lost. … yes

✔ Enter a name for the new migration: … schema init
Applying migration `20240819064523_schema_init`

The following migration(s) have been created and applied from new schema changes:

migrations/
  └─ 20240819064523_schema_init/
    └─ migration.sql

Your database is now in sync with your schema.

✔ Generated Prisma Client Python (v0.15.0) to ./../../../../../Library/Caches/pypoetry/virtualenvs/prisma-orm-example-2L4QBR3R-py3.12/lib/python3.12/site-packages/prisma in 78ms
```

As explained in the output, Prisma need to first reset the database to generate and apply the migration scripts.
> Migration scripts are generated in the `prisma/migrations` folder. 

In order to generate a new migration script, we will add the notion of User group in our schema:

```prisma
model Group {
  id    Int    @id @default(autoincrement())
  name  String
  users User[]
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
  posts     Post[]
  group     Group?   @relation(fields: [groupId], references: [id])
  groupId   Int?
}
```

It's not mandatory to apply the changes to the database using `prisma db push`.
We can directly generate the corresponding migration script with `prisma migrate dev`:

```bash
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Datasource "db": PostgreSQL database "postgres", schema "public" at "localhost:5432"

✔ Enter a name for the new migration: … add group model
Applying migration `20240819065840_add_group_model`

The following migration(s) have been created and applied from new schema changes:

migrations/
  └─ 20240819065840_add_group_model/
    └─ migration.sql

Your database is now in sync with your schema.

✔ Generated Prisma Client Python (v0.15.0) to ./../../../../../Library/Caches/pypoetry/virtualenvs/prisma-orm-example-2L4QBR3R-py3.12/lib/python3.12/site-packages/prisma in 80ms
```

We now have multiple migration scripts in the `prisma/migrations` folder in order to track each change:
- 20240819064523_schema_init
- 20240819065840_add_group_model 

