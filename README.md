# Asgard World Generator

Asgard World Generator is a FastAPI-based web application that generates procedural worlds and features a real-time chat system. It uses Redis for visit counting and WebSockets for chat functionality.

## Features

- Procedural world generation using wave function collapse algorithm
- Real-time chat system
- Visit counter
- FastAPI backend with Jinja2 templating
- Redis integration for data persistence

## Prerequisites

- Python 3.7+
- Redis server

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/asgard-world-generator.git
   cd asgard-world-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure Redis is running on localhost:6379 (default port)

5. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

6. Open your web browser and navigate to `http://localhost:8000`

## Project Structure

- `app/main.py`: Main FastAPI application file
- `app/world_generator.py`: World generation logic
- `app/templates/`: Jinja2 HTML templates
- `app/static/`: Static files (CSS, JS)
- `requirements.txt`: List of Python dependencies

## Contributing

We welcome contributions to the Asgard World Generator project! If you're interested in contributing, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear, descriptive commit messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please make sure to follow our [code of conduct](CODE_OF_CONDUCT.md) and read our [contributing guidelines](CONTRIBUTING.md) before submitting your pull request.

## License

This project is open source and available under the [Apache License 2.0](LICENSE).

## Contact

If you have any questions or suggestions, please open an issue on the GitHub repository or contact the project maintainers.

Thank you for your interest in the Asgard World Generator project!