# Creative Bonus Challenge: Cafe Xưa Customer Service Chatbot

This folder contains the implementation of a domain-aligned customer service assistant for **Cafe Xưa**, an authentic old-quarter style coffee shop located in Hanoi.

---

## 1. Chatbot Alignment Profile

- **Audience**: Customers seeking information about Cafe Xưa (FAQ, directions, signature menu, seat availability).
- **Domain**: Authentic Hanoi old-quarter cafe service. Traditional cafe vibe, warm, welcoming, polite, and service-oriented.
- **Application Objective**: Helpfully answer common customer questions, direct them properly, prevent hallucination of pricing or services, avoid generic AI language, and politely refuse/redirect competitive or off-topic queries.
- **Tone**: Traditional Hanoi politeness (using greetings like "Dạ", "ạ", and friendly forms of address like "bạn/shop", "anh/chị").

---

## 2. File Structure

- **`generate_data.py`**: Compiles and writes the 100 preference pairs containing Hanoi old quarter context into `data/pairs.parquet`.
- **`data/pairs.parquet`**: Stored binary preference dataset (formatted as `prompt`, `chosen`, and `rejected`).
- **`train.py`**: Code script to run `DPOTrainer` with Unsloth to align our policy on top of the SFT-mini adapter.
- **`demo/serve.py`**: A Gradio web user interface chat interface supporting both PyTorch (Unsloth) and quantized GGUF execution.
- **`MODEL-CARD.md`**: Official model card detailing the hyperparameters, boundary limits, and evaluation metrics.

---

## 3. How to Run

### Step 1: Generate Preference Data
Compile the 100 Hanoi old quarter preference pairs:
```bash
python bonus/generate_data.py
```

### Step 2: Train DPO Adapter
Run the DPO trainer to align the model weights:
```bash
python bonus/train.py
```

### Step 3: Run Gradio Web UI
Launch the server to chat with the aligned assistant:
```bash
python bonus/demo/serve.py
```
*(Gradio will output a public Share URL so you can also interact with it directly from your phone or Colab).*
