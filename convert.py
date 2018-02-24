import os
import json
emojifile = open('emoji.json', 'r')
emojilist = json.loads(emojifile.read())
emojidict = {}
ignored_keys = ['fruit', 'food']
for emoji in emojilist:
    if 'emoji' not in emoji:
        continue
    keywords = emoji.get('aliases', []) + emoji.get('tags', []) + emoji.get('description', '').split()
    for keyword in keywords:
        if keyword in ignored_keys:
            continue
        emojidict[keyword] = emojidict.get(keyword, []) + [emoji['emoji']]
emojioutfile = open('emojiconv.py', 'w')
emojioutfile.write('object_emoji=' + repr(emojidict))