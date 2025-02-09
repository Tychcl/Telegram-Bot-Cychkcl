from g4f.client import Client

client = Client()
response = client.images.generate(
    model="dall-e-3",
    prompt="girl",
    width=512,
    height=1024
)

image_url = response.data[0].url
print(response)
print(image_url)
exit()
lang = "English"
text = "Красивая рыжая девушка"
context = [{"role": "user",
        "content": f"Translate the following text to {lang}: {text}, only answer without other text pls"}]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=context
)

context.append({"role":response.choices[0].message.role,"content":response.choices[0].message.content})
translated = response.choices[0].message.content
context.append({
        "role": "user",
        "content": "сколько будет 4+4 и повтори предыдущий ответ еще раз"
    })

print(response.choices[0].message.content)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=context
)
print(response.choices[0].message.content)

exit()
response = client.images.generate(
    model="dall-e-3",
    prompt=translated,
    width=512,
    height=1024
)

image_url = response.data[0].url
print(response)