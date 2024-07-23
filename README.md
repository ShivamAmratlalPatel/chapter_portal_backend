# Chapter Portal Backend

## Code Structure

- `/backend` contains the FastAPI backend code
- `/testing` contains the testing code
- `/alembic` contains the database migration code
- `/scripts` contains the scripts to run the backend and the database migrations
- `/.github` contains the GitHub Actions workflows
- `.pre-commit-config.yaml` contains the pre-commit configuration
- `pyproject.toml` contains the Python dependencies. This file is used by Poetry to manage the dependencies. It contains
  the project metadata, the dependencies, and the development dependencies. It also contains configuration for black,
  ruff and coverage.
- `poetry.lock` contains the Poetry lock file. This file is used to lock the dependencies versions to ensure consistent
  builds.
- `README.md` contains the documentation.
- `Dockerfile` contains the Dockerfile for the backend. This file is used to build the Docker image for the backend.
- `docker-compose.yml` contains the Docker Compose file for the backend and the database. This file is used to run the
  backend and the database in Docker containers.
- `alembic.ini` contains the Alembic configuration. This file is used by the Alembic CLI to run the database migrations.

Within backend file, the code is structured as follows:

- `main.py` contains the FastAPI application. This file is used to create the FastAPI application and create the
  application.
- `middleware.py` contains the middleware for the FastAPI application. This file is used to add middleware to the
  FastAPI application. Middleware is code that runs before and after the request is processed by the FastAPI
  application.
- `helpers.py` contains helper functions for the FastAPI application. This file is used to define helper functions that
  are used throughout the FastAPI application. Currently this is just the `get_db` function which is used to get
  the `database session` from the request.
- `database.py` contains the database configuration. This file is used to configure the database connection and create
  the database session.
- `config.py` contains the configuration for the FastAPI application. This file is used to define the configuration
  settings for the FastAPI application. The configuration settings are loaded from environment variables.
- `__init__.py` is an empty file that tells Python that the directory should be treated as a package.
- `schemas.py` contains the general Pydantic schemas for the FastAPI application. This file is used to define the
  Pydantic schemas that are used to validate the request and response data.
- `utils.py` contains utility functions for the FastAPI application. This file is used to define utility functions that
  are used throughout the FastAPI application.
