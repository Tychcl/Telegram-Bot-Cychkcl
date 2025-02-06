from g4f.client import Client

client = Client()
lang = "English"
text = "Красивая рыжая девушка"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": f"Translate the following text to {lang}: {text}, only answer without other text pls"
    }]
)

translated = response.choices[0].message.content

response = client.images.generate(
    model="dall-e-3",
    prompt=translated,
    width=512,
    height=1024
)

image_url = response.data[0].url
print(response)