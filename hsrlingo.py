import os
design_data_dir = './StarRail_Data/StreamingAssets/DesignData/Windows/'

def replace_bytes(content, idx, choice, param):
    for i in range(param):
        content[idx:idx + 2] = choice.encode('utf-8')
        idx += 3
    return idx

choices = ['en', 'jp', 'cn', 'kr']
voice = None
while voice not in choices:
    voice = input(f'What voice language would you like? {choices}\n')
text = None
while text not in choices:
    text = input(f'What text language would you like? {choices}\n')

for filename in os.listdir(design_data_dir):
    filepath = os.path.join(design_data_dir, filename)
    with open(filepath, 'rb') as f:
        content = bytearray(f.read())
        pattern_to_find = 'SpriteOutput/UI/Fonts/RPG_CN.ttf'.encode('utf-8')
        try:
            idx = content.index(pattern_to_find)
        except ValueError:
            continue
        pattern = 'Korean'.encode('utf-8')
        idx = content.index(pattern)
        print(f'Found the relevant file {filename}')
        print('Patching language')
        # Move to os text language
        idx += 10
        # Change os text language
        idx += 4
        idx = replace_bytes(content, idx, text, 4)
        # Move to cn voice language
        idx += 1
        # Change cn voice language
        idx += 5
        idx = replace_bytes(content, idx, voice, 2)
        # Move to os voice language
        idx += 1
        # Change os voice language
        idx += 5
        idx = replace_bytes(content, idx, voice, 5)
        # Move to cn text language
        idx += 1
        # Change cn text language
        idx += 4
        idx = replace_bytes(content, idx, text, 2)
        print('Overwriting old file')
        with open(filepath, 'wb') as w:
            w.write(content)
        print('Language patched successfully')
        exit()
print('Couldn\'t find file to patch. Make sure this file is placed in the same folder as StarRail.exe')