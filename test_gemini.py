import google.generativeai as genai

genai.configure(api_key="AIzaSyAE4dmSfPkygp1ddzhJkOs1w_ReLwLa1bc")

try:
    models = genai.list_models()
    print("Available models:")
    for model in models:
        print(model.name)
except Exception as e:
    print(f"Error: {e}")
