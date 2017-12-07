from __future__ import print_function
from urllib2 import Request, urlopen, URLError
import json


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

# function to  return number in ordinal format by adding st, nd, rd, and th to numbers
def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def Coin(name):
    request = Request('https://api.coinmarketcap.com/v1/ticker/' + name)
    try:
        response = urlopen(request)
        data = json.load(response)
        return data

    except URLError, e:
        return


# change the numbers inputted to text
def numberToWords(num):
    to19 = 'One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve ' \
           'Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen'.split()
    tens = 'Twenty Thirty Forty Fifty Sixty Seventy Eighty Ninety'.split()
    def words(n):
        if n < 20:
            return to19[n-1:n]
        if n < 100:
            return [tens[n/10-2]] + words(n%10)
        if n < 1000:
            return [to19[n/100-1]] + ['Hundred'] + words(n%100)
        for p, w in enumerate(('Thousand', 'Million', 'Billion'), 1):
            if n < 1000**(p+1):
                return words(n/1000**p) + [w] + words(n%1000**p)
    return ' '.join(words(num)) or 'Zero'


def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to my cryptocurrency app. Start off by saying a command like: what is the marketcap of bitcoin"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I didn't get that, please try again"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying out my app. " \
                    "Bye!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_current_currency_attributes(current_currency):
    return {"currentCurrency": current_currency}

def rank(data):
    currency = data
    data = Coin(data)[0]
    return str(currency + " is currently the "+ord(int(data["rank"])) + " ranked currency on the market.")

def set_rank_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'currencyName' in intent['slots']:
        current_currency = intent['slots']['currencyName']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = rank(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me about any coins by stating your questoin and the coin followed after it. "
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def price_usd(data):
    currency = data
    data = Coin(data)[0]
    return "The price of "+currency + " in US dollars is "+ numberToWords(int(data["price_usd"].split(".")[0])) + " dollars."
def set_priceUSD_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'usdPrice' in intent['slots']:
        current_currency = intent['slots']['usdPrice']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = price_usd(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can also ask me for volume, marketcap, and percent change, by saying" \
                        "what is the marketcap for and the coin you want?"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def market_cap_usd(data):
    currency = data
    data = Coin(data)[0]
    return "The market cap for "+currency+" is "+ numberToWords(int(data["24h_volume_usd"].split(".")[0]))+ " dollars."
def set_MarketCap_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'marketcap' in intent['slots']:
        current_currency = intent['slots']['marketcap']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = market_cap_usd(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def h24_volume_usd(data):
    currency = data
    data = Coin(data)[0]
    return "The market 24 hour volume of "+currency+" is "+ numberToWords(int(data["24h_volume_usd"].split(".")[0]))+ " dollars."

def set_24hrVolume_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'volumeTwentyFour' in intent['slots']:
        current_currency = intent['slots']['volumeTwentyFour']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = set_24hrVolume_in_session(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def percent_change_7d(data):
    currency = data
    data = Coin(data)[0]
    return "The seven day percent change for "+currency+" is "+ data["percent_change_7d"] + " percent."

def set_7DayPercentChange_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'sevenDayPercentChange' in intent['slots']:
        current_currency = intent['slots']['sevenDayPercentChange']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = set_7DayPercentChange_in_session(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def symbol(data):
    currency = data
    data = Coin(data)[0]
    symbol = list(data["symbol"])
    return "The symbol of "+currency+" is "+" ".join(symbol)

def set_Symbol_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'symbol' in intent['slots']:
        current_currency = intent['slots']['symbol']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = set_Symbol_in_session(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def max_supply(data):
    currency = data
    data = Coin(data)[0]
    return "The max supply of "+currency+" is "+ numberToWords(int(data["max_supply"].split(".")[0]))+ " dollars."

def set_maxSupply_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'maxSupply' in intent['slots']:
        current_currency = intent['slots']['maxSupply']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = max_supply(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def percent_change_1h(data):
    currency = data
    data = Coin(data)[0]
    return "The one hour percent change for "+currency+" is "+data["percent_change_1h"]\
           + " percent."
def set_oneHRPercentChange_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'oneHRPercentChange' in intent['slots']:
        current_currency = intent['slots']['oneHRPercentChange']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = percent_change_1h(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def total_supply(data):
    currency = data
    data = Coin(data)[0]
    return "The total supply of "+currency+" is "+numberToWords(int(data["total_supply"].split(".")[0])) \
           +" coins."
def set_totalSupply_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'totalSupply' in intent['slots']:
        current_currency = intent['slots']['totalSupply']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = total_supply(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def available_supply(data):
    currency = data
    data = Coin(data)[0]
    return "The total supply of "+currency+" in the market is "+numberToWords(int(data["available_supply"].split(".")[0])) \
           +" coins."
def set_AvailableSupply_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'availableSupply' in intent['slots']:
        current_currency = intent['slots']['availableSupply']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = available_supply(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def percent_change_24h(data):
    currency = data
    data = Coin(data)[0]
    return "The twenty four hour percent change for "+currency+" is "+data["percent_change_24h"] + " percent."

def set_24HRpercentChange_in_session(intent, session):
    """ Sets the current_currency in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'percentChangeTwentyFourhr' in intent['slots']:
        current_currency = intent['slots']['percentChangeTwentyFourhr']['value']
        session_attributes = create_current_currency_attributes(current_currency)
        output = percent_change_24h(current_currency)
        speech_output = output+ " "
        reprompt_text = "You can ask me other questions about volume, percent change, max supply, etc"
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        reprompt_text = "I did't get that. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_currency_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "currentCurrency" in session.get('attributes', {}):
        current_currency = session['attributes']['currentCurrency']
        speech_output = "The current currency is " + current_currency + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I did't get that. " \
                        "Please try again.   "
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

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


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "WhatsMyCurrencyIntent":
        return get_currency_from_session(intent, session)


    elif intent_name == "getPriceUSD":
        return set_priceUSD_in_session(intent, session)
    elif intent_name == "getRank":
        return set_rank_in_session(intent, session)
    elif intent_name == "getMarketCap":
        return set_MarketCap_in_session(intent, session)
    elif intent_name == "getTwentyFourhrVolume":
        return set_24hrVolume_in_session(intent, session)
    elif intent_name == "getSevenDayPercentChange":
        return set_7DayPercentChange_in_session(intent, session)
    elif intent_name == "getSymbol":
        return set_Symbol_in_session(intent, session)
    elif intent_name == "getMaxSupply":
        return set_maxSupply_in_session(intent, session)
    elif intent_name == "getOnehrPercentChange":
        return set_oneHRPercentChange_in_session(intent, session)
    elif intent_name == "getTotalSupply":
        return set_totalSupply_in_session(intent, session)
    elif intent_name == "getAvailableSupply":
        return set_AvailableSupply_in_session(intent, session)
    elif intent_name == "getTwentyFourHRpercentChange":
        return set_24HRpercentChange_in_session(intent, session)

    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


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
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
