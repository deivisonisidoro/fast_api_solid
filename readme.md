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

## Project Structure

The project is organized as follows:

- `app/`: directory containing the application files.
- `Dockerfile`: file defining the Docker image for the application.
- `docker-compose.yml`: file defining the Docker service for the project.
- `README.md`: file containing project instructions and documentation.

## Contributing

1. Fork the project.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Adding new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## Code Standardization

This project follows the guidelines of [PEP 8](https://www.python.org/dev/peps/pep-0008/) and uses the [Black](https://github.com/psf/black) tool to maintain consistent code formatting. In addition, it is recommended to use the [PyLint](https://www.pylint.org/) tool for static code analysis.

## License

This project is licensed under the MIT license. Please see the LICENSE file for more information.
