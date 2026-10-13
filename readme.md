# AI-Powered Email Phishing Detection System

## 1. Project Overview

The **AI-Powered Email Phishing Detection System** is a tool designed to analyze email messages and identify potential phishing attempts, suspicious links, and malicious domains.

The system combines rule-based detection, machine learning classification, URL and domain analysis, and Large Language Model (LLM) explanations to help users understand why an email may be suspicious.

A Streamlit dashboard provides a user-friendly interface where users can paste email content or upload a CSV file for analysis.

### Objectives

* Detect phishing and suspicious emails.
* Compare rule-based and machine learning detection methods.
* Analyze URLs, domains, and email headers where available.
* Explain detection results using evidence-based reasoning.
* Provide actionable recommendations to users.
* Evaluate performance using precision, recall, F1-score, and end-to-end testing.
* Build a reliable, maintainable, and safe application.

## 2. Key Features

* **Email analysis:** Accept pasted email text and uploaded CSV files.
* **Rule-based detection:** Identify suspicious keywords, urgency, requests for credentials, and other warning signs.
* **Machine learning classification:** Predict whether an email is legitimate or phishing.
* **URL and domain analysis:** Extract links and examine suspicious URL patterns and domain indicators.
* **AI-generated explanations:** Summarize the evidence behind a risk assessment.
* **Risk classification:** Categorize emails as low, medium, or high risk.
* **Evidence-based results:** Display the indicators that influenced the decision.
* **Safety checks:** Handle malformed inputs, prompt injection attempts, and unsafe URLs.
* **Model evaluation:** Compare precision, recall, F1-score, and false-positive and false-negative rates.

> Important: The system provides risk assessments, not guaranteed proof that an email is safe or malicious. Users should verify important messages through trusted channels.

## 3. Technology Stack

| Component            | Suggested Technology                 | Purpose                                      |
| -------------------- | ------------------------------------ | -------------------------------------------- |
| Programming language | Python                               | Core development                             |
| Data processing      | pandas, NumPy                        | Dataset preparation and analysis             |
| Machine learning     | scikit-learn                         | Training and evaluating classifiers          |
| Baseline detection   | Python rules and regular expressions | Initial phishing detection                   |
| Email parsing        | Python `email` package               | Extract headers, sender, subject, and body   |
| URL parsing          | `urllib.parse`                       | Extract and inspect URLs                     |
| Domain analysis      | `tldextract` and optional DNS tools  | Examine domain structure and signals         |
| Dashboard            | Streamlit                            | User interface                               |
| Visualization        | Plotly or Matplotlib                 | Evaluation charts and statistics             |
| LLM integration      | An approved LLM API or local model   | Explain evidence and recommendations         |
| Testing              | pytest                               | Unit and integration testing                 |
| Data storage         | CSV and JSON                         | Dataset, predictions, and evaluation results |
| Version control      | Git and GitHub                       | Collaboration and source control             |

**Recommended starting point:** Use Python, pandas, scikit-learn, Streamlit, and pytest. Add external URL intelligence or an LLM API only after the basic detection pipeline works.

## 4. System Architecture

The application follows a modular pipeline:

1. The user pastes an email or uploads a CSV file.
2. The input validator checks the format, size, and required fields.
3. The email parser extracts the sender, subject, body, headers, and URLs.
4. The rule-based detector calculates a baseline result.
5. The machine learning model predicts the likelihood of phishing.
6. The URL and domain analyzer examines available indicators.
7. The decision module combines the model output and evidence according to a documented policy.
8. The explanation component generates a summary from the available evidence.
9. The Streamlit dashboard displays the risk label, evidence, and recommendations.
10. The evaluation module records test results and calculates performance metrics.

### Pipeline diagram

```text
                User Input
                    |
          +---------+---------+
          |                   |
      Paste Email          CSV Upload
          |                   |
          +---------+---------+
                    |
             Input Validation
                    |
              Email Parser
                    |
          +---------+---------+
          |         |         |
        Rules       ML     URL/Domain
          |         |      Analysis
          +---------+---------+
                    |
             Decision Module
                    |
            LLM Explanation
          (Evidence provided)
                    |
              Streamlit UI
                    |
        Risk + Evidence + Advice
                    |
             Evaluation Logs
```

## System Workflow

