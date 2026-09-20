import pandas as pd
import torch
import matplotlib.pyplot as plt

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -------------------------------
# LOAD MODEL
# -------------------------------
MODEL_PATH = "./Extension/toxishield_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

# -------------------------------
# LOAD FULL DATASET (NO SPLIT)
# -------------------------------
df = pd.read_csv("./Dataset/finetune_dataset.csv")

df.columns = df.columns.str.strip().str.lower()
df = df[["text", "label"]]

# -------------------------------
# COUNT ACTUAL LABELS
# -------------------------------
actual_neutral = len(df[df["label"] == 0])
actual_toxic = len(df[df["label"] == 1])

# -------------------------------
# MODEL PREDICTIONS
# -------------------------------
pred_neutral = 0
pred_toxic = 0

for _, row in df.iterrows():
    text = row["text"]

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    pred = torch.argmax(probs).item()

    if pred == 0:
        pred_neutral += 1
    else:
        pred_toxic += 1

# -------------------------------
# PRINT RESULTS
# -------------------------------
print("ACTUAL → Neutral:", actual_neutral, "Toxic:", actual_toxic)
print("PREDICTED → Neutral:", pred_neutral, "Toxic:", pred_toxic)

# -------------------------------
# BAR GRAPH
# -------------------------------
labels = ["Neutral", "Toxic"]

actual_counts = [actual_neutral, actual_toxic]
pred_counts = [pred_neutral, pred_toxic]

x = range(len(labels))

plt.figure(figsize=(6,5))

plt.bar([i - 0.2 for i in x], actual_counts, width=0.4, label="Actual")
plt.bar([i + 0.2 for i in x], pred_counts, width=0.4, label="Predicted")

plt.xticks(x, labels)
plt.ylabel("Number of Comments")
plt.title("Actual vs Predicted Toxicity Distribution")

plt.legend()

plt.savefig("dataset_comparison.png", dpi=300, bbox_inches='tight')
plt.show()