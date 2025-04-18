import tiktoken

def process_text(language_name: str):
    encoder = tiktoken.encoding_for_model("gpt-4o")
    print(f"\n--- {language_name} ---")
    print(f"Vocab Size: {encoder.n_vocab}")

    text = input(f"Enter {language_name} text to tokenizer: ")
    tokens = encoder.encode(text)
    print(f"Tokens: {tokens}")

    token_str = input(f" Enter valid token IDs to decode ({language_name}) separated by commas: ").strip()
    if not token_str:
        print(f"Error: Enter valid integers/Token IDs to decode.")
        return
    
    try:
        my_tokens = [int(token) for token in token_str.split(",") if token.strip()]
        decoded = encoder.decode(my_tokens)
        print(f"Decoded Tokens: {decoded}")
    except ValueError:
        print(f"Error: please enter valid integers separated by commas.")

def main():
    choices = {
        "1": "English",
        "2": "Hindi",
        "3": "Hinglish",
    }

    while True:
        print(f"\nChoose language: ")

        for key, name in choices.items():
            print(f" {key}.{name}")
        
        print("Enter Q / q to Quit")

        lang = input("Your choice: ").strip().lower()

        if lang == "q":
            print("Goodbye! Have a nice day.")
            break
        if lang == "Q":
            print("Goodbye! Have a nice day.")
            break
        elif lang in choices:
            process_text(choices[lang])
        else:
            print("Invalid choice. Please choose 1, 2, 3 and enter q to Quit")

if __name__ == "__main__":
    main()

# टोकन = [3330, 23325, 998]
# kaise ho tum? = [1854, 1096, 2021, 14803, 30]
# who are you? =[29997, 553, 481, 30]