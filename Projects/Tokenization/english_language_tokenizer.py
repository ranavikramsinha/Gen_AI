import tiktoken

def main():
    encoder = tiktoken.encoding_for_model("gpt-4o")
    print(f"Vocab Size: {encoder.n_vocab}")

    text = input(f"Enter English text to tokenize: ")
    tokens = encoder.encode(text)
    print(f"Tokens: {tokens}")

    token_str = input(f"Enter token IDs to decode (separated by commas): ").strip()
    if not token_str:
        print(f"Error: Please enter valide integers or token IDs separated by commas.")
        return
    
    try:
        my_tokens = [int(token) for token in token_str.split(",") if token.strip()]
        decoded = encoder.decode(my_tokens)
        print(f"Decoded Tokens: {decoded}")

    except ValueError:
        print("Error: Please enter valid integers or token IDs separated by commas")

if __name__ == "__main__":
    main()