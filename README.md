# yt-watch-history-analyzer

YouTube watch history analyzer
Retrieves your watch history and can show you charts of usage per interval (day, week, month)
Classifies video types to tell you if you reached a watch history goal, e.g.: 10 hours of learning content every week

## 0.1 Config

create `./config/config.yaml` file containing

```vim
api_key: # ADD YOUTUBE v3 API KEY HERE AS STRING
client_id: ...
client_secret: ...
client_secret_file: ...
```

## 0.2 Dev config

```
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

## 1.0 Install

```bash
make install
# or
pip install -U .
```

## 1.1 Run

```bash
# alias ipy="ipython --no-confirm-exit --no-banner -i
ipy -m yt_watch_history_analyzer
```
