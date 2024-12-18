[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/hhhscvx)


## Functionality
| Functional                                                            | Supported |
|-----------------------------------------------------------------------|:---------:|
| Multithreading                                                        |     ✅     |
| Binding a proxy to a session                                          |     ✅     |
| Auto complting tasks                                                  |     ✅     |
| Random number of clicks per request                                   |     ✅     |
| Support tdata / pyrogram .session / telethon .session                 |     ✅     |

## [Change Settings](https://github.com/hhhscvx/PlanesCryptoBot/blob/master/bot/config/config.py)
| Настройка                | Описание                                                                               |
|--------------------------|----------------------------------------------------------------------------------------|
| **API_ID / API_HASH**    | Platform data from which to launch a Telegram session (stock - Android)                |

## Installation
You can download [**Repository**](https://github.com/hhhscvx/PlanesCryptoBot) by cloning it to your system and installing the necessary dependencies:
```shell
~ >>> git clone https://github.com/hhhscvx/PlanesCryptoBot.git
~ >>> cd PlanesCryptoBot

#Linux
~/PlanesCryptoBot >>> python3 -m venv venv
~/PlanesCryptoBot >>> source venv/bin/activate
~/PlanesCryptoBot >>> pip3 install -r requirements.txt
~/PlanesCryptoBot >>> cp .env-example .env
~/PlanesCryptoBot >>> nano .env # Here you must specify your API_ID and API_HASH , the rest is taken by default
~/PlanesCryptoBot >>> python3 main.py

#Windows
~/PlanesCryptoBot >>> python -m venv venv
~/PlanesCryptoBot >>> venv\Scripts\activate
~/PlanesCryptoBot >>> pip install -r requirements.txt
~/PlanesCryptoBot >>> copy .env-example .env
~/PlanesCryptoBot >>> # Specify your API_ID and API_HASH, the rest is taken by default
~/PlanesCryptoBot >>> python main.py
```
