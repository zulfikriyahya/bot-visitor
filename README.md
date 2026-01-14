```bash

@reboot sleep 60 && cd /home/zulfikriyahya/bot-visitor && ./setup.sh > bot.log 2>&1

0 */6 * * * pkill -f main.py; pkill -f setup.sh; cd /home/zulfikriyahya/bot-visitor && ./setup.sh > bot.log 2>&1
```