The AI-powered email phishing detection system processes emails through eight stages, from user input to final evaluation.

### 1. User Input

The user provides an email to the system in one of two ways:

* **Paste Email:** Copy and paste the email text into the application.
* **CSV Upload:** Upload a CSV file containing multiple emails for batch analysis.

### 2. Input Validation

The system checks whether the provided input is valid and usable before processing it.

Validation checks include:

* Verify that the uploaded file uses a supported format.
* Check whether the email content is empty.
* Ensure the input does not exceed the permitted size.
* Validate required CSV columns and data types.
* Handle malformed or invalid input safely.

**Purpose:** To prevent processing errors and ensure that the system receives usable data.

### 3. Email Parser

The email parser extracts and organizes the important parts of an email.

The information may include:

* **Sender Address:** The email address of the sender.
* **Email Subject:** The subject line of the message.
* **Message Body:** The main content of the email.
* **URLs:** Links included in the email.
* **Email Headers:** Additional metadata, when available.

**Purpose:** To organize email information so that the detection components can examine different phishing indicators.

### 4. Three Analysis Methods

The system analyzes the email using three complementary methods.

#### 4.1 Rule-Based Detection

The rule-based detector checks for predefined phishing indicators, such as:

* Urgent or threatening language.
* Requests for passwords or sensitive information.
* Suspicious links.
* Unusual sender information.
* Messages that pressure users into taking immediate action.

**Purpose:** To identify known warning signs using predefined rules.

#### 4.2 Machine Learning (ML) Classification

The machine learning model analyzes patterns learned from previously labeled legitimate and phishing emails.

It uses these patterns to predict whether a new email is likely to be phishing.

**Purpose:** To detect patterns that may not be fully covered by predefined rules.

#### 4.3 URL and Domain Analysis

The URL and domain analyzer examines links found in the email.

It may check for:

* Unusual URL structures.
* IP addresses used instead of familiar domain names.
* Suspicious subdomains.
* Misspelled or misleading domain names.
* Other available indicators of potentially malicious links.

**Purpose:** To identify suspicious links and domains that may lead users to fraudulent websites.

### 5. Decision Module

The decision module combines the findings from rule-based detection, machine learning classification, and URL/domain analysis.

Based on the project's decision policy, the system assigns a risk category, such as:

* **Low Risk:** Few suspicious indicators were identified.
* **Medium Risk:** Some suspicious indicators require further investigation.
* **High Risk:** Multiple or significant phishing indicators were identified.

**Purpose:** To produce a consistent risk assessment using the available evidence.

The decision module should account for conflicting signals and incomplete information. A low-risk result does not guarantee that an email is safe.

### 6. LLM Explanation

The Large Language Model (LLM) converts the detection findings into a clear, human-readable explanation.

For example:

> This email may be a phishing attempt because it uses urgent language, requests account verification, and contains a suspicious link.

The explanation component should:

* Summarize the evidence identified by the detection system.
* Explain why the email received its risk classification.
* Provide practical recommendations to the user.
* Avoid inventing evidence or making unsupported claims.

**Purpose:** To help users understand the detection results instead of displaying only a risk label or score.

The LLM explains the available evidence; it should not independently override the detection decision.

### 7. Streamlit User Interface (UI)

The Streamlit dashboard provides the interface through which users interact with the system.

The dashboard displays:

* The final risk classification.
* The risk score, if available.
* Suspicious indicators identified during analysis.
* The LLM-generated explanation.
* Recommended next steps.
* Error messages when an email cannot be processed.

The interface supports both individual email analysis and CSV-based batch analysis.

**Purpose:** To present the detection results in a simple, understandable, and user-friendly format.

### 8. Evaluation Logs

The evaluation component records information needed to measure the system's performance and reliability.

Evaluation may include:

* Number of emails analyzed.
* Correctly detected phishing emails.
* Correctly identified legitimate emails.
* False positives: legitimate emails incorrectly classified as phishing.
* False negatives: phishing emails incorrectly classified as legitimate.
* Precision, recall, and F1-score.
* Processing errors and failed test cases.
* Results of malformed-input and prompt-injection tests.

**Purpose:** To determine how accurately and reliably the system detects phishing emails and identify areas for improvement.

Evaluation logs should avoid storing sensitive email content or personal information unnecessarily.

---

## Workflow Summary

