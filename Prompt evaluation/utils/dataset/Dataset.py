import json
import os
import re

from client.openrouter_client import OpenRouterChatClient

class DatasetGenerator:
    _instance = None
    prompt: str = """
            Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.
    
            Example output:
            ```json
            [
            {
                "task": "Description of task",
            },
            ...additional
            ]
            ```
    
            * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
            * Focus on tasks that do not require writing much code
    
            Please generate 3 objects.
            """ 

    def _extract_json_from_llm_response(self, response: str):
        """
        Extracts and parses JSON from an LLM response, handling markdown blocks 
        and common formatting errors like trailing commas.
        """
        # 1. Try to extract JSON from markdown code blocks (```json ... ``` or ``` ... ```)
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
        if match:
            json_str = match.group(1)
        else:
            # 2. Fallback: find the outermost JSON structure if no markdown block is used
            start_idx = next((i for i, c in enumerate(response) if c in '[{'), -1)
            end_idx = next((i for i in range(len(response) - 1, -1, -1) if response[i] in ']}'), -1)
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx + 1]
            else:
                json_str = response

        # 3. Clean up common LLM JSON formatting issues (e.g., trailing commas before closing brackets)
        json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
        
        # 4. Parse the cleaned JSON string into a native Python object
        return json.loads(json_str)
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _generate_dataset(self, client: OpenRouterChatClient):
        """
        Generate a dataset using LLM and extract the JSON from the response.
        """
        dataset: str = client.get_openrouter_text_response(DatasetGenerator.prompt)
        return self._extract_json_from_llm_response(dataset)

    def save_dataset_to_file(self, dataset: list, filename: str = "dataset.json", override: bool = False):
        """
        params:
            dataset: list - The dataset to be saved.
            filename: str - The name of the file to save the dataset to. Default is "dataset.json".
            override: bool - If True, will override the file if it already exists. Default is False.
        """
        if not os.path.exists(filename) or override:
            with open(filename, "w") as f:
                json.dump(dataset, f, indent=2)

    def prepare_dataset(self, client: OpenRouterChatClient, filename: str = "dataset.json", override: bool = False):
        """
        Generate a dataset and save it to a file.
        If the file already exists and override is False, it will not generate a new dataset.
        """
        if not os.path.exists(filename) or override:
            dataset = self._generate_dataset(client)
            self.save_dataset_to_file(dataset, filename, override)

    def load_dataset_from_file(self, filename: str = "dataset.json") -> list:
        """
        Load a dataset from a file.
        """
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
