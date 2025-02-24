import os
import argparse
from dotenv import load_dotenv
from openai import AzureOpenAI
import time
import random

load_dotenv()

system_prompt = """
# E-commerce Bookstore Assistant

You are an assistant for an e-commerce bookstore. You are knowledgeable about various genres of books, including fiction, non-fiction, science fiction, fantasy, mystery, romance, and more. You can help users find books based on their preferences and interests. You can also assist with recommendations for bestsellers, new releases, and classic literature.

## Website Features

You are familiar with the features of the bookstore's website, including:
- Searching for books
- Filtering by category
- Managing user accounts
- Adding books to the cart
- Proceeding to checkout
- Tracking orders

## Promotions and Discounts

You are knowledgeable about promotions and discounts available on the website. Currently, there are discounts on the following books:
- "Dune" by Frank Herbert - 20% off
- "Neuromancer" by William Gibson - 15% off
- "Foundation" by Isaac Asimov - 10% off

Additionally, there is a special promotion for first-time customers: use the code "WELCOME10" to get 10% off your first purchase. There are also seasonal discounts during holidays such as Black Friday, Cyber Monday, and Christmas.

## Customer Assistance

You can help users with any issues they may encounter, such as problems with payment or delivery. You are patient and provide clear, concise explanations. You can also assist with managing user reviews and ratings for books.

## Additional Information

You can provide information about:
- The history of the bookstore, its mission, and its values
- Different membership levels and the benefits associated with each
- The bookstore's return policy, including how to initiate a return and what to expect during the process
- The bookstore's customer service policies and contact information for further assistance
- Community events, such as book signings, author talks, and reading groups
- Gift card options and how to purchase and redeem gift cards
- The bookstore's loyalty program, including how to earn and redeem points
- Digital offerings, such as e-books and audiobooks, and how to navigate these options
- Shipping options, including delivery times and costs
- Social media presence and how to follow the bookstore on various platforms
- The bookstore's blog and newsletter, including how to subscribe
- Website accessibility features and how to use them
- The bookstore's privacy policy and how user data is protected
- Environmental initiatives and how the bookstore is working to reduce its environmental impact
- Charitable initiatives and how users can get involved

## Book Recommendations

You can recommend books based on various criteria, such as:
- Genre
- Author
- Publication date
- User ratings
- Bestseller lists
- Award-winning books

## Personalized Recommendations

You can provide personalized recommendations based on user preferences and reading history. You can also suggest books that are similar to ones the user has enjoyed in the past.

## Book Reviews and Ratings

You can help users find and write reviews for books. You can also provide information about the average rating and number of reviews for a particular book.

## Book Formats

You can provide information about the different formats available for books, including:
- Hardcover
- Paperback
- E-book
- Audiobook

You can also explain how to access and use these formats on various devices.

## Order Tracking

You can help users track their orders and provide information about the status of their delivery. You can also assist with resolving any issues related to shipping and delivery.

## Customer Support

You can provide contact information for the bookstore's customer support team and explain how to reach them for further assistance. You can also provide information about the bookstore's live chat support and email support options.

## Community Engagement

You can provide information about the bookstore's community engagement initiatives, such as:
- Book donation programs
- Literacy programs
- Partnerships with local schools and libraries

You are a valuable resource for any customer looking to find the perfect book or resolve any issues they may have with their orders.
"""

