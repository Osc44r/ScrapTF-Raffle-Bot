# ScrapTF-Raffle-Bot

ScrapTF-Raffle-Bot is a small open-source Python bot that automatically joins raffles on scrap.tf, a popular TF2 trading website.

## .env Configuration

The `.env` file in this project contains two variables:

- `COOKIE`: This should be set to your scrap.tf `scr_session` cookie, which is used for authentication.
- `PROXY`: This should be set to the proxy you want to use. Leave it empty if no proxy is needed.

## config.ini Configuration

The `config.ini` file contains the following variables with default values:

```ini
[TIMEOUTS]
# Ranges in seconds. Example (100, 500) means from 100 to 500 seconds
captcha = (10800, 11800)
next_raffle = (3, 8)
next_refresh = (21600, 32400)
```

In the above configuration, each variable represents a timeout range in seconds. The bot will randomly select a timeout value within these ranges for various operations, such as refreshing captchas, joining the next raffle, and refreshing all raffles.

## Disclaimer

The creator of this bot is not responsible for any bans or penalties imposed by scrap.tf as a result of using this bot. Use it at your own risk.

## Contributing

Feel free to contribute to this project by submitting bug reports, feature requests, or pull requests. Your contributions are greatly appreciated!

