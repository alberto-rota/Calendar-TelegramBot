# Calendar-TelegramBot
A Telegram Bot managing your events in Google Calendar: this Bot allows to view, edit, create and delete events in a simple interface from the Telegram chat. It also supports Tasks, that can be added, edited and modified from a similar interface and that will be notified to the user until selected as completed.
Moreover, it provides notifications for your events as specified in your Google calendar.

## Requirements
This bot is intended to be used by **only one user**: it therefore requires a host platform to run (the author is hosting his personal bot on a RaspberryPI) and the API keys for a Telegram Bot and the _Google Calendar API_. [Here](https://developers.google.com/calendar/api) is the guide for obtaining the API keys from Google and to activate your app by making it public, and [here](https://core.telegram.org/bots#6-botfather) is how to create a new Telegram bot and how to obtain its API token,

The bot cannot therefore handle too many requests at a time withoud noticeble delays, and it is as a matter of facts thought to be used from a single user or, at max, from a small group of people, always minding that multiple contemporary requests may easily result in unwanted/unexpected outputs.

## License
[GNU GPL3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Copyright
©2022, Alberto Rota

mailto:alberto_rota@outlook.com
