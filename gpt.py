#!/usr/bin/env python3

import openai
import tiktoken

# Let's get our OPENAI API key from a .env file
import dotenv
import os

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

import questionary

def num_tokens_from_messages(messages, allowed_models, model="gpt-3.5-turbo"):
    """
    Returns the number of tokens used by a list of messages.
    NOTE: Assumes all the models here act like gpt-3.5-turbo-0301.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in allowed_models:
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def initialize_messages(content="You are a helpful assistant."):
    """
    Initializes the messages list.
    """
    messages = [
        {"role": "system", "content": content},
    ]
    return messages


def generate_user_role_message(prompt):
    """
    Generates a user role message.
    """
    return {"role": "user", "content": prompt}


def append_messages(messages, prompt):
    """
    Appends a message to the messages list.
    """
    messages.append(prompt)
    return messages


def generate_response(messages, model_engine="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
    )
    #print(response)
    content = response["choices"][0]["message"]["content"]

    # Now let's create message dictionary for the assistant response
    assistant_response = {"role": "assistant", "content": content}

    # Now we append the assistant response to the messages list
    messages.append(assistant_response)

    prompt_tokens = response["usage"]["prompt_tokens"]
    completion_tokens = response["usage"]["completion_tokens"]
    total_tokens = response["usage"]["total_tokens"]
    return content, total_tokens


def main():
    # Define the models we want to use
    model_choices = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"]

    # Now make a dictionary of the models and their descriptions and a name for the model
    model_descriptions = {
        "gpt-3.5-turbo": "GPT-3.5 Turbo is a 3.5B parameter model trained on a large corpus of text data.",
        "gpt-4": "GPT-4 is a 4.5B parameter model trained on a large corpus of text data.",
        "gpt-4-32k": "GPT-4-32k is a 4.5B parameter model trained on a large corpus of text data with a larger context length",
    }

    # Create a dictionary of the models and their names
    model_name = {
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
        "gpt-4": "GPT-4",
        "gpt-4-32k": "GPT-4 32k",
    }

    # Create a dictionary of the models and their prices per token
    model_price_per_thousand_tokens = {
        "gpt-3.5-turbo": 0.002,
        "gpt-4": 0.03,
        "gpt-4-32k": 0.06,
    }

    # Now let's select the model we want to use using questionary with the choices
    # we defined above and with descriptions for each model
    model_request = questionary.select(
        "Which model do you want to use?",
        choices=["GPT-3.5 Turbo", "GPT-4"],
    ).ask()

    # Using the model_name dictionary, we can get the model name from the model_request
    # and use that to get the model engine name from the model_choices dictionary
    model_engine = [key for key, value in model_name.items() if value == model_request][0]

    # Now we have the model engine name, we can use tiktoken to get the price per token
    # First we get the encoding
    encoding = tiktoken.encoding_for_model(model_engine)

    # Let us initialize the messages list with the system role
    messages = initialize_messages()

    # Now let's create a loop where we ask the user for a question using questionary
    # After we get a response, we ask if the user wishes to continue.
    # If so, we ask another question. If not, we exit the program.

    while True:
        topic = questionary.text("What topic do you want to talk about?").ask()

        # Generate the messages
        user_role_message = generate_user_role_message(topic)

        # Append the messages
        messages = append_messages(messages, user_role_message)

        response_text, total_tokens = generate_response(messages, model_engine=model_engine)

        print(f"Response from {model_name[model_engine]}:\n")

        print(response_text)

        print()

        # Estimate the cost of the request
        total_cost = total_tokens * model_price_per_thousand_tokens[model_engine] / 1000
        print(f"Tokens used: {total_tokens}. Cost: ${total_cost:.5f}.")

        continue_chatting = questionary.confirm(
            "Do you want to continue chatting?"
        ).ask()
        if not continue_chatting:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
