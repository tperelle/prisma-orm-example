![python](https://img.shields.io/badge/python-3.12-blue)

# Prisma ORM example

This is a simple example of how to use [Prisma ORM](https://www.prisma.io/) with a PostgreSQL database.
Our example is a Python app, so we will also use the [Prisma Client Python](https://prisma-client-py.readthedocs.io/en/stable/) to interact with the database.

## Table of contents

- [Setup](#setup-the-environment)

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


