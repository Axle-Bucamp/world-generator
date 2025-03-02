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

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).