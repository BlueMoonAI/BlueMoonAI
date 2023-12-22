from bluemoon.utils.logly import logly
from modules.expansion import BlueMoonExpansion

expansion = BlueMoonExpansion()

text = 'a boy running in the park'

for i in range(64):
    logly.info(expansion(text, seed=i))
