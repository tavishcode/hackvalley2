import os
import json
emojifile = open('emoji.json', 'r')
emojilist = json.loads(emojifile.read())
emojidict = {}
ignored_keys = ['fruit', 'food', 'red', 'blue', 'color']
forbidden_keys = ['People', 'person', 'people']
for emoji in emojilist:
    if 'emoji' not in emoji:
        continue
    keywords = emoji.get('aliases', []) + emoji.get('tags', []) + emoji.get('description', '').split()
    removeEmoji = False
    for fk in forbidden_keys:
        if fk in keywords:
            removeEmoji = True
            break
    if removeEmoji:
        continue
    for keyword in keywords:
        keyword = keyword.lower()
        if keyword in ignored_keys:
            continue
        emojidict[keyword] = emojidict.get(keyword, set([])).union(set([emoji['emoji']]))
emojioutfile = open('emojiconv.py', 'w')
emojioutfile.write('object_emoji=' + repr(emojidict))