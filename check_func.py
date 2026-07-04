with open('e:/vibecode/sillytavern-image-gen/index.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(4860, 4920):
    print(f'{i+1}: {lines[i]}', end='')