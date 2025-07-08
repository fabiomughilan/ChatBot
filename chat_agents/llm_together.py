# llm_together.py
from crewai import LLM
from together import Together

class TogetherLLM(LLM):
    def __init__(self, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"):
        self.client = Together()
        self.model = model

    def call(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
