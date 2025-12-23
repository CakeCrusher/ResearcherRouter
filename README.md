# ResearcherRouter

A Discord bot that helps researchers find people who discussed specific topics by automatically indexing research papers and discussions using Qdrant vector database.

## 🏗️ Project Structure

```
ResearcherRouter/
├── main.py                 # Main entry point
├── test_paper.py           # Test script for paper-related features
├── .env                    # Environment variables (create this)
├── pyproject.toml          # Poetry dependencies
├── poetry.lock             # Locked dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── config/                 # Configuration files
│   ├── Dockerfile          # Docker configuration
│   ├── docker-compose.yml  # Qdrant service
│   ├── .dockerignore       # Docker ignore rules
│   └── qdrant_storage/     # Qdrant local data storage
├── icon/                   # Bot icons, branding assets
└── src/                    # Source code
    ├── bot/                # Discord bot code
    │   ├── main.py         # Bot entry point
    │   ├── cogs/           # Bot commands and events
    │   │   ├── Commands.py     # Search commands
    │   │   └── Events.py       # Event handlers
    │   ├── logic/          # Business logic
    │   │   ├── __init__.py
    │   │   ├── add_log_tag.py       # Add tags to logs
    │   │   ├── add_thread.py        # Add thread info to Qdrant
    │   │   ├── initialize.py        # Initialize bot/session state
    │   │   ├── on_message_update.py # Handle message edits/updates
    │   │   └── thread_summary.py    # Handle thread summary logic
    │   └── pydantic_configure/      # Pydantic settings and models
    │       ├── __init__.py
    │       └── pydantic_conf.py     # Pydantic BaseSettings & config loading
    ├── qdrant/             # Qdrant database code
    │   └── qdrant.py       # Qdrant operations

```

## 🚀 Quick Start

### 1. Set up environment
```bash
# Install dependencies
poetry install

# Create .env file with your Discord bot credentials
cp .env.example .env
# Edit .env with your actual values
```

### 2. Start Qdrant
```bash
# Using Docker Compose
sudo docker-compose -f config/docker-compose.yml up -d

# Or using Docker directly
sudo docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Run the bot
```bash
poetry run python main.py
```

## 🔧 Configuration

Create a `.env` file with:
```bash
# Discord
DISCORD_TOKEN=your_discord_bot_token_here
PAPER_CHANNEL_ID=your_paper_channel_id_here
SUMMARIZED_TAG=your_summarized_tag_id_here
LOGGED_TAG=your_logged_tag_id_here

# Qdrant
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
COLLECTION_NAME=test
```

## 🤖 Bot Commands

- `@bot <topic>` - Search for people who discussed a topic
- `!search <topic>` - Same as above
- `!ping` - Test if bot is working

## 📊 Features

- **Automatic indexing** of Discord threads as research papers
- **Semantic search** using sentence transformers
- **Participant tracking** - finds all people who discussed topics
- **Summary detection** - automatically identifies summarized papers
- **Real-time updates** - indexes new messages and threads

## 🐳 Docker Deployment

```bash
# Clone repository and configure your .env file
git clone https://github.com/CakeCrusher/ResearcherRouter
cd ResearcherRouter
nano .env

# Start Docker
cd config
docker compose up -d
```
Other commands (execute in `config/`):
```bash
# To check that it's running
docker compose ps

# To view logs
docker compose logs -f

# To stop the container
docker compose down
```
To update the existing container, rebuild the image and recreate the container automatically:
```bash
docker compose down
docker compose build
docker compose up -d
```

