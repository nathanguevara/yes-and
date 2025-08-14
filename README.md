# Humorous AI Cohost 🎭

A witty AI comedy partner built for real-time banter, jokes, and improvised humor. This project creates a custom-tuned language model that can serve as a comedic cohost for conversations, streams, or interactive applications.

## Project Overview

**Goal**: Build an AI that can deliver witty, contextual humor in real-time conversations.

**Current Status**: MVP - Basic chatbot with prompt-engineered humor layers

**Next Phase**: Fine-tuning on comedy dialogue datasets

## Architecture

```
yes-and/
├── src/
│   ├── chatbot/           # Main chatbot application
│   ├── training/          # Model fine-tuning pipeline
│   ├── data/              # Comedy datasets and preprocessing
│   └── utils/             # Shared utilities
├── models/                # Trained model checkpoints
├── data/                  # Training data (comedic dialogues)
├── experiments/           # Training experiments and logs
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── logs/                  # Application and training logs
├── .venv/                 # Python virtual environment (created by uv)
└── pyproject.toml         # Project configuration and dependencies
```

## Current Features

- **Streamlit Chat Interface**: Interactive web-based chatbot
- **Multiple Humor Styles**: Witty, sarcastic, observational, self-deprecating, absurd
- **Real-time Response**: Uses Ollama for local inference
- **Feedback System**: User ratings to improve humor quality
- **Conversation Memory**: Maintains context across exchanges
- **Rule-based Enhancements**: Adds comedic timing and wordplay

## Quick Start