The complete process follows this sequence:

1. **User Input:** The user pastes an email or uploads a CSV file.
2. **Input Validation:** The system validates the input.
3. **Email Parser:** The email is separated into structured components.
4. **Analysis:** Rules, machine learning, and URL/domain analysis examine the email.
5. **Decision Module:** The findings are combined to determine the risk category.
6. **LLM Explanation:** The system generates an evidence-based explanation.
7. **Streamlit UI:** The risk assessment and recommendations are displayed.
8. **Evaluation Logs:** Performance and reliability information is recorded.

### Expected Outcome

The final system provides users with an email risk assessment, supporting evidence, a plain-language explanation, and recommended actions. The evaluation process helps the development team measure performance and improve the system over time.


The LLM should explain the evidence rather than independently override the detector's decision.

## 5. Team Responsibilities

### Student 1 — Data Lead

**Ownership:** Dataset preparation, labeling, schema, and data quality.

Responsibilities:

* Collect or generate legitimate and phishing email examples.
* Label and validate the dataset.
* Document dataset sources, licenses, and usage restrictions.
* Provide consistent sample inputs for the development team.
* Coordinate data quality checks.
* Check for duplicate records, missing values, and label inconsistencies.
* Prevent data leakage between training, validation, and test sets.

Deliverables:

* `data/` directory structure and dataset documentation.
* Data schema and labeling guidelines.
* Validated training, validation, and test datasets.
* Data quality report.
* Representative sample emails for testing.

### Student 2 — AI Lead

**Ownership:** Detection algorithms and machine learning evaluation.

Responsibilities:

* Implement the rule-based baseline.
* Train a machine learning phishing classifier.
* Compare precision, recall, and F1-score.
* Tune decision thresholds using validation data.
* Document false positives and false negatives.
* Save the trained model and preprocessing pipeline.
* Compare the ML model against the rule-based baseline.

Deliverables:

* Rule-based detector.
* Trained model and preprocessing artifacts.
* Model evaluation report.
* Confusion matrix and performance metrics.
* Documented model limitations and threshold selection.

### Student 3 — Agent Lead

**Ownership:** Email parsing, investigation orchestration, and explanations.

Responsibilities:

* Implement the email parser.
* Build the investigation pipeline.
* Integrate URL and domain analysis.
* Connect the LLM explanation component.
* Validate structured outputs and safe tool use.
* Handle missing headers, malformed messages, and invalid URLs.
* Ensure email content is treated as untrusted input.

Deliverables:

* Email parsing module.
* Investigation orchestrator.
* URL and domain analysis module.
* Structured explanation interface.
* Input and output validation tests.

### Student 4 — App Lead

**Ownership:** User interface and application integration.

Responsibilities:

* Build the Streamlit dashboard.
* Implement paste-email and CSV-upload functionality.
* Display risk labels, evidence, and recommendations.
* Integrate the detection and investigation pipeline.
* Maintain the application setup instructions.
* Display useful error messages and loading states.
* Ensure results are understandable and accessible.

Deliverables:

* Working Streamlit application.
* Single-email analysis interface.
* CSV batch-analysis interface.
* Results and evidence display.
* Installation and launch instructions.

### Student 5 — Evaluation Lead

**Ownership:** Testing, safety, reliability, and final documentation.

Responsibilities:

* Create evaluation test cases.
* Test malformed inputs and prompt injection.
* Review evidence quality and explanations.
* Measure end-to-end reliability.
* Prepare the final report, screenshots, and demo script.
* Verify that all team modules work together.
* Document limitations, ethical considerations, and future improvements.

Deliverables:

* Test plan and test cases.
* Unit and integration test results.
* Safety and robustness report.
* Final project report.
* Demo script and screenshots.
* End-to-end evaluation summary.

## 6. Suggested Project Structure

