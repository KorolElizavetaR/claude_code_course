
from abc import ABC, abstractmethod
import logging

from client.openrouter_client import OpenRouterChatClient

logger = logging.getLogger(__name__)

prompt = "Please solve the following task: {}"

class IPromptEvaluation(ABC):
    def __init__(self, dataset: list):
        self.prompt = prompt
        self.dataset = dataset
        super().__init__()

    def _get_response(self, test:str) -> str:
        """
        Get the model's response to the prompt.
        """
        finalPrompt: str = self.prompt.format(test)
        client: OpenRouterChatClient = OpenRouterChatClient()
        result: str = client.get_openrouter_text_response(finalPrompt)
        logger.info(f"result: {result}")
        return result

    def evaluate(self, test:str) -> float:
        """
        Evaluate the model's performance based on results from the evaluation.
        """
        # 1. get response from the model
        response: str = self._get_response(test)
        # 2. grade
        # TODO: grading
        score = 10

       # 3. collect results
        return {
            "test": test,
            "output": response,
            "score": score
        }  

    def evaluate_dataset(self) -> list:
        """
        Evaluate the model's performance on the entire dataset.
        """
        results = []
        for test in self.dataset:
            result = self.evaluate(test)
            results.append(result)
        return results             

class LLMEvaluation(IPromptEvaluation):
    pass