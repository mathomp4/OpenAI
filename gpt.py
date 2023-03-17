#!/usr/bin/env python3

import openai

# Let's get our OPENAI API key from a .env file
import dotenv
import os
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

import questionary

def generate_response(prompt, model_engine="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            ],
        max_tokens=2048
    )
    output = response['choices'][0]['message']['content']
    return output

def main():

    # Define the models we want to use
    model_choices = ["gpt-3.5-turbo", "gpt-4"]

    # Now make a dictionary of the models and their descriptions and a name for the model
    model_descriptions = {
        "gpt-3.5-turbo": "GPT-3.5 Turbo is a 3.5B parameter model trained on a large corpus of text data.",
        "gpt-4": "GPT-4 is a 4.5B parameter model trained on a large corpus of text data.",
    }
    model_name = {
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
        "gpt-4": "GPT-4",
    }

    # Now let's select the model we want to use using questionary with the choices
    # we defined above and with descriptions for each model

    model_request = questionary.select(
        "Which model do you want to use?",
        choices=["GPT-3.5 Turbo", "GPT-4"],
    ).ask()

    # Now let's get the model engine name from the model name we selected
    model_engine = [key for key, value in model_name.items() if value == model_request][0]

    # Now let's create a loop where we ask the user for a question using questionary
    # After we get a reponse, we ask if the user wishes to continue.
    # If so, we ask another question. If not, we exit the program.

    while True:
        topic = questionary.text("What topic do you want to talk about?").ask()
        response = generate_response(topic, model_engine=model_engine)

        print(f'Response from {model_name[model_engine]}:\n')

        print(response)

        # Print a line break
        print()

        continue_chatting = questionary.confirm("Do you want to continue chatting?").ask()
        if not continue_chatting:
            print("Goodbye!")
            break

if __name__ == '__main__':
    main()
