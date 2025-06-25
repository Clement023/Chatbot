import argparse
import json
from transformers import AutoModelForCausalLM, AutoTokenizer # type: ignore

# Define default model name as a constant
DEFAULT_MODEL_NAME = "gpt2-large"

def load_model_and_tokenizer(model_name=DEFAULT_MODEL_NAME):
    """
    Load the pre-trained model and tokenizer.
    """
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
   
    # Set the pad_token to eos_token if pad_token is not already set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer

def generate_text(prompt, model, tokenizer, conversation_history=None, max_length=50, temperature=0.7, num_return_sequences=1, top_k=50, top_p=0.9):
    """
    Generate text based on a given prompt and conversation history.
    """
    try:
        # Combine conversation history with the current prompt
        if conversation_history:
            prompt = "\n".join(conversation_history) + "\n" + prompt

        # Tokenize the input and create attention mask
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Generate text with attention mask and pad token ID
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,  # Limit to top_k tokens for diversity
            top_p=top_p,  # Use nucleus sampling for diversity
            pad_token_id=tokenizer.eos_token_id  # Use the EOS token as the pad token
        )

        return tokenizer.batch_decode(outputs, skip_special_tokens=True)
    except Exception as e:
        error_message = f"An error occurred: {str(e)} | Prompt: {prompt} | Conversation History: {conversation_history}"
        print(error_message)  # Log the error for debugging
        return [error_message]

def main():
    """ 
    Main function to handle argument parsing and text generation.
    """
    parser = argparse.ArgumentParser(description="Generate text using a pre-trained GPT model.")
    parser.add_argument("--model_name", type=str, default=DEFAULT_MODEL_NAME, help="Name of the pre-trained model to use.")
    parser.add_argument("--prompt", type=str, required=True, help="Input text prompt for text generation.")
    parser.add_argument("--max_length", type=int, default=50, help="Maximum length of the generated text.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature.")
    parser.add_argument("--num_return_sequences", type=int, default=1, help="Number of sequences to generate.")
    parser.add_argument("--conversation_history", type=str, nargs="*", help="Optional conversation history.")
    args = parser.parse_args()

    if args.num_return_sequences <= 0:
        raise ValueError("The 'num_return_sequences' argument must be a positive integer.")

    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model_name)

    # Generate text
    generated_text = generate_text(
        prompt=args.prompt,
        model=model,
        tokenizer=tokenizer,
        conversation_history=args.conversation_history,
        max_length=args.max_length,
        temperature=args.temperature,
    )
    print(json.dumps({"generated_text": generated_text}, indent=4))


if __name__ == "__main__":
    main()