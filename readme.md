# Anime Search API

This project is an example of a web application using FastAPI and Docker to provide a simple API for searching anime titles.

## Requirements

Before getting started, you need to have the following requirements installed on your computer:

- Docker
- Docker Compose

## Running the Project

1. Clone the repository to your computer.
2. Navigate to the project directory.
3. Run the command `docker-compose up` to build and run the Docker image.
4. Open a web browser and navigate to `http://localhost:8000` to view the project's homepage.

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
