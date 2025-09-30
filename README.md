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
<ul>
    <li><b>/start</b> – Starts the bot and shows info buttons.</li>
    <li><b>/news &lt;channel&gt;</b> – Set the Telegram channel to post news.</li>
    <li><b>/addrss &lt;rss_link&gt;</b> – Add a new RSS feed to fetch news from.</li>
    <li><b>/listrss</b> – List all registered RSS feeds.</li>
</ul>

<h2>Installation</h2>
<ol>
    <li>Clone the repository:
        <pre>git clone https://github.com/yourusername/AnimeNewsBot.git
cd AnimeNewsBot</pre>
    </li>
    <li>Install dependencies:
        <pre>pip install -r requirements.txt</pre>
    </li>
    <li>Configure the bot in <b>config.py</b>:
        <pre>
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
MONGO_URI = "mongodb://localhost:27017/"
ADMINS = [123456789]
START_PIC = None  # Optional image URL or local file
        </pre>
    </li>
    <li>Run the bot:
        <pre>python bot.py</pre>
    </li>
</ol>

<h2>Optional Deployment</h2>

<h3>Heroku</h3>
<ol>
    <li>Add a <b>Procfile</b>:
        <pre>worker: python bot.py</pre>
    </li>
    <li>Set environment variables in Heroku dashboard: <b>API_ID, API_HASH, BOT_TOKEN, MONGO_URI, ADMINS</b>.</li>
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
<p><b>Team Wine 🍷</b> – Made with love for anime news automation.</p>

<h2>License</h2>
<p>MIT License – Free to use, modify, and distribute.</p>
