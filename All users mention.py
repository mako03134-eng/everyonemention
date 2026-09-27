import json, discum, os, requests, time

try:
    config = json.loads(open("config.json", "r", encoding="utf-8").read())
    token = config["token"]
    guild_id = config["parse_info"]["guild_id"]
    channel_id = config["parse_info"]["channel_id"]
    count = config["count"]
except:
    open("config.json", "w").write("""{

    "token": "User's Token",
    
    "parse_info":{
        "guild_id": "guild_id",
        "channel_id": "channel_id"
    },

    "count": 1

}""")
    exit()

bot = discum.Client(token=token)

def close_after_fetching(resp, guild_id):
    if bot.gateway.finishedMemberFetching(guild_id):
        lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
        print(str(lenmembersfetched) + ' members fetched')
        bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
        bot.gateway.close()

def get_members(guild_id, channel_id):
    bot.gateway.fetchMembers(guild_id, channel_id, keep='all', wait=1)
    bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
    bot.gateway.run()
    bot.gateway.resetSession()
    return bot.gateway.session.guild(guild_id).members

members = get_members(guild_id=guild_id, channel_id=channel_id)

mentions = []
for member_id in members:
    mentions.append("<@" + str(member_id) + ">")

mentionsed = mentions

time.sleep(3)

os.system("cls")

send_messages = [

]

mentions = []
for mention in mentionsed:
    if len(" ".join(mentions)) > 2000:
        send_messages.append(" ".join(mentions))
        mentions = []
    else:
        mentions.append(mention)
send_messages.append(" ".join(mentions))

def main(send_message):
    while True:
        try:
            message = requests.post(f"https://discordapp.com/api/v9/channels/{channel_id}/messages", headers={
                "authorization": token,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36"
            }, json={
                "content": send_message
            })
            id = message.json()["id"]
            while True:
                try:
                    res = requests.delete(f"https://discordapp.com/api/v9/channels/{channel_id}/messages/{id}", headers={
                        "authorization": token,
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36"
                    })
                    if res.status_code == 204:
                        print(str(len(send_message.split(" "))) + "명의 유저를 맨션함")
                        break
                except:
                    pass
            break
        except:
            pass

for _ in range(count):
    for send_message in send_messages:
        main(send_message)
    print(f"[+] Count {_ + 1} Finished")
print("\n[!] All Users Mention Finished")
while True: pass