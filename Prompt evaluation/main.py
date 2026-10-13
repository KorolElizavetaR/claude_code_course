import json
import logging
from textwrap import indent

from client.openrouter_client import OpenRouterChatClient
from utils.dataset.Dataset import DatasetGenerator
from utils.eval.Evaluation import IPromptEvaluation, LLMEvaluation

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)

    client: OpenRouterChatClient = OpenRouterChatClient()
    datasetGenerator: DatasetGenerator = DatasetGenerator()
    datasetFilename: str = "dataset.json"
    datasetGenerator.prepare_dataset(client, filename=datasetFilename)

    dataset: list = datasetGenerator.load_dataset_from_file(filename=datasetFilename)
    logger.info(f"Loaded dataset with {len(dataset)} samples from {datasetFilename}")

    evaluator: IPromptEvaluation = LLMEvaluation(dataset=dataset)
    evaluation_results: list = evaluator.evaluate_dataset()

    print("Evaluation Results:")
    for result in evaluation_results:   
        print(json.dumps(result, indent=2))

main() 

# task: str = input(">> ")
# prompt = f"""
# Please provide a solution to the following task:
# {task}
# """

# print(client.chat_response(prompt).choices[0].message.content)