```text
email-phishing-detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── samples/
│   └── README.md
│
├── models/
│   ├── .gitkeep
│   └── README.md
│
├── src/
│   ├── __init__.py
│   ├── email_parser.py
│   ├── data_preprocessing.py
│   ├── rule_detector.py
│   ├── ml_classifier.py
│   ├── url_analyzer.py
│   ├── domain_analyzer.py
│   ├── investigation_pipeline.py
│   ├── explanation.py
│   └── decision_engine.py
│
├── evaluation/
│   ├── evaluate_model.py
│   ├── evaluate_pipeline.py
│   └── results/
│
├── tests/
│   ├── test_parser.py
│   ├── test_rules.py
│   ├── test_classifier.py
│   ├── test_url_analyzer.py
│   ├── test_pipeline.py
│   ├── test_security.py
│   └── test_app.py
│
├── docs/
│   ├── architecture.md
│   ├── dataset.md
│   ├── evaluation.md
│   ├── security.md
│   └── demo_script.md
│
└── reports/
    └── screenshots/
```

The team can adjust this structure as the implementation evolves. Large datasets, trained models, secrets, and private email samples should not be committed to GitHub.

## 7. Dataset and Schema

Each dataset record should have a consistent format.

| Field      | Type                      | Description                         |
| ---------- | ------------------------- | ----------------------------------- |
| `email_id` | String                    | Unique record identifier            |
| `sender`   | String                    | Sender address, if available        |
| `subject`  | String                    | Email subject                       |
| `body`     | String                    | Email message body                  |
| `urls`     | List or serialized string | Extracted URLs                      |
| `label`    | Integer                   | `0` = legitimate, `1` = phishing    |
| `source`   | String                    | Dataset source or generation method |

Optional fields include `headers`, `received_date`, `language`, and `notes`.

### Data preparation guidelines

1. Use reputable, appropriately licensed datasets.
2. Record the source and license for every dataset.
3. Remove duplicates and handle missing fields consistently.
4. Normalize labels to one agreed convention.
5. Remove personal information when possible.
6. Split data into training, validation, and test sets before model tuning.
7. Avoid placing near-duplicate emails in different splits.
8. Keep the test set separate until final evaluation.
9. Use synthetic emails only as clearly documented supplementary data.
10. Ensure all team members use the same schema and label definitions.

Do not publish confidential messages, credentials, private sender information, or unlicensed datasets.

## 8. Implementation Plan

### Phase 1 — Requirements and setup

* Agree on the scope and minimum viable product.
* Finalize the dataset schema and label convention.
* Create the GitHub repository.
* Create the project folders.
* Set up a Python virtual environment.
* Install shared dependencies.
* Assign module owners and agree on function interfaces.

### Phase 2 — Dataset preparation

Student 1 leads this phase.

* Collect or generate labeled email examples.
* Validate the data.
* Remove duplicates and inspect class balance.
* Create training, validation, and test splits.
* Publish sample inputs and the dataset documentation.

### Phase 3 — Baseline and machine learning

Student 2 leads this phase.

* Build an initial rule-based detector.
* Establish baseline performance.
* Convert email text into numerical features using methods such as TF-IDF.
* Train a classifier such as Logistic Regression.
* Evaluate the classifier on validation data.
* Tune thresholds and document trade-offs.

Start with a simple, explainable model before experimenting with more complex algorithms.

### Phase 4 — Parsing and investigation

Student 3 leads this phase.

* Parse email headers, subject, and body.
* Extract URLs and inspect suspicious patterns.
* Implement the investigation pipeline.
* Define a consistent output schema.
* Connect the explanation component.
* Test malformed inputs and untrusted email content.

### Phase 5 — Dashboard and integration

Student 4 leads this phase.

* Build the Streamlit interface.
* Add email text input.
* Add CSV upload and batch processing.
* Display the risk label, evidence, and recommendations.
* Connect the interface to the pipeline.
* Handle errors and loading states.

### Phase 6 — Evaluation and security

Student 5 leads this phase.

* Write unit and integration tests.
* Evaluate precision, recall, F1-score, and confusion matrix.
* Test benign emails that look suspicious.
* Test phishing emails with few obvious indicators.
* Test malformed files, oversized input, and prompt injection.
* Verify that explanations do not invent evidence.
* Record limitations and end-to-end results.

### Phase 7 — Final delivery

All students contribute.

* Review the README and installation instructions.
* Run the project from a clean environment.
* Confirm that all modules work together.
* Capture screenshots of the working dashboard.
* Prepare the presentation and demo script.
* Submit the report, code, test results, and required documentation.

## 9. Installation and Setup

### Prerequisites

* Python 3.10 or a compatible version supported by the selected dependencies.
* Git.
* A code editor such as Visual Studio Code.
* Internet access if installing packages or using external APIs.

