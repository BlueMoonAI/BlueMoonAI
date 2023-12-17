from modules.expansion import BlueMoonExpansion

expansion = BlueMoonExpansion()

text = 'a boy running in the park'

for i in range(64):
    print(expansion(text, seed=i))
