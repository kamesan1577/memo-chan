# MemoChan
[](./memochan.png)

技育 CAMP vol.8 でのチーム開発リポジトリ

## Install
### With Docker
- README.mdの動作だと./sqliteディレクトリにdbが保存される設定になっています
```shell
docker pull kamesan1577/discord-memo:latest 
docker run --env DISCORD_TOKEN="your_bot_token" \
--env SQLALCHEMY_DATABASE_URL="sqlite:////src/discord_memo/bot.db" \
-v ./sqlite/:/src/discord_memo/ \
kamesan1577/discord-memo:latest 
```
または
```shell
git clone --depth 1 https://github.com/kamesan1577/geek-camp-vol8.git
cd geek-camp-vol8 && cp .env.sample .env
vim .env # discord bot tokenを記述する
docker compose up --build
```
