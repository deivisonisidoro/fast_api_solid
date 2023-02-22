# Fast API SOLID

This is a study project that demonstrates how to implement the SOLID principles using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python. The project provides a sample implementation of a web application that follows SOLID principles, with clean architecture and dependency injection.

The codebase is structured according to the Domain-Driven Design (DDD) approach, with separate directories for configuration, controllers, models, providers, repositories, schemas, templates, tests, and utilities. It also includes a main server.py file that runs the FastAPI application and a routers.py file that defines the API endpoints.

This project serves as an example of how to build scalable and maintainable web applications using modern Python tools and best practices.

## Requirements

Before getting started, you need to have the following requirements installed on your computer:

- Docker
- Docker Compose
- Pipenv

## Project Architecture

The project is organized into the following directories and files:

- `.pytest_cache` - directory for pytest cache files
- `.vscode` - directory for VS Code configuration
- `alembic` - directory for Alembic migration scripts
- `src` - directory for source code files
- `.env.example` - example environment variables file
- `.flake8` - configuration file for Flake8 linter
- `.gitignore` - Git ignore file
- `alembic.ini` - Alembic configuration file
- `docker-compose.yml` - Docker Compose configuration file
- `Dockerfile` - Dockerfile for building the Docker image
- `LICENSE` - license file
- `Pipfile` - Pipenv configuration file
- `Pipfile.lock` - Pipenv lock file
- `pyproject.toml` - configuration file for Pyproject
- `readme.md` - README file

## Using Environment Variables

This project relies on environment variables to be set in a .env file. To set up the necessary environment variables, create a copy of the `.env.example` file and rename it to `.env`. Then, fill in the values for each variable.

## Running the Project

1. Clone the repository to your computer.
2. Navigate to the project directory.
3. Run the command `pipenv install` to install the required Python dependencies.
4. Run the command `docker-compose up -d` to build and run the Docker image.
5. Open a web browser and navigate to `http://localhost:8000` to view the project's homepage.

### Viewing Logs

To view the logs for the web service, you can use the following command:

`docker-compose logs -f web`

This will show you the logs for the web service in real time.

## Database Migrations with Alembic

This project uses Alembic for database migrations. To generate a new migration script, run the following command:

`docker-compose exec web alembic revision --autogenerate -m "description of migration"`

This will generate a new migration script in the `alembic/versions` directory.

To apply the migration to the database, run the following command:

`docker-compose exec web alembic upgrade head`

## Contributing

1. Fork the project.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Adding new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## Code Standardization

This project follows the guidelines of [PEP 8](https://www.python.org/dev/peps/pep-0008/) and uses the [Black](https://github.com/psf/black) tool to maintain consistent code formatting. In addition, it is recommended to use the [PyLint](https://www.pylint.org/) tool for static code analysis.

## API Documentation

The API documentation can be accessed by opening a web browser and navigating to `http://localhost:8000/docs` or `http://localhost:8000/redoc`. This will display the Swagger UI or ReDoc where you can view and test the API endpoints.

## Testing

This project uses pytest for testing. To run the tests, run the following command:

`docker-compose exec web pytest`

This will run all the tests in the `tests` directory.

## License

This project is licensed under the MIT license. Please see the LICENSE file for more information.