### Step 1: Clone the repository

```bash
git clone https://github.com/KaushalDhakal0/Phishing-and-BEC-Defense.git
cd Phishing-and-BEC-Defense
code .
```

Replace the placeholder with the actual repository URL.

### Step 2: Create a virtual environment

Windows:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```


### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip 
pip install -r requirements.txt
```

### Step 5: Prepare the data and model

Follow the dataset preparation and model training scripts documented by the team. Save trained artifacts in the expected model directory.

The application should provide a clear error message if the model or required dataset is missing.

### Step 6: Launch the dashboard

```bash
python create_dataset.py
streamlit run app.py
```

Open the local URL displayed in the terminal.

**Note:** The exact training commands depend on the scripts implemented by the team. Add the final commands to this section once those scripts are available.

## 10. Evaluation Metrics

The project should compare the rule-based baseline with the trained classifier.

| Metric           | Meaning                                                                        |
| ---------------- | ------------------------------------------------------------------------------ |
| Accuracy         | Fraction of all predictions that are correct                                   |
| Precision        | Fraction of predicted phishing emails that are actually phishing               |
| Recall           | Fraction of phishing emails successfully detected                              |
| F1-score         | Harmonic mean of precision and recall                                          |
| Confusion matrix | Counts of true positives, true negatives, false positives, and false negatives |

For phishing detection, recall is important because missed phishing emails can be dangerous. Precision is also important because excessive false alarms can make users ignore warnings.

Use validation data for threshold selection and reserve the test set for final evaluation. Report actual measured values rather than estimated or invented results.

## 11. Security and Responsible Use

* Treat email text, headers, and attachments as untrusted input.
* Never execute links, attachments, or embedded code during analysis.
* Do not automatically visit suspicious URLs without appropriate isolation and safeguards.
* Treat email instructions as data, not as instructions for the LLM or application.
* Validate LLM responses against a predefined structured schema.
* Do not allow the LLM to independently execute tools or change the detection result.
* Limit file size, row count, and accepted input formats.
* Avoid storing raw email content unnecessarily.
* Protect API keys and redact sensitive information from logs.
* Clearly distinguish observed evidence from model-generated explanations.
* Do not claim a message is safe solely because no suspicious indicators were found.

The application should provide an uncertainty-aware result when evidence is incomplete or contradictory.


## 13. Definition of Done

The project is ready for submission when:

* [ ] The dataset is labeled, validated, and documented.
* [ ] The rule-based baseline works.
* [ ] The ML classifier is trained and evaluated.
* [ ] Precision, recall, F1-score, and confusion matrix are reported.
* [ ] The email parser handles missing and malformed fields.
* [ ] URL and domain indicators are integrated.
* [ ] The explanation component produces validated structured output.
* [ ] The Streamlit dashboard supports pasted emails and CSV uploads.
* [ ] The end-to-end pipeline works on representative examples.
* [ ] Prompt injection and malformed input tests are documented.
* [ ] Installation instructions work in a clean environment.
* [ ] Screenshots, the final report, and demo script are prepared.
* [ ] All external data sources and licenses are documented.

## 14. Future Improvements

Potential future extensions include:

* Better handling of HTML emails and email authentication headers.
* Integration with trusted threat-intelligence feeds.
* Multilingual phishing detection.
* Model calibration and confidence analysis.
* Improved explainability and analyst feedback.
* Privacy-preserving evaluation.
* Deployment to a secure cloud environment.
* Monitoring model performance as phishing patterns change.

## 15. Team Members

| Role      | Name           | Main Responsibility          |
| --------- | -------------- | ---------------------------- |
| Student 1 | To be assigned | Dataset and schema           |
| Student 2 | To be assigned | Detection and ML             |
| Student 3 | To be assigned | Parsing and orchestration    |
| Student 4 | To be assigned | Dashboard and integration    |
| Student 5 | To be assigned | Evaluation and documentation |

## 16. Conclusion

This project combines rule-based detection, machine learning, URL and domain analysis, and evidence-based AI explanations in a single email phishing analysis application.

By separating responsibilities across five team members and defining shared interfaces, evaluation standards, and safety requirements, the team can develop the application incrementally and deliver a reproducible, testable university project.

**Project status:** Initial project plan. Update this README as the implementation, dataset, model results, and interface are completed.
