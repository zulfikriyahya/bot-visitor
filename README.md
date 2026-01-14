```bash

# 1. Jalan otomatis saat server nyala (reboot)
@reboot sleep 60 && cd /home/zulfikriyahya/bot-visitor && ./setup.sh > bot.log 2>&1

# 2. Restart paksa setiap 6 jam (untuk refresh RAM & Proxy)
0 */6 * * * pkill -f main.py; pkill -f setup.sh; sleep 5; cd /home/zulfikriyahya/bot-visitor && ./setup.sh > bot.log 2>&1
```
