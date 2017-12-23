from __future__ import print_function
from twitter import Twitter, OAuth

"""
 Twitter Vars
"""
request_url = 'https://api.twitter.com/1.1/trends/place.json?id=1'
access_key = '717077395-OZhKTbYQPGdD2N5ZrKxsKcQN7spofhmschwLUbk1'
access_secret = 'j0rqs8UB9s7j5wI0Trs5aeKmUoQ80z9dxc8CdwQnVO3uK'
consumer_key = '5DXDPPphnJDplxrUNhIgyMSrZ'
consumer_secret = 'XhE0jiiU3cOZs7v44BQTCbGPvB3OpcT6VLzwn0SpIEqlBAHWfh'
twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

# ------------ Fetch Twitter Trends ---------------

def getTrends(intent, session):
    results = twitter.trends.place(_id = 23424977)
    session_attributes = {}
    reprompt_text = ""
    trends = ['Here is what is trending in the United States.']
    for location in results:
        for trend in location["trends"]:
            trends.append(str(trend["name"].replace('#','')))
    return build_response(session_attributes, build_speechlet_response(
        "USA Trends", str(trends), reprompt_text, True))

# --------------- Helpers that build Response ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# ------------ Welcome Response ---------------

def get_welcome_response():
    welcome = "Just ask Trending Topics what is trending"
    return build_response({}, build_speechlet_response(
        "Trending Topics", welcome, "", True))

# ------------ Handle Intent ---------------

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetTrends":
        return getTrends(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

# --------------- Session Events ------------------

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Trending Topics."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.dc470a40-3aad-41b5-82cb-8b559f977b4a"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])