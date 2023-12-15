from modules.expansion import BlueMoonExpansion

expansion = BlueMoonExpansion()

text = 'a handsome man'

for i in range(64):
    print(expansion(text, seed=i))
