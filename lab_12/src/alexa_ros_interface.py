#!/usr/bin/env python3
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler, AbstractRequestHandler
from alexa_ros.msg import AlexaTaskAction, AlexaTaskResult, AlexaTaskGoal
import rospy
import actionlib
import threading

threading.Thread(target=lambda: rospy.init_node('alexa_ros_interface', disable_signals=True)).start()
client = actionlib.SimpleActionClient('alexa_task', AlexaTaskAction)

app = Flask(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome Master, How can I help you ?"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Online", speech_text)).set_should_end_session(False)

        goal = AlexaTaskGoal(task_number=0)
        client.send_goal(goal)

        return handler_input.response_builder.response

class PickIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PickIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Affirmative Master I am grabbing the object now!!"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Pick", speech_text)).set_should_end_session(False)

        goal = AlexaTaskGoal(task_number=1)
        client.send_goal(goal)

        return handler_input.response_builder.response

class SleepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SleepIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "okay master I am going to sleep now"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Sleep", speech_text)).set_should_end_session(False)
        
        goal = AlexaTaskGoal(task_number=2)
        client.send_goal(goal)

        return handler_input.response_builder.response

class WakeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("WakeIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Master I am online now, What would like to do now ?"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Wake", speech_text)).set_should_end_session(False)

        goal = AlexaTaskGoal(task_number=3)
        client.send_goal(goal)

        return handler_input.response_builder.response

class ExitIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ExitIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Master I am going to kill myself, Goodbye Have a Nice Day!!!"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Exit", speech_text)).set_should_end_session(True)

        goal = AlexaTaskGoal(task_number=4)
        client.send_goal(goal)

        return handler_input.response_builder.response

class AllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speech = "Master, I am not getting what you are saying to me"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

skill_builder = SkillBuilder()
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(PickIntentHandler())
skill_builder.add_request_handler(SleepIntentHandler())
skill_builder.add_request_handler(WakeIntentHandler())
skill_builder.add_request_handler(ExitIntentHandler())
skill_builder.add_exception_handler(AllExceptionHandler())

skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.9695fcab-1fa0-4e0f-b2ec-f28669141d67", app=app)

skill_adapter.register(app=app, route="/")

if __name__ == '__main__':
    app.run()