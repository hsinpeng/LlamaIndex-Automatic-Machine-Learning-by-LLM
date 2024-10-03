# LlamaIndex: Naïve Automatic Machine Learning by LLM
This application leverages OpenAI's language models and LlamaIndex's agents and tools to provide users with automatic machine learning and data visualization of the upload file. 

![application homepage](./homepage.png)

## Python Libraries
This application is powered by several libraries:
- [Streamlit](https://streamlit.io/): For the User Interface 🖥️
- [scikit-learn](https://scikit-learn.org/stable/): For performing machine learning tasks 🧑‍💻
- [XGBoost](https://xgboost.ai/): The regularizing gradient boosting framework 🛠️
- [statsmodels](https://www.statsmodels.org/stable/index.html): For performing statistical tests and data exploration 📉
- [seaborn](https://seaborn.pydata.org/): For performing statistical data visualization 📊
- [LlamaIndex](https://www.llamaindex.ai/): For creating LLMs agents and tools 🔗
- [OpenAI](https://openai.com/): The Large Language Models (LLM) provider 🧠


# Getting started 🏁

## Requirements

The [Python Runtime Environment](https://www.python.org/) should be installed on your computer.
Please choose the latest version of Python 3. The tested Python version is 3.10.12 on Ubuntu 22.04.5 LTS.


## Installation

Clone the repository and install the dependencies:

```bash
git clone [this repository]
cd LlamaIndex-Automatic-Machine-Learning-by-LLML
python3 -m pip install -r requirements.txt
```

Rename "secret_template.yaml" to "secret.yaml" and edit it for the proper LLM settings:
```yaml
model_type: "openai" # "openai" or "azure" or "ollama"
# OpenAI
openai_apikey: ""
openai_model_name: ""
# Azure OpenAI
azure_apikey: ""
azure_apibase: ""
azure_apiversion: ""
azure_llm_deployment: ""
# Ollama
ollama_model_name: ""
ollama_request_timeout: 120
ollama_base_url: "http://localhost:11434"
# Others
```

Nate: The application supports OpenAI, AzureOpenAI and local Ollama LLM providers only. 😅

## Run the application

```bash
streamlit run app.py
```
 
# Usage 📖

Thanks to the graphical user interface, the usage of this application is pretty tuitive. 🤓

1. Upload your data file. We only support CSV, XLS, XLSX, XLSM, and XLSB file types with 200MB size limitation. 📂
2. Select a proper analysis mode. Default mode is AutoML, LLM agent will decide which mode works best for your data. ❓
3. Click the "Start Analysis" button. The LLM agent will perform data analysis first by tool calling. 💡
4. After reviewing the analysis report, then Click the "Start Training Model" button. The LLM agent will perform machine learning tasks by tool calling. 🖥️
5. Top 3 best models and their evaluation reports will be displayed right after ML tasks are finished. You can download the preferred model for later use. 📥

Note: If you don't have a suitable data file. [Sample datasets](https://github.com/hsinpeng/sample_datasets.git) are provided on my github as well.


# Features ✨
- Natural language interface for performing data visualization and machine learning by LLM agent and tools. 📊
- Support variouse analysis modes(classification, regression and clustering), models and file types fo dataset. 📄
- Implementation of LlamaIndex. (Note that most of the related projects are developed by LangChain) 👍


# Limitations ⚠️
- Cannot deal with non-tabular data, or extract tabular data from unsupported file types. 💔
- Cannot deal with large datasets since the LLM has its token limitation. 🚫
- The data is not cached, including final models and analysis reports as well. 🔄


# Improvements 🚀
- Voice interface: Convert user's speech to text and perform a machine learning task 🗣️
- Third-party's data sources: Integrating internal and external data without file uploading 🤝
- Data understanding: Isolating features of data profiling from existing analysis modes 📚
- Perform intermediates checkings on the results to avoid LLM bias 🤔


# Background 🧑‍🎓
My name is [Sheldon Hsin-Peng Lin](https://www.linkedin.com/in/sheldon-hsin-peng-lin-51306685/). I'm a software engineer and a research staff. I build various applications in telecommunication industry. 👨‍🔧
Since LLMs are really good at understanding human semantics, and an agent can perform machine learning tasks automatically by LLM reasoning and tool calling. 📚
This application is developed based on the above conditions, and I hope it can help you as well. 👍


# Acknowledgements 🙏
The application is greatly inspired by [Streamline Analyst](https://github.com/Wilson-ZheLin/Streamline-Analyst.git) which implemented by LangChain. ❤️