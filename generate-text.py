#!/usr/bin/python

# https://medium.com/pythoneers/use-ai-to-generate-text-with-3-lines-of-python-code-190aa30f3ac4

import sys
from transformers import pipeline

prompt = sys.argv[1:][0]
print('The prompt is: "' + prompt + '"')
print('Please wait...')

# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

results = generator(prompt, max_length=300, do_sample=True, temperature=0.9)
result = results[0]['generated_text'].split('.')[:-1]

print('.'.join(result))

