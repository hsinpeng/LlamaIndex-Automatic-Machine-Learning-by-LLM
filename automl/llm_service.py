import os, json, re
import yaml
import streamlit as st
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core import PromptTemplate, Settings

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

secret_path = os.path.join(os.path.dirname(__file__), '../', 'secret.yaml')
with open(secret_path, 'r') as file:
    secret = yaml.safe_load(file)

if secret["model_type"] == "openai":
    openai_apikey = secret["openai_apikey"]
    openai_model_name = secret["openai_model_name"]
    llm = OpenAI(model=openai_model_name, api_key=openai_apikey, temperature=0)
elif secret["model_type"] == "azure":
    azure_apikey = secret["azure_apikey"]
    azure_apibase = secret["azure_apibase"]
    azure_apiversion = secret["azure_apiversion"]
    azure_llm_deployment = secret["azure_llm_deployment"]
    llm = AzureOpenAI(
        model="gpt-35-turbo-16k",
        deployment_name=azure_llm_deployment,
        api_key=azure_apikey,
        azure_endpoint=azure_apibase,
        api_version=azure_apiversion,
        temperature=0
    )
elif secret["model_type"] == "ollama":
    ollama_model_name = secret["ollama_model_name"]
    ollama_request_timeout = secret["ollama_request_timeout"]
    llm = Ollama(model=ollama_model_name, request_timeout=ollama_request_timeout, temperature=0)
else:
    st.error('Wrong model_type in secret.yaml!')
    st.stop()

Settings.llm = llm

def llm_execution(query_prompt):
    """
    Using a language model via the Llama-Index SDK.

    Parameters:
    - query_prompt (str): The chat message(query) as the role of human.

    Returns:
    - A JSON object containing the recommended encoding types for the given query_prompt.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        chat_engine = SimpleChatEngine.from_defaults()
        llm_answer = chat_engine.chat(query_prompt)
        if '```json' in str(llm_answer):
            match = re.search(r'```json\n(.*?)```', str(llm_answer), re.DOTALL)
            if match: json_str = match.group(1)
        else: json_str = str(llm_answer)
        return json_str
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_encode_type(attributes, data_frame_head):
    """
    Decides the encoding type for given attributes using a language model via the Llama-Index SDK.

    Parameters:
    - attributes (list): A list of attributes for which to decide the encoding type.
    - data_frame_head (DataFrame): The head of the DataFrame containing the attributes. This parameter is expected to be a representation of the DataFrame (e.g., a string or a small subset of the actual DataFrame) that gives an overview of the data.

    Returns:
    - A JSON object containing the recommended encoding types for the given attributes. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["numeric_attribute_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(attributes=attributes, data_frame_head=data_frame_head)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_fill_null(attributes, types_info, description_info):
    """
    Decides the best encoding type for given attributes using an AI model via Llama-Index SDK.

    Parameters:
    - attributes (list): List of attribute names to consider for encoding.
    - data_frame_head (DataFrame or str): The head of the DataFrame or a string representation, providing context for the encoding decision.

    Returns:
    - dict: A JSON object with recommended encoding types for the attributes. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["null_attribute_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(attributes=attributes, types_info=types_info, description_info=description_info)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_model(shape_info, head_info, nunique_info, description_info):
    """
    Decides the most suitable machine learning model based on dataset characteristics.

    Parameters:
    - shape_info (dict): Information about the shape of the dataset.
    - head_info (str or DataFrame): The head of the dataset or its string representation.
    - nunique_info (dict): Information about the uniqueness of dataset attributes.
    - description_info (str): Descriptive information about the dataset.

    Returns:
    - dict: A JSON object containing the recommended model and configuration. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["decide_model_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(shape_info=shape_info, head_info=head_info, nunique_info=nunique_info, description_info=description_info)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_cluster_model(shape_info, description_info, cluster_info):
    """
    Determines the appropriate clustering model based on dataset characteristics.

    Parameters:
    - shape_info: Information about the dataset shape.
    - description_info: Descriptive statistics or information about the dataset.
    - cluster_info: Additional information relevant to clustering.

    Returns:
    - A JSON object with the recommended clustering model and parameters. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["decide_clustering_model_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(shape_info=shape_info, description_info=description_info, cluster_info=cluster_info)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_regression_model(shape_info, description_info, Y_name):
    """
    Determines the appropriate regression model based on dataset characteristics and the target variable.

    Parameters:
    - shape_info: Information about the dataset shape.
    - description_info: Descriptive statistics or information about the dataset.
    - Y_name: The name of the target variable.

    Returns:
    - A JSON object with the recommended regression model and parameters. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["decide_regression_model_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(shape_info=shape_info, description_info=description_info, Y_name=Y_name)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_target_attribute(attributes, types_info, head_info):
    """
    Determines the target attribute for modeling based on dataset attributes and characteristics.

    Parameters:
    - attributes: A list of dataset attributes.
    - types_info: Information about the data types of the attributes.
    - head_info: A snapshot of the dataset's first few rows.

    Returns:
    - The name of the recommended target attribute. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["decide_target_attribute_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(attributes=attributes, types_info=types_info, head_info=head_info)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)["target"]
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_test_ratio(shape_info):
    """
    Determines the appropriate train-test split ratio based on dataset characteristics.

    Parameters:
    - shape_info: Information about the dataset shape.

    Returns:
    - The recommended train-test split ratio as a float. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["decide_test_ratio_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(shape_info=shape_info)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)["test_ratio"]
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()


def decide_balance(shape_info, description_info, balance_info):
    """
    Determines the appropriate method to balance the dataset based on its characteristics.

    Parameters:
    - shape_info: Information about the dataset shape.
    - description_info: Descriptive statistics or information about the dataset.
    - balance_info: Additional information relevant to dataset balancing.

    Returns:
    - The recommended method to balance the dataset. Please refer to prompt templates in config.py for details.

    Raises:
    - Exception: If unable to access the Llama-Index SDK or another error occurs.
    """
    try:
        template = config["decide_balance_template"]
        prompt_template = PromptTemplate(template=template)
        summary_prompt = prompt_template.format(shape_info=shape_info, description_info=description_info, balance_info=balance_info)

        json_str = llm_execution(summary_prompt)
        return json.loads(json_str)["method"]
    except Exception as e:
        st.error(f'error msg:{e}')
        st.stop()
