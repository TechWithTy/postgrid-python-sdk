# PostGrid SDK

An async Python client for the [PostGrid Print & Mail API](https://docs.postgrid.com/), integrated into the Lead Ignite backend. Built with `aiohttp` and `pydantic` for high-performance, type-safe API interactions.

[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PostGrid API](https://img.shields.io/badge/PostGrid-API-00A3E0)](https://docs.postgrid.com/)

## ✨ Features

- 🚀 **Async-First**: Built with `asyncio` for non-blocking API interactions
- 🧠 **Type Safety**: Full Python type hints with Pydantic models
- 🛡️ **Robust Error Handling**: Comprehensive error hierarchy and validation
- ⏱ **Rate Limiting**: Built-in rate limiting with configurable thresholds
- 🔄 **Automatic Retries**: Configurable retry logic with exponential backoff
- 🔒 **Secure**: Environment-based configuration and secrets management
- 📦 **Modular Design**: Clean separation of concerns with dedicated API modules
- ✅ **Test Coverage**: Comprehensive test suite with pytest

## 📦 Installation

This package is part of the Lead Ignite backend and is automatically installed as a dependency.

For development:

```bash
# Install with poetry
poetry add --group dev -e ./app/core/third_party_integrations/postgrid
```

## ⚙️ Configuration

Configuration is managed through environment variables. Create a `.env` file in your project root:

```env
# Required
POSTGRID_API_KEY=your_live_or_test_api_key

# Optional (with defaults shown)
POSTGRID_BASE_URL=https://api.postgrid.com/print-mail/v1/
POSTGRID_TIMEOUT=30
POSTGRID_MAX_RETRIES=3
POSTGRID_RATE_LIMIT=50  # Requests per minute
```

## 🚀 Quick Start

### Initialization

```python
import asyncio
from app.core.third_party_integrations.postgrid.client import PostGridClient

async def main():
    # Initialize with default config (loads from environment)
    async with PostGridClient() as client:
        try:
            # Your code here
            pass
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example: Sending a Postcard

```python
async def send_postcard():
    async with PostGridClient() as client:
        try:
            postcard = await client.post(
                "/postcards",
                json={
                    "to": {
                        "firstName": "John",
                        "lastName": "Doe",
                        "addressLine1": "123 Main St",
                        "city": "Toronto",
                        "provinceOrState": "ON",
                        "postalOrZip": "M1M1M1",
                        "country": "CA"
                    },
                    "from": {
                        "company": "Your Company",
                        "addressLine1": "456 Business Ave",
                        "city": "New York",
                        "provinceOrState": "NY",
                        "postalOrZip": "10001",
                        "country": "US"
                    },
                    "front": "<html>Front HTML</html>",
                    "back": "<html>Back HTML</html>"
                }
            )
            return postcard
        except Exception as e:
            logger.error(f"Failed to send postcard: {e}")
            raise
```

## 📚 API Reference

### Client Methods

#### `PostGridClient`

Main client class for interacting with the PostGrid API.

**Methods:**

- `get(endpoint: str, response_model: Type[T] = None, **kwargs) -> Any`
  - Make a GET request to the specified endpoint
  - Returns: Parsed response data

- `post(endpoint: str, response_model: Type[T] = None, **kwargs) -> Any`
  - Make a POST request to the specified endpoint
  - Returns: Parsed response data

- `put(endpoint: str, response_model: Type[T] = None, **kwargs) -> Any`
  - Make a PUT request to the specified endpoint
  - Returns: Parsed response data

- `delete(endpoint: str, **kwargs) -> Any`
  - Make a DELETE request to the specified endpoint
  - Returns: Parsed response data

### Available Endpoints

The client supports all PostGrid API endpoints, organized into logical modules:

- `letters/` - Create and manage physical letters
- `postcards/` - Design and send postcards
- `contacts/` - Manage contact information
- `templates/` - Store and manage reusable templates
- `webhooks/` - Configure and manage webhook events
- `trackers/` - Track mail pieces and events
- `events/` - Retrieve system and mail events

## 🔄 Error Handling

The client raises specific exceptions for different error scenarios:

- `PostGridAuthenticationError`: Invalid or missing API key (401)
- `PostGridValidationError`: Invalid request data (400)
- `PostGridRateLimitError`: Rate limit exceeded (429)
- `PostGridAPIError`: Other API errors (500+)

## 🧪 Testing

Run the test suite with pytest:

```bash
pytest app/core/third_party_integrations/postgrid/tests/
```

### Test Configuration

Tests use a mock server by default. To run against the live API:

```bash
POSTGRID_API_KEY=your_test_key POSTGRID_ENV=test pytest -v
```

## 🛠 Development

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function signatures
- Document all public methods with Google-style docstrings
- Keep functions small and focused

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Resources

- [PostGrid API Documentation](https://docs.postgrid.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [aiohttp Documentation](https://docs.aiohttp.org/)

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For support, please open an issue in the repository or contact the maintainers.

---

<div align="center">
  <p>Built with ❤️ by the Lead Ignite Team</p>
  <p>Part of the Lead Ignite Marketing Automation Platform</p>
</div>

### `PostGridClient`

The main client class for interacting with the PostGrid API.

#### Initialization

```python
from postgrid_sdk import PostGridClient

# With default config (loads from environment)
client = PostGridClient()

# Or with custom config
from postgrid_sdk.config import PostGridConfig

config = PostGridConfig(
    api_key="your_api_key_here",
    base_url="https://api.postgrid.com/print-mail/v1/",
    timeout=30,
    max_retries=3,
    rate_limit=50
)
client = PostGridClient(config=config)
```

#### Methods

- `get(endpoint: str, **kwargs)`: Make a GET request
- `post(endpoint: str, **kwargs)`: Make a POST request
- `put(endpoint: str, **kwargs)`: Make a PUT request
- `delete(endpoint: str, **kwargs)`: Make a DELETE request
- `close()`: Close the client session (automatically handled by context manager)

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=postgrid_sdk --cov-report=term-missing

# Run with specific test
pytest tests/test_client.py -v
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

TechWithTy - [@techwithty](https://github.com/techwithty)

Project Link: [https://github.com/techwithty/postgrid-python-sdk](https://github.com/techwithty/postgrid-python-sdk)

## 🔗 Related Projects

- [PostGrid API Documentation](https://docs.postgrid.com/)
- [aiohttp](https://docs.aiohttp.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
