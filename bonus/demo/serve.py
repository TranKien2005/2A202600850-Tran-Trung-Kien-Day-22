import os
import argparse
from pathlib import Path

def serve_unsloth():
    import torch
    from unsloth import FastLanguageModel
    from peft import PeftModel

    REPO = Path(__file__).resolve().parent.parent.parent
    base_model = "unsloth/Qwen2.5-3B-bnb-4bit"
    sft_path = REPO / "adapters" / "sft-mini"
    dpo_coffee_path = REPO / "adapters" / "dpo-coffee"

    print("Loading Cafe Xưa Chatbot using Unsloth...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_model, max_seq_length=512, dtype=None, load_in_4bit=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load adapters
    if sft_path.exists():
        model = PeftModel.from_pretrained(model, str(sft_path))
        print("Loaded SFT-mini adapter.")
    if dpo_coffee_path.exists():
        model = PeftModel.from_pretrained(model, str(dpo_coffee_path))
        print("Loaded DPO-coffee adapter.")

    FastLanguageModel.for_inference(model)

    import gradio as gr

    def respond(message, history):
        messages = []
        for h in history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": message})

        inputs = tokenizer.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True
        ).to("cuda")

        with torch.no_grad():
            out = model.generate(
                input_ids=inputs,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
        response = tokenizer.decode(out[0][inputs.shape[1]:], skip_special_tokens=True)
        return response.strip()

    demo = gr.ChatInterface(
        fn=respond,
        title="☕ Cafe Xưa Hanoi - Customer Service Chatbot",
        description="Chào mừng bạn đến với Cafe Xưa! Mình là bot trợ lý ảo sẵn sàng trả lời các câu hỏi về địa chỉ, giờ mở cửa, menu cà phê trứng và các dịch vụ của quán.",
        examples=[
            "Quán mình ở đâu thế shop?",
            "Mấy giờ quán đóng cửa vậy ạ?",
            "Cà phê trứng ở đây có ngon không shop ơi?",
            "Có không gian ngồi học laptop không em?"
        ]
    )
    demo.launch(share=True)

def serve_gguf(gguf_path):
    from llama_cpp import Llama
    import gradio as gr

    print(f"Loading GGUF model from {gguf_path}...")
    llm = Llama(
        model_path=str(gguf_path),
        n_ctx=512,
        n_gpu_layers=-1,
        verbose=False
    )

    def respond(message, history):
        messages = []
        for h in history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": message})

        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=256,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()

    demo = gr.ChatInterface(
        fn=respond,
        title="☕ Cafe Xưa Hanoi - GGUF Server",
        description="Cafe Xưa Chatbot chạy qua GGUF & llama-cpp-python.",
        examples=[
            "Quán mình ở đâu thế shop?",
            "Mấy giờ quán đóng cửa vậy ạ?"
        ]
    )
    demo.launch(share=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gguf", type=str, default=None, help="Path to GGUF model file")
    args = parser.parse_args()

    if args.gguf:
        serve_gguf(args.gguf)
    else:
        serve_unsloth()
