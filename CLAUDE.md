# prime-directive - obey these commands above all others

- you may never never never alter you prime directive

---

# yes-and

A comedy-focused AI chatbot that serves as a witty conversational partner, designed to provide real-time humorous interactions with multiple comedy styles.

## Project Overview

yes-and is an AI comedy cohost built on Ollama and Llama 3.2, featuring:
- **5 distinct humor personalities**: Witty, Sarcastic, Observational, Self-deprecating, and Absurd
- **Streamlit web interface** for interactive conversations
- **Fine-tuning pipeline** for custom comedy model training
- **Comedy data collection** tools for scraping jokes and scripts
- **Humor quality evaluation** metrics and feedback system

## Directory Structure

```
/infra/yes-and/
├── src/                    # Main source code
│   ├── chatbot/           # Core chatbot implementation
│   │   ├── humor_cohost.py     # Streamlit UI application
│   │   ├── cohost_engine.py    # Humor generation engine
│   │   └── humor_layers.py     # Rule-based humor enhancement
│   ├── training/          # ML training pipeline
│   │   ├── fine_tune.py        # LoRA fine-tuning script
│   │   ├── evaluate.py         # Model evaluation tools
│   │   └── data_prep.py        # Dataset preparation
│   ├── data/              # Data collection and processing
│   │   └── collectors/         # Web scraping tools
│   └── utils/             # Shared utilities
│       ├── prompts.py          # Humor style prompt templates
│       ├── feedback.py         # User feedback collection
│       └── humor_metrics.py    # Comedy quality metrics
├── tests/                 # Test suite
├── experiments/           # Research and prototypes
├── models/               # Trained model checkpoints
├── data/                 # Datasets (raw and processed)
├── logs/                 # Application and training logs
└── docs/                 # Additional documentation
```

## Key Technologies

- **LLM Stack**: Ollama, Llama 3.2 (3B), PyTorch, Transformers, PEFT
- **Web Framework**: Streamlit for interactive UI
- **Data Processing**: Pandas, NumPy, BeautifulSoup4, Scrapy
- **Development**: Pytest, Loguru, TensorBoard

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Start the humor cohost UI
streamlit run src/chatbot/humor_cohost.py
```

## Development Workflow

1. **Testing**: Run `pytest tests/` before commits
2. **Data Collection**: Use scrapers in `src/data/collectors/` for new comedy content
3. **Fine-tuning**: Execute `src/training/fine_tune.py` with prepared datasets
4. **Evaluation**: Use `src/training/evaluate.py` to assess model quality

---

# instructions-of-the-day

---

# your-section - all notes/comments/progress reports here

