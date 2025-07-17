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
└── venv/                  # Python virtual environment
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
- Python 3.8+
- 8GB+ RAM for local model inference
- Ollama installed and running

### Installation
```bash
# Clone and setup
git clone <repo-url>
cd yes-and
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Start Ollama
ollama serve

# Pull base model
ollama pull llama3.2:3b

# Run chatbot
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
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black src/
isort src/
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
- **Python 3.8+**: Required for type hints and async features
- **Ollama**: Local LLM inference engine
- **CUDA** (optional): For GPU acceleration during training

### Python Packages
See `requirements.txt` for full list. Key dependencies:
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

## Support

For issues or questions:
- Create GitHub issue
- Check existing discussions
- Review documentation in `/docs`
- Check logs in `logs/` directory for debugging

---

*"I told my computer a joke about infinity. It's still laughing..." - Your AI Cohost* 🤖
