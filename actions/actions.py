from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionProvideSupport(Action):

    def name(self) -> Text:
        return "action_provide_support"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        problem = tracker.get_slot('problem')
        
        if problem:
            response = f"I'm here to help you with your {problem}. Can you tell me more about what's bothering you?"
        else:
            response = "I'm here to help. Can you tell me more about what's bothering you?"

        dispatcher.utter_message(text=response)
        return []

class ActionGiveAdvice(Action):

    def name(self) -> Text:
        return "action_give_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        problem = tracker.get_slot('problem')

        if problem == "work":
            advice = "It's important to take regular breaks, prioritize tasks, and talk to your manager about your workload if it feels overwhelming."
        elif problem == "exams":
            advice = "Make sure to get plenty of rest, organize your study time, and don't hesitate to ask for help if you need it."
        elif problem == "relationships":
            advice = "Communication is key. Try to talk openly with the people involved, and consider seeking the help of a counselor if needed."
        else:
            advice = "It's important to take care of yourself. Make sure to take breaks, get enough sleep, and talk to someone you trust."

        dispatcher.utter_message(text=advice)
        return []

class ActionSetProblemSlot(Action):

    def name(self) -> Text:
        return "action_set_problem_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        problem = next(tracker.get_latest_entity_values("problem"), None)

        if problem:
            return [SlotSet("problem", problem)]
        else:
            return []
