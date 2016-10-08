#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import tweepy
from datetime import timedelta

# 各種キーをセット
CONSUMER_KEY = ' *** '
CONSUMER_SECRET = ' *** '
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

# Access TokenとAccess Token Secretを取得してそれぞれオブジェクトとして保存
ACCESS_TOKEN = " *** "
ACCESS_SECRET = " *** "

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
print('Done!')

#f_words設定
f_words = []
with open('f_words.txt', 'r') as f:
    for line in f:
        if True == line.startswith("#"):
            continue
        else:
            f_words.append(line.strip())

class Listener(tweepy.StreamListener):

    def on_status(self, status):
        status.created_at += timedelta(hours=9)  # 世界標準時から日本時間に

        print('------------------------------')
        print(status.text)
        print(u"{name}({screen}) {created} via {src}\n".format(
            name=status.author.name, screen=status.author.screen_name,
            created=status.created_at, src=status.source))

        if self.is_f_text(status.text):
            status_id = status.id
            screen_name = status.author.screen_name
            reply_text = "@" + screen_name + " " + "#f"
            api.update_status(status=reply_text, in_reply_to_status_id=status_id)
            print('replied!')

        return True

    def is_f_text(self, text):
        for f_word in f_words:
            if re.search(f_word, text):
                return True
        return False

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

if __name__ == '__main__':
    listener = Listener()
    stream = tweepy.Stream(auth, listener)
    stream.userstream()