from mlx_lm import load, generate
import os
os.environ["HF_TOKEN"] = "virgo5-vizvyr-sunnIz"


#model, tokenizer = load("mlx-community/Qwen3-4B-4bit")

model, tokenizer = load("lmstudio-community/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit")


prompt = "Plan a trip to Barcelona for me."
messages = [{"role": "user", "content": prompt}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True
)

text = generate(model, tokenizer, prompt=prompt, verbose=True)