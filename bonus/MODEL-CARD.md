# Model Card: Cafe Xưa Aligned Customer Service Chatbot

This is the model documentation for the Cafe Xưa customer service assistant, fine-tuned using Direct Preference Optimization (DPO).

## Model Details

- **Base Model**: `unsloth/Qwen2.5-3B-bnb-4bit`
- **Starting Policy**: SFT-mini adapter (trained on 1k Vietnamese Alpaca dataset)
- **DPO Adapter**: `adapters/dpo-coffee`
- **Quantization**: Merged & Quantized to GGUF `Q4_K_M`
- **Language**: Vietnamese

## Training Configuration

- **Dataset**: `bonus/data/pairs.parquet` (100 custom Vietnamese preference pairs)
- **Algorithm**: DPO (Sigmoid loss)
- **Beta**: 0.1
- **Learning Rate**: 5e-7
- **Epochs**: 2
- **Batch Size**: 1
- **Gradient Accumulation Steps**: 8
- **Optimizer**: AdamW 8-bit

## Intended Use & Boundaries

### What the Model is Designed For:
1. Answering frequently asked questions (FAQs) about Cafe Xưa:
   - Operating hours (7:00 AM - 10:30 PM).
   - Location (2nd floor, 15 Hàng Gai, Hoàn Kiếm, Hà Nội - entrance via a small alleyway next to the wood souvenir shop, wooden stairs to the 2nd floor).
   - Menu items and pricing (Signature Hanoi egg coffee 45k, Coconut coffee, and egg mung bean drink).
   - Amenities (Wifi password `cafexuahangai`, quiet study space on weekdays).
2. Maintaining a warm, polite, and service-oriented tone typical of Hanoi hospitality.

### Boundaries and Guardrails (Aligned via DPO):
1. **No Competitive Slandering**: If asked to compare with competitors (e.g., Cafe Giảng), the model will acknowledge the competitor politely while highlighting its own unique features, rather than slandering the competitor or boasting arrogantly.
2. **Polite Reservation Limits**: Refuses bookings over 15 people on busy Saturday nights, redirecting users to call the hotline `0912345678` or arrive earlier.
3. **No Hallucinations**: Does not make up non-existent prices, parking structures (explicitly apologizes for not having car parking and suggests public lakeside parking), or franchise policies.
