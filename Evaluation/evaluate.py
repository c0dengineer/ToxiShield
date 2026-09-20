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

# CONFUSION MATRIX COUNTERS
TP = 0
TN = 0
FP = 0
FN = 0

for _, row in df.iterrows():
    text = row["text"]
    actual = row["label"]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    pred = torch.argmax(probs).item()

    # Count predicted totals
    if pred == 0:
        pred_neutral += 1
    else:
        pred_toxic += 1

    # Confusion matrix logic
    if actual == 1 and pred == 1:
        TP += 1
    elif actual == 0 and pred == 0:
        TN += 1
    elif actual == 0 and pred == 1:
        FP += 1
    elif actual == 1 and pred == 0:
        FN += 1

# -------------------------------
# PRINT RESULTS
# -------------------------------
print("ACTUAL:- \nNeutral:", actual_neutral, "\nToxic:", actual_toxic)
print("\nPREDICTED:- \nNeutral:", pred_neutral, "\nToxic:", pred_toxic)

print("\nCONFUSION MATRIX:")
print("TP (Toxic correctly detected):", TP)
print("TN (Neutral correctly detected):", TN)
print("FP (False Positive - Neutral → Toxic):", FP)
print("FN (False Negative - Toxic → Neutral):", FN)

# -------------------------------
# GRAPH 1: ACTUAL vs PREDICTED
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

# -------------------------------
# GRAPH 2: ERROR COUNTS (FP vs FN)
# -------------------------------
error_labels = ["False Positive", "False Negative"]
error_counts = [FP, FN]

plt.figure(figsize=(5,4))
plt.bar(error_labels, error_counts)

plt.ylabel("Number of Comments")
plt.title("Model Errors: False Positives vs False Negatives")

for i, v in enumerate(error_counts):
    plt.text(i, v + 1, str(v), ha='center')

plt.savefig("error_analysis.png", dpi=300, bbox_inches='tight')
plt.show()

# -------------------------------
# GRAPH 3: NORMALIZED ERROR RATES (IMPORTANT)
# -------------------------------

# Avoid division by zero
fp_rate = (FP / actual_neutral) * 100 if actual_neutral > 0 else 0
fn_rate = (FN / actual_toxic) * 100 if actual_toxic > 0 else 0

rate_labels = [
    "FP Rate\n(Neutral → Toxic)",
    "FN Rate\n(Toxic → Neutral)"
]

rates = [fp_rate, fn_rate]

plt.figure(figsize=(6,4))
bars = plt.bar(rate_labels, rates)

plt.ylabel("Percentage (%)")
plt.title("Normalized Error Rates (Model Bias Insight)")

# Show percentage values
for i, v in enumerate(rates):
    plt.text(i, v + 0.5, f"{v:.2f}%", ha='center')

plt.ylim(0, 100)

plt.savefig("normalized_error_rates.png", dpi=300, bbox_inches='tight')
plt.show()