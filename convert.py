import os
import json
emojifile = open('emoji.json', 'r')
emojilist = json.loads(emojifile.read())
emojidict = {}
for emoji in emojilist:
    if 'emoji' not in emoji:
        continue
    keywords = emoji.get('aliases', []) + emoji.get('tags', [])
    if 'description' in emoji:
        keywords.append(emoji['description'])
    for keyword in keywords:
        emojidict[keyword] = emojidict.get(keyword, []) + [emoji['emoji']]
emojioutfile = open('emojiconv.py', 'w')
emojioutfile.write(repr(emojidict))