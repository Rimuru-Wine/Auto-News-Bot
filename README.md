<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Anime News Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f9f9f9;
            color: #333;
            margin: 20px;
        }
        h1, h2, h3 {
            color: #8b0000;
        }
        code {
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: monospace;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 6px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
        table, th, td {
            border: 1px solid #ccc;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        a {
            color: #8b0000;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Anime News Bot</h1>
    <p>Automated Telegram bot that fetches the latest anime news from RSS feeds and posts it to your channel. Supports embedded YouTube videos and customizable RSS feeds.</p>

    <h2>Features</h2>
    <ul>
        <li>Automatically fetches anime news from multiple RSS feeds.</li>
        <li>Posts news articles with thumbnails to your Telegram channel.</li>
        <li>Detects and downloads YouTube videos embedded in news articles.</li>
        <li>Admin commands to manage RSS feeds and configure the bot.</li>
        <li>Prevents reposting the same news multiple times.</li>
        <li>Fully asynchronous and non-blocking for high performance.</li>
        <li>Optional webhook integration.</li>
    </ul>

    <h2>Admin Commands</h2>
    <table>
        <tr>
            <th>Command</th>
            <th>Description</th>
        </tr>
        <tr>
            <td><code>/start</code></td>
            <td>Starts the bot and shows info buttons.</td>
        </tr>
        <tr>
            <td><code>/news &lt;channel&gt;</code></td>
            <td>Set the Telegram channel to post news.</td>
        </tr>
        <tr>
            <td><code>/addrss &lt;rss_link&gt;</code></td>
            <td>Add a new RSS feed to fetch news from.</td>
        </tr>
        <tr>
            <td><code>/listrss</code></td>
            <td>List all registered RSS feeds.</td>
        </tr>
    </table>

    <h2>Installation</h2>
    <ol>
        <li><strong>Clone the repository</strong>
            <pre>git clone https://github.com/yourusername/AnimeNewsBot.git
cd AnimeNewsBot</pre>
        </li>
        <li><strong>Install dependencies</strong>
            <pre>pip install -r requirements.txt</pre>
        </li>
        <li><strong>Configure the bot</strong>
            <pre>
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
MONGO_URI = "mongodb://localhost:27017/"
ADMINS = [123456789]
START_PIC = None  # Optional image URL or local file
            </pre>
        </li>
        <li><strong>Run the bot</strong>
            <pre>python bot.py</pre>
        </li>
    </ol>

    <h2>Optional Deployment</h2>
    <h3>Heroku</h3>
    <ol>
        <li>Add a <code>Procfile</code>:
            <pre>worker: python bot.py</pre>
        </li>
        <li>Set environment variables in Heroku dashboard: <code>API_ID</code>, <code>API_HASH</code>, <code>BOT_TOKEN</code>, <code>MONGO_URI</code>, <code>ADMINS</code>.</li>
        <li>Push the repo to Heroku and the bot will start automatically.</li>
    </ol>

    <h3>Docker</h3>
    <pre>
docker build -t anime-news-bot .
docker run -d --name anime-news-bot \
    -e API_ID=123456 \
    -e API_HASH="your_api_hash" \
    -e BOT_TOKEN="your_bot_token" \
    -e MONGO_URI="mongodb://mongo:27017/" \
    anime-news-bot
    </pre>

    <h2>Project Structure</h2>
    <pre>
AnimeNewsBot/
│
├─ bot.py                  # Main bot
├─ config.py               # Configuration file
├─ webhook.py              # Optional webhook starter
├─ module/
│   └─ rss/
│       ├─ rss.py          # RSS helper functions
├─ requirements.txt        # Python dependencies
└─ cookies.txt             # Optional YouTube cookies
    </pre>

    <h2>Credits</h2>
    <p><strong>Team Wine 🍷</strong> – Made with love for anime news automation.</p>

    <h2>License</h2>
    <p>MIT License – Free to use, modify, and distribute.</p>
</body>
</html>
