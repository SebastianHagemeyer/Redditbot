
# Reddit Video Compilation and YouTube Upload Bot

This bot scrapes content from Reddit, compiles posts and comments into a video, and uploads the result to YouTube.

## Features

- Scrapes posts, images, and comments from Reddit.
- Compiles the scraped content into a video with intro/outro.
- Automatically uploads the video to YouTube with custom titles, descriptions, and tags.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/reddit-youtube-upload-bot.git
   cd reddit-youtube-upload-bot
   ```

2. **Run the setup**:

   - All prerequisites are installed via the `setup.bat` file. Simply run:

   ```bash
   setup.bat
   ```

3. **Run the bot**:

   ```bash
   python main.py
   ```

## Configuration

- **Subreddits**: Modify the subreddits list in `main.py` to target specific subreddits.
- **YouTube Upload**: Titles, descriptions, and tags are automatically generated but can be customized in the script.

## License

This project is licensed under the MIT License.
