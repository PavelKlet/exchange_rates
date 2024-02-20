from openai import OpenAI

client = OpenAI(api_key="sk-4c1734cf75e948a6bc77d05abee37ba7",
                base_url="https://api.deepseek.com/v1"
                )

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "ОТВЕЧАЙ НА РУССКОМ"},
    ]
)

print(response.choices[0].message.content)