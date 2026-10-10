
from pathlib import Path

folders = [
    "data/raw",
    "data/processed",
    "src",
    "training",
    "models",
    "tests",
    "docs",
    "demo",
]

files = [
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".env.example",
    ".gitignore",
    "src/__init__.py",
    "src/email_parser.py",
    "src/feature_extractor.py",
    "src/risk_engine.py",
    "src/url_analyzer.py",
    "src/ml_classifier.py",
    "src/explanation_agent.py",
    "src/pipeline.py",
    "src/schemas.py",
    "training/train_model.py",
    "training/evaluate_model.py",
    "tests/test_parser.py",
    "tests/test_features.py",
    "tests/test_risk_engine.py",
    "tests/test_pipeline.py",
    "tests/test_safety.py",
    "docs/architecture.md",
    "docs/data_dictionary.md",
    "docs/evaluation.md",
    "docs/limitations.md",
    "demo/demo_script.md",
    "data/sample_emails.csv",
    "models/.gitkeep",
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for filename in files:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

Path("requirements.txt").write_text(
    "streamlit\n"
    "pandas\n"
    "numpy\n"
    "scikit-learn\n"
    "tldextract\n"
    "dnspython\n"
    "python-dotenv\n"
    "requests\n"
    "pytest\n"
    "joblib\n"
)

print("Project folders and files created successfully!")