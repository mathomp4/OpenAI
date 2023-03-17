#!/usr/bin/env python3

import openai

# Let's get our OPENAI API key from a .env file
import dotenv
import os
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

chat_history = []
model_engine = "gpt-3.5-turbo"

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            ],
        max_tokens=150
    )
    output = response['choices'][0]['message']['content']
    chat_history.append(output)
    return output

def main():
    while True:
        user_input = input("You: ")
        # If the user types 'q', 'quit', or 'exit', exit the program
        if user_input.lower() in ['q', 'quit', 'exit']:
            print('AI: Goodbye!')
            break
        # Otherwise, ask GPT-3 a question
        else:
            response = generate_response(user_input)
            print("AI: " + response)


if __name__ == '__main__':
    main()
