from typing import Any, Iterator, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from mlx_lm import load
from mlx_lm.generate import stream_generate
from mlx_lm.sample_utils import make_sampler

class MLXChatModel(BaseChatModel):
    """
    LangChain-compatible chat model wrapper for local MLX inference.
    Drop this into any script that needs local Apple Silicon LLM inference.
    """

    model_path: str
    max_tokens: int = 1024
    temperature: float = 0.5
    stop_sequences: List[str] = ["</s>", "<|end|>", "<|eot_id|>", "<｜end▁of▁sentence｜>"]

    # Internal fields — excluded from Pydantic serialisation
    _model: Any = None
    _tokenizer: Any = None

    class Config:
        arbitrary_types_allowed = True

    def _load_model(self):
        """Lazy-load the model on first use so import doesn't trigger a load."""
        if self._model is None:
            print(f"Loading MLX model: {self.model_path}")
            self._model, self._tokenizer = load(self.model_path)
            print("Model loaded.")

    def _build_prompt(self, messages: List[BaseMessage]) -> str:
        """
        Convert LangChain messages into a plain prompt string.
        Uses the tokenizer's chat template if available, otherwise falls back
        to a simple Human/Assistant format.
        """
        lc_to_role = {"human": "user", "ai": "assistant", "system": "system"}

        chat_messages = [
            {"role": lc_to_role.get(m.type, "user"), "content": m.content}
            for m in messages
        ]

        if hasattr(self._tokenizer, "apply_chat_template"):
            return self._tokenizer.apply_chat_template(
                chat_messages,
                tokenize=False,
                add_generation_prompt=True,
            )

        # Fallback for tokenizers without a chat template
        lines = []
        for msg in chat_messages:
            if msg["role"] == "system":
                lines.append(f"System: {msg['content']}")
            elif msg["role"] == "user":
                lines.append(f"Human: {msg['content']}")
            elif msg["role"] == "assistant":
                lines.append(f"Assistant: {msg['content']}")
        lines.append("Assistant:")
        return "\n\n".join(lines)

    def _should_stop(self, generated_so_far: str) -> bool:
        return any(seq in generated_so_far for seq in self.stop_sequences)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs,
    ) -> ChatResult:
        self._load_model()
        prompt = self._build_prompt(messages)
        active_stop = self.stop_sequences + (stop or [])

        collected = []
        for token in stream_generate(
            self._model,
            self._tokenizer,
            prompt=prompt,
            max_tokens=self.max_tokens,
            sampler=make_sampler(temp=self.temperature),
        ):
            text = token.text if hasattr(token, "text") else str(token)
            collected.append(text)
            full = "".join(collected)
            if any(seq in full for seq in active_stop):
                # Trim the stop sequence from the end
                for seq in active_stop:
                    if seq in full:
                        full = full[: full.index(seq)]
                return ChatResult(
                    generations=[ChatGeneration(message=AIMessage(content=full.strip()))]
                )

        return ChatResult(
            generations=[
                ChatGeneration(message=AIMessage(content="".join(collected).strip()))
            ]
        )

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs,
    ) -> Iterator[ChatGenerationChunk]:
        self._load_model()
        prompt = self._build_prompt(messages)
        active_stop = self.stop_sequences + (stop or [])

        collected = []
        for token in stream_generate(
            self._model,
            self._tokenizer,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temp=self.temperature,
        ):
            text = token.text if hasattr(token, "text") else str(token)
            collected.append(text)
            full = "".join(collected)

            if any(seq in full for seq in active_stop):
                for seq in active_stop:
                    if seq in full:
                        clean = full[: full.index(seq)].strip()
                        # Yield only the new part of the clean text
                        already_yielded = "".join(collected[:-1])
                        remainder = clean[len(already_yielded):]
                        if remainder:
                            yield ChatGenerationChunk(
                                message=AIMessageChunk(content=remainder)
                            )
                return

            yield ChatGenerationChunk(message=AIMessageChunk(content=text))

    @property
    def _llm_type(self) -> str:
        return "mlx-local"