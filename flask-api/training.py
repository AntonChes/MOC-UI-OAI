import os
import openai
openai.api_key = ""
openai.FineTune.create(training_file="/Users/master/Documents/openai_api/train1_prepared.jsonl")