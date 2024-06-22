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

class ActionSuggestRelaxation(Action):
    def name(self) -> Text:
        return "action_suggest_relaxation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        relaxation_techniques = [
            "Take a few deep breaths and focus on your breathing.",
            "Try progressive muscle relaxation: tense and then slowly relax each muscle group.",
            "Listen to calming music or nature sounds.",
            "Practice mindfulness or meditation."
        ]
        technique = random.choice(relaxation_techniques)
        dispatcher.utter_message(text=technique)
        return []

class ActionRecommendSelfCare(Action):
    def name(self) -> Text:
        return "action_recommend_self_care"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        self_care_activities = [
            "Take a warm bath.",
            "Read a book you enjoy.",
            "Spend some time in nature.",
            "Write in a journal about your thoughts and feelings."
        ]
        activity = random.choice(self_care_activities)
        dispatcher.utter_message(text=activity)
        return []

class ActionCheckInMood(Action):
    def name(self) -> Text:
        return "action_check_in_mood"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mood_check_questions = [
            "How have you been feeling lately?",
            "Is there anything on your mind you'd like to talk about?",
            "How are you coping with things today?",
            "Is there something specific that's been bothering you?"
        ]
        question = random.choice(mood_check_questions)
        dispatcher.utter_message(text=question)
        return []


class ActionDailyAffirmation(Action):
    def name(self) -> Text:
        return "action_daily_affirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        affirmations = [
            "You are capable and strong.",
            "You are worthy of love and respect.",
            "You can handle whatever comes your way.",
            "Believe in yourself and your abilities."
        ]
        affirmation = random.choice(affirmations)
        dispatcher.utter_message(text=affirmation)
        return []

class ActionSuggestHobby(Action):
    def name(self) -> Text:
        return "action_suggest_hobby"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        hobbies = [
            "Have you considered trying a new hobby like painting or drawing?",
            "Gardening can be very relaxing and rewarding.",
            "Learning a musical instrument could be fun.",
            "How about starting a small DIY project?"
        ]
        hobby = random.choice(hobbies)
        dispatcher.utter_message(text=hobby)
        return []


class ActionSleepTips(Action):
    def name(self) -> Text:
        return "action_sleep_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        sleep_tips = [
            "Stick to a regular sleep schedule, even on weekends.",
            "Create a relaxing bedtime routine, like reading or taking a bath.",
            "Avoid screens (TV, phone, computer) for at least an hour before bed.",
            "Make your sleep environment comfortable and free from distractions."
        ]
        tip = random.choice(sleep_tips)
        dispatcher.utter_message(text=tip)
        return []


class ActionExerciseTips(Action):
    def name(self) -> Text:
        return "action_exercise_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        exercise_tips = [
            "Even a short walk can boost your mood and energy.",
            "Try a quick workout video on YouTube for a guided session.",
            "Stretching exercises can help reduce tension and improve flexibility.",
            "Consider joining a local sports team or fitness class for social interaction and exercise."
        ]
        tip = random.choice(exercise_tips)
        dispatcher.utter_message(text=tip)
        return []


class ActionOfferResources(Action):
    def name(self) -> Text:
        return "action_offer_resources"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        resources = [
            "If you're feeling overwhelmed, consider talking to a therapist.",
            "There are many online resources for mental health support, such as BetterHelp or Talkspace.",
            "Hotlines like the National Suicide Prevention Lifeline (1-800-273-8255) are available 24/7.",
            "Local community centers often offer free or low-cost counseling services."
        ]
        resource = random.choice(resources)
        dispatcher.utter_message(text=resource)
        return []