### Prerequisites
- Python 3.11+
- 8GB+ RAM for local model inference
- Ollama installed and running
- uv package manager (https://github.com/astral-sh/uv)

### Installation
```bash
# Clone and setup
git clone <repo-url>
cd yes-and

# Install dependencies with uv
uv sync

# Start Ollama
ollama serve

# Pull base model
ollama pull llama3.2:3b

# Run chatbot
uv run streamlit run src/chatbot/humor_cohost.py

# Or activate the environment first
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
streamlit run src/chatbot/humor_cohost.py
```

### Usage
1. Open browser to `http://localhost:8501`
2. Select humor style from sidebar
3. Start chatting with your AI comedy partner!

## Development Roadmap

### Phase 1: MVP (Current)
- [x] Basic chatbot with Ollama integration
- [x] Humor style selection
- [x] Feedback collection system
- [x] Rule-based humor enhancements

### Phase 2: Data Collection
- [x] Scrape comedy dialogue datasets (reddit_scraper.py, script_parser.py)
- [ ] Clean and format training data
- [x] Implement conversation logging
- [x] Build feedback analysis tools

### Phase 3: Fine-tuning
- [x] Set up training pipeline with LoRA (fine_tune.py)
- [ ] Fine-tune on comedy datasets
- [x] Implement model evaluation metrics (evaluate.py, humor_metrics.py)
- [ ] A/B testing framework

### Phase 4: Advanced Features
- [ ] Voice integration for verbal comedy
- [ ] Persona switching (different comedy styles)
- [ ] Context-aware humor (knows about user)
- [ ] Multi-turn joke setups

## Model Details

**Base Model**: Llama 3.2 3B Instruct
- Chosen for: Instruction following, efficiency, humor understanding
- Alternatives: Gemma 2 2B, Phi-3 Mini, Qwen2.5 7B

**Fine-tuning Approach**: LoRA (Low-Rank Adaptation)
- Memory efficient for local training
- Preserves base model capabilities
- Allows quick experimentation

## Data Sources

### Target Datasets
- Reddit: r/jokes, r/clevercomebacks, r/roastme
- TV/Movie Scripts: Friends, The Office, Brooklyn 99
- Stand-up Comedy: Public domain transcripts
- Improv: Comedy dialogue patterns
- Twitter: Witty exchanges and one-liners

### Data Format
```json
{
  "conversations": [
    {
      "setup": "User input or conversation context",
      "punchline": "Witty AI response",
      "style": "witty|sarcastic|observational|absurd",
      "rating": 1-5,
      "context": "Previous conversation turns"
    }
  ]
}
```

## File Structure

```
src/
├── chatbot/
│   ├── humor_cohost.py        # Main Streamlit app
│   ├── cohost_engine.py       # Core humor generation
│   └── humor_layers.py        # Rule-based enhancements
├── training/
│   ├── data_prep.py           # Dataset preprocessing
│   ├── fine_tune.py           # Model training script
│   └── evaluate.py            # Model evaluation
├── data/
│   ├── collectors/            # Data scraping scripts
│   ├── raw/                   # Raw comedy datasets
│   └── processed/             # Cleaned training data
└── utils/
    ├── humor_metrics.py       # Scoring and analysis
    ├── feedback.py            # User feedback handling
    └── prompts.py             # Humor prompt templates
```

## Contributing

### Setup Development Environment
```bash
# Install all dependencies including dev tools
uv sync

# Activate environment
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Run tests
uv run pytest tests/

# Code formatting
uv run black src/
uv run ruff check src/
uv run mypy src/
```

### Adding New Humor Styles
1. Add style definition to `humor_styles` dict
2. Create corresponding prompt template
3. Add style-specific rule enhancements
4. Update UI selector options

### Data Collection Guidelines
- Respect copyright and fair use
- Anonymize personal information
- Focus on dialogue patterns, not specific jokes
- Maintain diverse humor styles in dataset

## Configuration

### Environment Variables
```bash
OLLAMA_HOST=localhost:11434
MODEL_NAME=llama3.2:3b
HUMOR_STYLE=witty
LOG_LEVEL=INFO
FEEDBACK_DB=data/feedback.json
```

### Model Parameters
```python
# Training config
BATCH_SIZE = 4
LEARNING_RATE = 2e-5
EPOCHS = 3
LORA_RANK = 16
LORA_ALPHA = 32

# Inference config
TEMPERATURE = 0.9
TOP_P = 0.9
MAX_TOKENS = 100
```

## Evaluation Metrics

### Humor Quality
- User ratings (1-5 scale)
- Response time
- Conversation engagement length
- Repeat user rate

### Technical Metrics
- Model perplexity
- Response coherence
- Context retention
- Inference speed

## Dependencies

### Core Requirements
- **Python 3.11+**: Required for modern type hints and async features
- **Ollama**: Local LLM inference engine
- **CUDA** (optional): For GPU acceleration during training
- **uv**: Fast Python package manager

### Python Packages
See `pyproject.toml` for full list. Key dependencies:
- `streamlit`: Web UI framework
- `ollama`: Python client for Ollama
- `torch`, `transformers`, `peft`: ML/training stack
- `loguru`: Advanced logging
- `pydantic`: Data validation

## Known Issues

- Ollama connection timeout on slow systems
- Humor quality varies by topic
- Limited conversation memory (5 exchanges)
- No persistent user profiles

## Future Enhancements

### Technical
- GPU acceleration for faster inference
- Distributed training for larger datasets
- Real-time model updating based on feedback
- API endpoint for external integrations

### Features
- Voice-to-voice comedy interaction
- Personalized humor based on user history
- Multi-language comedy support
- Comedy timing visualization

## License

MIT License - See LICENSE file for details

## Testing

Run the test suite:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_basic.py
```

## Logs and Debugging

Application logs are stored in `logs/` directory:
- `humor_cohost.log`: Main application logs
- Training logs: Created during fine-tuning sessions

Enable debug logging:
```bash
LOG_LEVEL=DEBUG streamlit run src/chatbot/humor_cohost.py
```

## API Specification

### Base URL
- Development: `http://localhost:8000`
- Docker: `http://localhost:8000`

### Authentication
Currently, the API does not require authentication. This may change in future versions.

### Endpoints

#### 1. Root Endpoint
**GET /**

Returns basic API information.

**Response:**
```json
{
  "name": "Yes-And Comedy API",
  "version": "0.1.0",
  "description": "AI Comedy Cohost API"
}
```

#### 2. Health Check
**GET /health**

Check if the API and Ollama connection are working.

**Response:**
```json
{
  "status": "healthy",
  "ollama_available": true,
  "model": "llama3.2:3b",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 3. Generate Humor Response
**POST /generate**

Generate a humorous response based on user input and selected humor style.

**Request Body Examples:**

Example 1 - Simple request (no conversation history):
```json
{
  "user_input": "hit me with your best shot"
}
```

Example 2 - Specify humor style:
```json
{
  "user_input": "What's the deal with airplane food?",
  "humor_style": "observational"
}
```

Example 3 - Include session tracking:
```json
{
  "user_input": "Tell me about your day",
  "humor_style": "self_deprecating",
  "session_id": "user-session-123"
}
```

Example 4 - Single exchange history:
```json
{
  "user_input": "That's hilarious! Tell me more",
  "humor_style": "witty",
  "conversation_history": [
    {
      "role": "user",
      "content": "What do you think about coffee?"
    },
    {
      "role": "assistant",
      "content": "Coffee is just adult peer pressure in liquid form"
    }
  ],
  "session_id": "coffee-chat-456"
}
```

Example 5 - Full conversation context:
```json
{
  "user_input": "Okay but what about tea then?",
  "humor_style": "sarcastic",
  "conversation_history": [
    {
      "role": "user",
      "content": "What do you think about coffee?"
    },
    {
      "role": "assistant",
      "content": "Coffee is just adult peer pressure in liquid form"
    },
    {
      "role": "user", 
      "content": "That's hilarious! Tell me more"
    },
    {
      "role": "assistant",
      "content": "Well, it's the only socially acceptable addiction where withdrawal symptoms are considered a personality trait"
    }
  ],
  "session_id": "coffee-chat-456"
}
```

**Parameters:**
- `user_input` (string, required): User's input message
- `humor_style` (string, optional): One of: "witty", "sarcastic", "observational", "self_deprecating", "absurd". Default: "witty"
- `conversation_history` (array, optional): Previous conversation turns for context
- `session_id` (string, optional): Session identifier for tracking conversations

**Response:**
```json
{
  "response": "My day? Picture a sitcom where the main character keeps walking into glass doors. That's been me, but with less laugh track and more actual bruises.",
  "humor_style": "self_deprecating",
  "processing_time": 1.23,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Response:**
```json
{
  "detail": "Error generating response: Ollama service unavailable"
}
```

#### 4. Submit Feedback
**POST /feedback**

Submit user rating for a generated response.

**Request Body:**
```json
{
  "message": "Tell me about your day",
  "response": "My day? Picture a sitcom where...",
  "rating": 4,
  "humor_style": "self_deprecating",
  "session_id": "optional-session-identifier"
}
```

**Parameters:**
- `message` (string, required): Original user message
- `response` (string, required): AI's response
- `rating` (integer, required): Rating from 1-5
- `humor_style` (string, required): Style used for generation
- `session_id` (string, optional): Session identifier for tracking

**Response:**
```json
{
  "status": "success",
  "feedback_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 5. Get Feedback Statistics
**GET /feedback/stats**

Retrieve aggregated feedback statistics.

**Query Parameters:**
- `humor_style` (string, optional): Filter by specific humor style
- `days` (integer, optional): Number of days to include (default: 7)

**Response:**
```json
{
  "total_ratings": 150,
  "average_rating": 3.8,
  "rating_distribution": {
    "1": 10,
    "2": 15,
    "3": 40,
    "4": 55,
    "5": 30
  },
  "by_humor_style": {
    "witty": {
      "count": 45,
      "average": 4.1
    },
    "sarcastic": {
      "count": 35,
      "average": 3.5
    }
  },
  "period": "7_days"
}
```

#### 6. Get Model Information
**GET /model/info**

Get information about the current model and configuration.

**Response:**
```json
{
  "model_name": "llama3.2:3b",
  "ollama_version": "0.1.17",
  "available_humor_styles": [
    "witty",
    "sarcastic", 
    "observational",
    "self_deprecating",
    "absurd"
  ],
  "generation_params": {
    "temperature": 0.9,
    "top_p": 0.9,
    "max_tokens": 100
  }
}
```

### Error Handling

All endpoints follow consistent error response format:

```json
{
  "detail": "Error message describing what went wrong",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Common Error Codes:**
- `OLLAMA_UNAVAILABLE`: Ollama service is not accessible
- `MODEL_NOT_FOUND`: Requested model is not available
- `INVALID_HUMOR_STYLE`: Provided humor style is not supported
- `RATE_LIMIT_EXCEEDED`: Too many requests (future implementation)

### Rate Limiting
Currently not implemented but planned for future versions:
- 60 requests per minute per IP
- 1000 requests per hour per IP

### WebSocket Support (Future)
Planned endpoint for real-time streaming responses:
- `WS /ws/chat` - WebSocket connection for streaming humor generation

### Python Client Example

```python
import requests

# Initialize client
base_url = "http://localhost:8000"

# Check health
health = requests.get(f"{base_url}/health").json()
print(f"API Status: {health['status']}")

# Generate humor response
response = requests.post(
    f"{base_url}/generate",
    json={
        "message": "What's the deal with airplane food?",
        "humor_style": "observational"
    }
).json()
print(f"AI Response: {response['response']}")

# Submit feedback
feedback = requests.post(
    f"{base_url}/feedback",
    json={
        "message": "What's the deal with airplane food?",
        "response": response['response'],
        "rating": 4,
        "humor_style": "observational"
    }
).json()
print(f"Feedback submitted: {feedback['feedback_id']}")
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Generate response
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a joke", "humor_style": "witty"}'

# Get feedback stats
curl http://localhost:8000/feedback/stats?humor_style=witty
```

### API Client Library

A Python client library is provided in `src/frontend/api_client.py`:

```python
from src.frontend.api_client import HumorAPIClient

client = HumorAPIClient(base_url="http://localhost:8000")

# Generate response
response = client.generate_response(
    message="Hello!",
    humor_style="sarcastic"
)

# Submit feedback  
client.submit_feedback(
    message="Hello!",
    response=response,
    rating=5,
    humor_style="sarcastic"
)
```

## Support

For issues or questions:
- Create GitHub issue
- Check existing discussions
- Review documentation in `/docs`
- Check logs in `logs/` directory for debugging

---

*"I told my computer a joke about infinity. It's still laughing..." - Your AI Cohost* 🤖
