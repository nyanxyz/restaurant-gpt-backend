import json


class ParkingInfoGenerator:
    def __init__(self, gpt_manager):
        self.gpt_manager = gpt_manager

    def generate_parking_info(self, post):
        system_prompt = """
            You will receive a blog post enclosed within triple quotes, which may include information about parking at a specific restaurant.

            Your task is to determine whether parking is available and, if there are any sentences related to parking information, extract them.
            Focus on identifying key details about parking facilities, such as location, capacity, or any special instructions provided in the review.

            Provide output in JSON format as follows:

            {
                "available": "true" or "false" or "unknown",
                "info": {one-sentence, under 30 words} // optional
            }
            """

        return self.gpt_manager.generate(
            system_prompt, post, max_tokens=128, use_history=False
        )

    def get_parking_info_json(self, post):
        count = 0

        while count < 3:
            count += 1
            parking_info_json_str = self.generate_parking_info(post)

            try:
                data = json.loads(parking_info_json_str)
                if data["available"] is None:
                    print("Error: available이 None입니다. (get_parking_info_json)")
                    continue
            except json.JSONDecodeError:
                print("Error: 문자열이 올바른 JSON 형식이 아닙니다. (get_parking_info_json)")
                continue
            else:
                return data
