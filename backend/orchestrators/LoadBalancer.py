import random
import os
import json
from dotenv import load_dotenv

load_dotenv()
class OpenAIContext():
    def __init__(self, resource: str, model: str, endpoint_url: str, key: str, weight: float, version: str):
        # these are the values required to create each endpoint context
        self.resource = resource
        self.model = model
        self.endpoint_url = endpoint_url
        self.key = key
        self.weight = weight
        self.version = version

    def to_dict(self):
            return {
                'resource': self.resource,
                'model': self.model,
                'endpoint_url': self.endpoint_url,
                'key': self.key,
                'weight': self.weight,
                'version': self.version
            }

class LoadBalancer:
    
    def __init__(self):
        open_ai_env_contexts = os.environ.get("AZURE_OPENAI_CONTEXTS")
        open_ai_contexts = json.loads(open_ai_env_contexts)
        api_version = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION")

        # unpack the list of dictionaries into keyword arguments and assigne to an OpenAIContext object
        self.contexts = [OpenAIContext(version=api_version, **context) for context in open_ai_contexts]

    def get_openai_context(self) -> OpenAIContext:
        total_weight = sum(context.weight for context in self.contexts)

        # calculate the relative weight of each endpoint for randomization purposes
        relative_weights = [round(context.weight / total_weight, 2) for context in self.contexts]

        # all weights in order
        all_weights = [round(sum(relative_weights[:i+1]), 2) for i in range(len(relative_weights))]

        for _ in enumerate(self.contexts):
            rand_num = random.random()  # Generates a random float number between 0.0 to 1.0

            for i, cumulative_weight in enumerate(all_weights):
                if rand_num <= cumulative_weight:
                    selected_context_obj = self.contexts[i]
                    selected_context = selected_context_obj.to_dict()
                    return selected_context
