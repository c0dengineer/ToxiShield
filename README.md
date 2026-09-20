# ToxiShield

ToxiShield is an AI-powered multilingual cyberbullying detection browser extension. It analyzes comments on supported social media platforms, blurs comments classified as toxic, and lets users reveal or hide the detected content.

The project also includes an optional local Flask dashboard for reviewing comments detected while the dashboard is running.

## Features

- Real-time toxic comment detection
- Multilingual text classification through a hosted Hugging Face inference service
- Automatic blurring of toxic comments
- View/hide control for blurred comments
- Toxicity percentage and severity display
- Optional local admin dashboard
- Toxic and neutral comment filtering
- CSV export and comment deletion
- Support for Instagram, X/Twitter, and YouTube comment pages

## Architecture

1. The Chrome extension scans comment text on supported social media pages.
2. The extension sends the text to the hosted ToxiShield prediction API.
3. Toxic comments are blurred and annotated with the returned toxicity information.
4. When the local dashboard is running, the extension also sends detected comments to the local Flask server for storage.

The dashboard is optional. Detection continues to use the hosted API when the local dashboard is unavailable, but comments are not stored locally.

## Project Structure

```text
ToxiShield/
|-- Dataset/
|   `-- finetune_dataset.csv
|-- Docs/
|-- Evaluation/
|   `-- evaluate.py
|-- Extension/
|   |-- admin/
|   |   |-- admin_app.py
|   |   |-- create_db.py
|   |   `-- templates/
|   |-- content.js
|   |-- manifest.json
|   |-- train.py
|   `-- toxishield_model/
`-- README.md
```

## Requirements

- Python 3.10 or later
- Google Chrome
- Internet access for Hugging Face inference

## Local Dashboard Setup

Create and activate a virtual environment from the repository root:

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dashboard dependencies:

```bash
pip install flask flask-cors
```

Create the SQLite database and start the dashboard:

```bash
cd Extension/admin
python create_db.py
python admin_app.py
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001) in a browser. The dashboard is intended for local administrative use only.

> The current dashboard implementation uses the local credentials `admin` and `1234`. Change these credentials and the Flask secret key before using the dashboard beyond local development.

## Browser Extension Setup

1. Open Google Chrome.
2. Visit `chrome://extensions/`.
3. Enable **Developer mode**.
4. Select **Load unpacked**.
5. Choose the repository's `Extension` directory.

The extension is configured for Instagram, Twitter/X, and YouTube pages. Visit a supported page to begin scanning comments.

## AI Model and API

The extension currently uses these hosted Hugging Face resources:

- Model repository: <https://huggingface.co/VishakhaST/toxishield_model>
- Inference Space: <https://huggingface.co/spaces/VishakhaST/toxishield1>
- Prediction endpoint: `https://vishakhast-toxishield1.hf.space/api/predict`

The prediction service returns a label and, for toxic comments, toxicity percentage and severity information.

## Dataset

The included dataset was independently created and annotated by the project team for academic and research purposes. Its label taxonomy was informed by publicly available toxic-language classification research, including the Jigsaw Toxic Comment Classification challenge, but the samples and annotations are not copied from or derived from that dataset.

## Training and Evaluation

Training and evaluation scripts are included in `Extension/train.py` and `Evaluation/evaluate.py`. Model training may require additional machine-learning dependencies such as PyTorch and Hugging Face Transformers; install versions appropriate for your Python environment before running those scripts.

## Privacy and Limitations

- Comment text is sent to the hosted inference API for classification.
- The local dashboard stores detected comments in `Extension/admin/database.db` when it is running.
- The dashboard is not configured for public deployment.
- Detection depends on the availability of the hosted inference service and internet access.

## Acknowledgements

ToxiShield was developed for academic purposes and uses Hugging Face Transformers, PyTorch, Flask, Flask-CORS, SQLite, and Chrome Extension APIs.

## Team

- Sania Musliar
- Vishakha Talele
- Navya Roshni
- Tanaya Deshmukh

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.