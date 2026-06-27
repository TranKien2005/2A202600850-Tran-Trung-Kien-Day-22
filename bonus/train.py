import os
import json
from pathlib import Path
import torch
from datasets import Dataset
from peft import PeftModel
from trl import DPOConfig, DPOTrainer
from unsloth import FastLanguageModel

def main():
    REPO = Path(__file__).resolve().parent.parent
    sft_path = REPO / "adapters" / "sft-mini"
    pref_path = REPO / "bonus" / "data" / "pairs.parquet"
    output_dir = REPO / "adapters" / "dpo-coffee"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== Training DPO Chatbot for Cafe Xưa ===")
    print(f"SFT Adapter: {sft_path}")
    print(f"Preference Dataset: {pref_path}")
    print(f"Output: {output_dir}")

    # Set parameters similar to NB3
    base_model = "unsloth/Qwen2.5-3B-bnb-4bit"
    max_len, max_prompt = 512, 256
    batch, grad_accum = 1, 8

    # Load policy model
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_model, max_seq_length=max_len, dtype=None, load_in_4bit=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load SFT adapter
    if sft_path.exists():
        model = PeftModel.from_pretrained(model, str(sft_path), is_trainable=True)
        print("Loaded SFT-mini adapter as starting policy.")
    else:
        print("WARNING: SFT-mini adapter not found. Training DPO directly on base model.")

    # Get PEFT model for DPO
    model = FastLanguageModel.get_peft_model(
        model, r=16, lora_alpha=32, lora_dropout=0.0, bias="none",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        use_gradient_checkpointing="unsloth",
        random_state=42, use_rslora=False, loftq_config=None,
    )

    config = DPOConfig(
        output_dir=str(output_dir.parent / "dpo-coffee-checkpoints"),
        per_device_train_batch_size=batch,
        gradient_accumulation_steps=grad_accum,
        num_train_epochs=2, # Let's train for 2 epochs since dataset is small (100 pairs)
        learning_rate=5e-7,
        beta=0.1,
        max_length=max_len,
        max_prompt_length=max_prompt,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        logging_steps=5,
        save_strategy="no",
        optim="adamw_8bit",
        bf16=torch.cuda.is_bf16_supported(),
        fp16=not torch.cuda.is_bf16_supported(),
        seed=42,
        loss_type="sigmoid",
        report_to="none",
    )

    pref = Dataset.from_parquet(str(pref_path))
    trainer = DPOTrainer(
        model=model, ref_model=None, args=config,
        train_dataset=pref, processing_class=tokenizer,
    )
    
    train_result = trainer.train()

    trainer.model.save_pretrained(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    print(f"Saved DPO Cafe adapter to {output_dir}")

if __name__ == "__main__":
    main()
