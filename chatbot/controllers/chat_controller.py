from ..controllers.restaurant_controller import RestaurantController
from ..services.gpt import GPTManager
from ..models.intent import IntentClassifier


class ChatController:
    def __init__(self, chat_history):
        self.chat_history = chat_history
        self.restaurant_controller = RestaurantController(chat_history)
        self.gpt_manager = GPTManager(chat_history)
        self.intent_classifier = IntentClassifier(self.gpt_manager)

    async def response(self, query):
        self.chat_history.set_role("user")
        self.chat_history.save(query)
        self.chat_history.flush()

        self.chat_history.set_role("assistant")
        intent_json = self.intent_classifier.get_intent_json(query)
        intent_type = intent_json["INTENT_TYPE"]

        if intent_type == "RESTAURANT":
            location = intent_json.get("LOCATION")
            food = intent_json.get("FOOD")
            async for response_part in self.restaurant_controller.find_restaurants(
                location, food
            ):
                yield response_part

        elif intent_type == "REVIEW":
            restaurant = intent_json.get("RESTAURANT")
            location = intent_json.get("LOCATION")
            async for response_part in self.restaurant_controller.find_reviews(
                restaurant, location
            ):
                yield response_part

        elif intent_type == "PARKING":
            restaurant = intent_json.get("RESTAURANT")
            location = intent_json.get("LOCATION")
            async for response_part in self.restaurant_controller.find_parking_info(
                restaurant, location
            ):
                yield response_part

    def run_chat_session(self):
        prompt = """맛집에 대해 질문해보세요!
예시: 강남에 있는 좋은 파스타 식당 추천해주세요
예시: 낙성대 장블랑제리 후기가 궁금해요
예시: 서울대입구 하노이별에 주차가 가능한가요?
>>> """

        additional_prompt = """다른 질문이 있으신가요?
Bye를 입력하면 종료됩니다.
>>> """

        query = input(prompt)
        print()

        # save user's query to chat history
        self.chat_history.set_role("user")
        self.chat_history.save(query)
        self.chat_history.flush()

        while True:
            self.chat_history.set_role("assistant")
            self.response(query)
            self.chat_history.flush()

            print()
            query = input(additional_prompt)
            print()
            if query.lower() == "bye":
                break
            self.chat_history.set_role("user")
            self.chat_history.save(query)
            self.chat_history.flush()
