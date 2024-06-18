from typing import Any, Text, Dict, List
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Action to set the problem slot based on user input
class ActionSetProblemSlot(Action):
    def name(self) -> Text:
        return "action_set_problem_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        problem = next(tracker.get_latest_entity_values("problem"), None)
        if problem:
            return [SlotSet("problem", problem)]
        return []

# Action to provide support based on the identified problem
class ActionProvideSupport(Action):
    def name(self) -> Text:
        return "action_provide_support"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        problem = tracker.get_slot("problem")
        if problem:
            dispatcher.utter_message(text=f"I'm sorry to hear that you're stressed about {problem}. Can I help with some advice?")
        else:
            dispatcher.utter_message(text="I'm here to help. What seems to be the problem?")
        return []

# Action to give general advice
class ActionGiveAdvice(Action):
    def name(self) -> Text:
        return "action_give_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Generic advice examples
        advice_list = [
            "It's important to take regular breaks and stay positive.",
            "Talking to friends or a counselor might help.",
            "Exercise and a healthy diet can improve your mental health.",
            "Try to keep a balanced schedule and prioritize your tasks."
        ]
        advice = random.choice(advice_list)
        dispatcher.utter_message(text=advice)
        return []

# Action to provide motivational quotes
class ActionProvideMotivation(Action):
    def name(self) -> Text:
        return "action_provide_motivation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Motivational quotes
        motivation_list = [
            "“The only way to do great work is to love what you do.” – Steve Jobs",
            "“Don’t watch the clock; do what it does. Keep going.” – Sam Levenson",
            "“You are never too old to set another goal or to dream a new dream.” – C.S. Lewis",
            "“Success is not the key to happiness. Happiness is the key to success.” – Albert Schweitzer"
        ]
        motivation = random.choice(motivation_list)
        dispatcher.utter_message(text=motivation)
        return []

# Action to tell a joke
class ActionTellJoke(Action):
    def name(self) -> Text:
        return "action_tell_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Jokes
        jokes_list = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
            "Why don’t skeletons fight each other? They don’t have the guts."
        ]
        joke = random.choice(jokes_list)
        dispatcher.utter_message(text=joke)
        return []

# Action to provide fun facts
class ActionFunFact(Action):
    def name(self) -> Text:
        return "action_fun_fact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Fun facts
        fun_facts = [
            "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!",
            "Bananas are berries, but strawberries aren’t!",
            "A single strand of spaghetti is called a spaghetto.",
            "Octopuses have three hearts."
        ]
        fact = random.choice(fun_facts)
        dispatcher.utter_message(text=fact)
        return []
