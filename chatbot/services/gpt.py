import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


class GPTManager:
    def __init__(self, chat_history):
        self.chat_history = chat_history

    def generate(
        self, system_prompt, query, max_tokens=64, stream=False, use_history=True
    ):
        messages = []

        if use_history:
            history = self.chat_history.get_messages()
            print("history: ", history)
            messages = [*history]

        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        result = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=max_tokens,
            stream=stream,
        )

        if stream:
            return result

        return result.choices[0].message.content
