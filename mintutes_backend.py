
import modal

# Set up the Modal stub with the required image and dependencies
stub = modal.Stub(name="minutes-project", image=modal.Image.debian_slim().pip_install("openai"))

# Define the function to generate meeting minutes using OpenAI
@stub.function(secret=modal.Secret.from_name("my-openai-secret"))
def generate_minutes(prompt):
    import openai
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": prompt}
                                                      ])
    return completion.choices[0].message.content

# Local entry point for testing
@stub.local_entrypoint()
def main(prompt: str):
    minutes = generate_minutes.remote(prompt)
    print(minutes)

# If you want to run the function locally for testing
if __name__ == "__main__":
    # Replace with your instructPrompt + transcript
    request = "Your instructPrompt and transcript here"
    main(request)
