from g4f import Client
import g4f
import g4f.Provider
import g4f.providers

c = Client()

response = c.chat.completions.create(
        model="deepseek-v3",
        messages=[{'role': 'user', 'content': 'Translate the following text to English: Красивая темнокожая девушка, only answer without other text pls'}],
        provider=g4f.Provider.DeepseekAI_JanusPro7b
    )
print(response)