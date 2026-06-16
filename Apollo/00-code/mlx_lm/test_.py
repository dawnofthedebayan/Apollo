from mlx_lm import load, generate

model, tokenizer = load("lmstudio-community/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit")

prompt = "Plan a day trip to Barcelona including Sagrada Familia, Park Güell, and the Gothic Quarter, with breakfast, lunch, dinner, snacks, local food/drink, and a budget plan."

text = generate(model, tokenizer, prompt=prompt, verbose=True, max_tokens=1024)
print(text)