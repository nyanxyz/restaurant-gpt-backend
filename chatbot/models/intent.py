from ..services.gpt import GPTManager
import json


class IntentClassifier:
    def __init__(self, gpt_manager):
        self.gpt_manager = gpt_manager

    def classify_intent(self, query):
        system_prompt = """
        You will be provided with user's query about a restaurant.
        Classify each query into a category and extract the values.

        The categories and values to extract are:
        - INTENT_TYPE: RESTAURANT
            - The user wants to know about good restaurants. (ex: 강남 맛집, 파스타 식당)
            - VALUE: LOCATION > location of the restaurant (ex: 강남)
            - VALUE: FOOD > food that the restaurant serves (ex: 파스타)
        - INTENT_TYPE: REVIEW
            - The user wants to know about reviews of a specific restaurant. (ex: 브레드 앤 브루어스 후기)
            - VALUE: RESTAURANT > name of the restaurant (ex: 브레드 앤 브루어스)
            - VALUE: LOCATION > location of the restaurant (ex: 강남)
        - INTENT_TYPE: PARKING
            - The user wants to know about parking information of a specific restaurant. (ex: 브레드 앤 브루어스 주차장)
            - VALUE: RESTAURANT > name of the restaurant (ex: 브레드 앤 브루어스)
            - VALUE: LOCATION > location of the restaurant (ex: 강남)
        - INTENT_TYPE: NONE
            - 

        Provide output in JSON format as follows:

        {
            "INTENT_TYPE": {category},
            "LOCATION": {location}, // optional
            "FOOD": {food}, // optional
            "RESTAURANT": {restaurant} // optional
        }
        """

        return self.gpt_manager.generate(system_prompt, query)

    def get_intent_json(self, query):
        count = 0

        while count < 3:
            count += 1
            intent_json_str = self.classify_intent(query)

            try:
                data = json.loads(intent_json_str)
                if data["INTENT_TYPE"] is None:
                    print("Error: INTENT_TYPE이 None입니다. (get_intent_json)")
                    continue
            except json.JSONDecodeError:
                print(intent_json_str)
                print("Error: 문자열이 올바른 JSON 형식이 아닙니다. (get_intent_json)")
                continue
            else:
                return data