user_prompt = """
I am looking for a new science fiction book to read. I prefer books that have a mix of adventure and thought-provoking themes. Can you recommend some popular science fiction books that fit this description? Additionally, I would like to know if there are any ongoing promotions or discounts on science fiction books. I am also interested in learning how to create an account on the bookstore's website and how to add books to my cart. Can you provide step-by-step instructions for these tasks? Furthermore, I would like to know how to track my orders once I have made a purchase. Any advice or resources you can provide would be greatly appreciated. Thank you for your help. Also, I am interested in learning more about the bookstore's history and mission. Can you provide some information about that? I would also like to know about the different membership levels and the benefits associated with each. Additionally, I am curious about the bookstore's return policy. Can you explain how to initiate a return and what to expect during the process? I am also interested in the bookstore's community events, such as book signings, author talks, and reading groups. Can you provide information about these events and how to participate? I would like to know more about the bookstore's gift card options and how to purchase and redeem gift cards. Can you provide information about the bookstore's loyalty program, including how to earn and redeem points? I am also interested in the bookstore's digital offerings, such as e-books and audiobooks. Can you help me navigate these options and provide information about the different formats available and how to access them? Additionally, I would like to know about the bookstore's shipping options, including delivery times and costs. Can you help me track my orders and resolve any issues with delivery? I am also interested in the bookstore's social media presence and how to follow the bookstore on various platforms. Can you provide information about the bookstore's blog and newsletter, including how to subscribe? I would like to know about the bookstore's website accessibility features and how to use them. Can you provide information about the bookstore's privacy policy and how user data is protected? I am also interested in the bookstore's environmental initiatives and how the bookstore is working to reduce its environmental impact. Can you provide information about the bookstore's charitable initiatives and how users can get involved? Thank you for your help.
"""

def main(deployment: str, iterations: int):
    if deployment == "random":
        deployment = random.choice(["standard", "datazone", "global"])
    elif deployment not in ["standard", "datazone", "global"]:
        raise ValueError("Invalid deployment value. Must be one of: 'standard', 'datazone', 'global', or 'random'")

    if iterations == "random":
        iterations = random.randint(1, 10)
    elif not (1 <= iterations <= 10):
        raise ValueError("Invalid iterations value. Must be an integer between 1 and 10, or 'random'")

    if deployment == "standard":
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_STANDARD")
        api_key = os.getenv("AZURE_OPENAI_API_KEY_STANDARD")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION_STANDARD")
        deployment_name = os.getenv("AZURE_OPENAI_DEPELOYMENT_NAME_STANDARD")
    elif deployment == "datazone":
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_DATAZONE")
        api_key = os.getenv("AZURE_OPENAI_API_KEY_DATAZONE")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION_DATAZONE")
        deployment_name = os.getenv("AZURE_OPENAI_DEPELOYMENT_NAME_DATAZONE")
    elif deployment == "global":
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_GLOBAL")
        api_key = os.getenv("AZURE_OPENAI_API_KEY_GLOBAL")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION_GLOBAL")
        deployment_name = os.getenv("AZURE_OPENAI_DEPELOYMENT_NAME_GLOBAL")


    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )

    print(f"Using deployment: {deployment}")
    print(f"Number of iterations: {iterations}")

    for i in range(iterations):
        print(f"Iteration: {i + 1}")

        start_time = time.time()

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt },
                {"role": "user", "content": user_prompt }
            ]
        )

        # Measure response time
        response_time = time.time() - start_time

        # Get usage information, including cached tokens
        usage_data = response.usage

        # Check and print usage details
        if hasattr(usage_data, 'prompt_tokens'):
            print(f"Prompt Tokens: {usage_data.prompt_tokens}")
        else:
            print("Prompt tokens data not available.")

        if hasattr(usage_data, 'completion_tokens'):
            print(f"Completion Tokens: {usage_data.completion_tokens}")
        else:
            print("Completion tokens data not available.")

        if hasattr(usage_data, 'total_tokens'):
            print(f"Total Tokens: {usage_data.total_tokens}")
        else:
            print("Total tokens data not available.")

        if hasattr(usage_data, 'prompt_tokens_details') and hasattr(usage_data.prompt_tokens_details, 'cached_tokens'):
            cached_tokens = usage_data.prompt_tokens_details.cached_tokens
            print(f"Cached Tokens: {cached_tokens} / {usage_data.prompt_tokens}")
        else:
            print("Cached tokens data not available or caching not applied.")

        # Print response
        #print(f"Response: {response.choices[0].message.content}")
        print(f"Response Time: {response_time:.4f} seconds\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process deployment and iterations")
    parser.add_argument("deployment", type=str, choices=["standard", "datazone", "global", "random"], help="Deployment type")
    parser.add_argument("iterations", type=str, help="Number of iterations (1-10 or 'random')")
    args = parser.parse_args()
    main(args.deployment, args.iterations)