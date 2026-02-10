# Learning Lab

A collection of learning resources, Jupyter notebooks, and Python scripts for various APIs and platforms. This repository serves as a centralized place for experiments, tutorials, and boilerplate code for different integrations.

## 🚀 Projects Included

### 📱 [LINE Messaging API](./line)
- **Objective**: Learn to interact with the LINE Messaging API.
- **Topics Covered**: Messages, Insights, Audience Management, and User profiles.
- **Resources**: `line_api_learning.ipynb`, `api_doc.md`.

### 📊 [Looker SDK](./looker)
- **Objective**: Explore the Looker Python SDK.
- **Topics Covered**: Retrieving dashboard elements, constructing queries from elements, and executing queries.
- **Resources**: `looker_learning.ipynb`.

### 📈 [Facebook Lead Generation](./facebook/leadgen)
- **Objective**: Tutorial on managing and retrieving Facebook Lead Forms.
- **Topics Covered**: Direct API calls to retrieve lead information.
- **Resources**: `facebook_lead_form_tutorial.ipynb`.

### 📝 [Google Sheets](./googlesheet)
- **Objective**: Automate interactions with Google Sheets.
- **Topics Covered**: Authentication using Service Accounts and basic Read/Write operations.
- **Resources**: `googlesheet_learning.ipynb`.

### 🎯 [CleverTap](./clevertap)
- **Objective**: Master the CleverTap API and SDK.
- **Topics Covered**: User profile management and event tracking.
- **Resources**: `clevertap_learning.ipynb`, `clevertap.py`.

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.9+
- Jupyter Notebook or JupyterLab

### Environment Configuration
Most modules require environment variables. Each module folder contains a `.env.example` file.
1. Navigate to the specific module folder.
2. Copy `.env.example` to `.env`.
3. Fill in the required credentials.

Example:
```bash
cp googlesheet/.env.example googlesheet/.env
```

### Dependency Installation
Since each module has its own dependencies, it is recommended to create a virtual environment for each or install them as needed.

```bash
# Example for LINE API
cd line
pip install -r requirements.txt
```

## 📓 How to Use
1. Open your terminal and navigate to the root of this repository.
2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
3. Navigate to the desired `.ipynb` file and follow the instructions within the notebook.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.