- The rest of the code is split into folders which contain:
    - `routes` files which contain the route definitions for the FastAPI application. These files are used to define the
      routes for the FastAPI application.
    - `models` files which contain the database models for the FastAPI application. These files are used to define the
      database models for the FastAPI application.
    - `schemas` files which contain the Pydantic schemas for the FastAPI application. These files are used to define the
      Pydantic schemas that are used to validate the request and response data.
    - `commands` folder which contain functions are used in the routes or across the application.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- [Python 3.11](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ShivamAmratlalPatel/chapter_portal_backend
    ```

2. Navigate to the repository:

    ```bash
    cd chapter-portal-backend
    ```

3. Install project dependencies using Poetry:

    ```bash
    poetry install
    ```

## Running the Application

To start the FastAPI application, follow these steps:

1. Start the application using Docker Compose:

    ```bash
    docker-compose up
    ```

2. Migrate the database:

    ```bash
    docker exec -it chapter-portal-backend sh ./scripts/migrate.sh
    ```

3. Navigate to the application's Swagger documentation at [http://localhost:8001/docs](http://localhost:8001/docs).

## Generating a New Migration

If you have made changes to the database models, you will need to generate a new migration. To do this:

1. Make sure the application is running.
2. In /scripts/generate_migration.sh, change the `$x` to a description of the migration
   e.g. `add new column to user model`.
3. Run the following command:

```bash
docker exec -it chapter_portal_backend-local sh ./scripts/generate_migration.sh
```

## Testing

To run all tests, run:

```bash
docker exec -it chapter_portal_backend-local pytest
```

To run a specific test, run:

```bash
docker exec -it chapter_portal_backend-local pytest ./testing/test_file.py::test_name
```

## Pre-commit Hooks

This project includes pre-commit hooks, which are automated checks that run before each commit to ensure code quality
and maintain consistency. The hooks are managed using [pre-commit](https://pre-commit.com/).

To set up the pre-commit hooks, run the following command after installing the project dependencies:

 ```bash
 poetry run pre-commit install
 ```

You can check it worked by running manually with:

 ```bash
 poetry run pre-commit run --all-files
 ```

## Linting

This project uses [ruff](https://beta.ruff.rs/docs/) for linting. To run the linter, run the following command:

```bash
poetry run ruff check .
```

Optionally you can run the linter with the `--fix` flag to automatically fix any linting errors:

```bash
poetry run ruff check . --fix
```

## Formatting

This project uses [black](https://black.readthedocs.io/en/stable/) for formatting. To run the formatter, run the
following command:

```bash
poetry run black .
```

This project also uses [isort](https://pycqa.github.io/isort/) for sorting imports. To run the import sorter, run the
following command:

```bash
poetry run isort .
```

Both of these run with pre-commit hooks, so you shouldn't need to run them manually.

## PyCharm Setup

### Python Interpreter

For this project, you can either use a local Python interpreter or a Docker interpreter.
The Docker interpreter is recommended as it will be more consistent across different machines.
The Docker interpreter will be needed to run tests which require a database.

#### Docker Interpreter

1. Open the project in PyCharm.
2. Go to `File > Settings > Project: chapter-portal-backend > Python Interpreter`.
3. Click the gear icon and select `Add`.
4. Select `On Docker Compose`.
5. Select the `docker-compose.yml` file in the root of the project.
6. Select the `backend` service.
7. Click `Next`.
8. Click `Next` again.
9. Select `System Interpreter`.
10. The interpreter path should be `/usr/local/bin/python`, not `/usr/local/bin/python3`.
11. Click `Create`.
12. Set the chapter-portal-backend folder as the sources root

#### Local Interpreter

1. Open the project in PyCharm.
2. Go to `File > Settings > Project: chapter-portal-backend > Python Interpreter`.
3. Click the gear icon and select `Add`.
4. Select `Add Local Interpreter`.
5. Select `Poetry Environment` from the left-hand menu.
6. Make sure the base interpreter is set to your local Python 3.11 installation.
7. Click `OK`.

### Running tests in PyCharm

1. Go to `Run > Edit Configurations`.
2. Click the `+` icon and select `Python tests > pytest`.
3. Set the name to `pytest`.
4. Set the target to `Script path` and enter the testing directory.
5. Make sure the interpreter is set to the Docker interpreter.
6. Set the working directory to the root of the project.

#### Running an individual test

1. Click the play button next to the test you want to run.
2. Initially this will fail as the working directory is not set correctly.
3. Click edit configuration and set the working directory to the root of the project.
4. Rename the test path to include the path from the root of the project to the test file.
5. Click `OK`.
6. Click the play button again.

### Commit settings

1. Go to `File > Settings > Version Control > Commit`.
2. There you can have PyCharm automatically run the tests on each commit by selecting `Run tests` and selecting
   the `pytest` configuration.
3. Also selecting `Run git hooks` will run the pre-commit hooks on each commit.

### File Watchers

1. Go to `File > Settings > Tools > File Watchers`.
2. Click the `+` icon and select `Custom`.
3. Set the name to `black`.
4. Set the file type to `Python`.
5. Set the scope to `Project Files`.
6. Set the program to the Docker interpreter.
7. Set the arguments to `black --quiet $FilePathRelativeToProjectRoot$`.
8. Set the working directory to `$ProjectFileDir$`.
9. Click `OK`.

### Actions on Save

1. Go to `File > Settings > Tools > Actions on Save`.
2. Disable `Reformat code`.
3. Enable `Run File Watchers`.

### Backend Import Errors

If you are getting import errors in the backend, try setting chapter-portal-backend as a Sources Root.