import re
import constant
from utils import sender_actions, send_api, user_profile_api, pass_thread_control_api
from utils import chatbot_context_manager, icanhazdadjoke_helper

# Context manager is for storing the intent behind the last message that was sent by the bot
# It helps in gathering data and handling an edge case where user types out an option
# instead of selecting it in quick replies.
context_manager = chatbot_context_manager.ContextManager.default_db()

def compare_string_ignore_case_punctuation(str1, str2):
    """comapers sting ignoring special characters and case

    Args:
        str1 (String): String to compare
        str2 (String): String to compare

    Returns:
        Bool: Boolean value indicating equality
    """
    fun = lambda s: re.sub(r"[^\w\s]", "", s).casefold()
    return fun(str1) == fun(str2)

def handle_messaging_object(messaging_object):
    if "message" in messaging_object.keys():
        handle_message(messaging_object)
    elif "postback" in messaging_object.keys():
        handle_postback(messaging_object)
    elif "pass_thread_control" in messaging_object.keys():
        handle_thread_control(messaging_object)

def handle_thread_control(messaging_object):
    """Handles passing of thread control of this app.
    If "list all" is given as metadata. It dumps all the
    stored jokes twice.

    Args:
        messaging_object {Dictionary} -- Messaging object recieved by webhook
    """
    psid = messaging_object["sender"]["id"]
    metadata = messaging_object["pass_thread_control"]["metadata"]
    if metadata == "list all":
        send_api.send_simple_message(psid, "\n\n".join(constant.default_jokes))
        send_api.send_simple_message(psid, "\n\n".join(constant.default_jokes))
    handle_payload(psid, constant.payload.START_AGAIN_PAYLOAD)

def handle_message(messaging_object):
    """Handle messaging message object

    Arguments:
        messaging_object {Dictionary} -- Messaging object recieved by webhook
    """
    psid = messaging_object["sender"]["id"]
    sender_actions.inform_user_seen(psid)
    message_object = messaging_object["message"]

    # To check if message has payload to handle quick replies
    # and payload is not one to be discarded
    # (This done as I can't send quick reply without payload)
    if "quick_reply" in message_object.keys():
        # extract payload and handle them the same way as postback payloads
        payload_object = message_object["quick_reply"]["payload"]
        handle_payload(psid, payload_object)
    else:
        text = message_object["text"]

        # cancel any work and restart again
        if compare_string_ignore_case_punctuation(text, constant.message.CANCEL):
            handle_payload(psid, constant.payload.CANCEL_PAYLOAD)

       # check if word is a safe word and then pass thread control if needed
        elif any(compare_string_ignore_case_punctuation(text, s) for s in constant.safe_words):
            code = pass_thread_control_api.pass_thread_control(psid, "sos")
            if code == 200:
                context_manager.store_context(psid, constant.context.SOS_CONTEXT)

        # try to handle message based on context
        else:
            context = context_manager.get_context(psid)
            handle_context(psid, context, text)

def handle_postback(messaging_object):
    """Handle messaging postback object

    Arguments:
        messaging_object {Dictionary} -- Messaging object recieved by webhook
    """
    sender_id = messaging_object["sender"]["id"]
    sender_actions.inform_user_seen(sender_id)
    payload_object = messaging_object["postback"]["payload"]
    handle_payload(sender_id, payload_object)


def handle_context(psid, context, message):
    """Handles a message sent by user depending on the context it was sent in.
    In case the message is an option of a quick reply it's payload is forwarded
    to handle_payload

    Arguments:
        psid {String} -- PSID of user
        context {String} -- context of last message sent by us
        message {String} -- message sent by user
    """

    # compares message to quick reply options depending on context
    # and does the work that should be done
    # as the context is stored if the message doesn't match any option we can ask for another one

    if context in [constant.context.GET_STARTED_DECISION_CONTEXT,
                   constant.context.START_AGAIN_CONTEXT]:
        if compare_string_ignore_case_punctuation(message, constant.message.YES):
            handle_payload(psid, constant.payload.TELL_A_JOKE)
        elif compare_string_ignore_case_punctuation(message, constant.message.NO):
            handle_payload(psid, constant.payload.CANCEL_PAYLOAD)
        else:
            send_api.send_simple_message(psid, constant.message.CAN_NOT_UNDERSTAND)

    elif context == constant.context.CANCEL_CONTEXT:
        if compare_string_ignore_case_punctuation(message, constant.message.START):
            handle_payload(psid, constant.payload.START_AGAIN_PAYLOAD)
        else:
            send_api.send_simple_message(psid, constant.message.CAN_NOT_UNDERSTAND)

    elif context == constant.context.TOLD_JOKE_CONTEXT:
        if compare_string_ignore_case_punctuation(message, constant.message.TELL_ME_MORE):
            handle_payload(psid, constant.payload.TELL_A_JOKE)
        elif compare_string_ignore_case_punctuation(message, constant.message.EXIT):
            handle_payload(psid, constant.payload.CANCEL_PAYLOAD)
        else:
            send_api.send_simple_message(psid, constant.message.CAN_NOT_UNDERSTAND)

    else:
        send_api.send_simple_message(psid, constant.message.CAN_NOT_UNDERSTAND)




def handle_payload(psid, payload):
    """Method to handle payloads recieved

    Arguments:
        psid {String} -- PSID of user
        payload {String} -- payload recieved
    """

    # payload is from get started button. It is the first conversation.
    # Introducing bot and showing options
    if payload == constant.payload.GET_STARTED_PAYLOAD:

        send_api.send_simple_message(
            psid,
            constant.message.FIRST_MESSAGE.format(user_profile_api.get_user_first_name(psid))
        )

        context_manager.store_context(psid, constant.context.GET_STARTED_DECISION_CONTEXT)

        send_api.send_text_with_quick_reply(
            psid,
            constant.message.FIRST_CHOICE_TEXT,
            dict([(constant.message.YES, constant.payload.TELL_A_JOKE),
                  (constant.message.NO, constant.payload.CANCEL_PAYLOAD)]))

    # payload for starting again
    elif payload == constant.payload.START_AGAIN_PAYLOAD:

        context_manager.store_context(psid, constant.context.START_AGAIN_CONTEXT)

        send_api.send_text_with_quick_reply(
            psid,
            constant.message.RESTART_CHOICE_TEXT.format(user_profile_api.get_user_first_name(psid)),
            dict([(constant.message.YES, constant.payload.TELL_A_JOKE),
                  (constant.message.NO, constant.payload.CANCEL_PAYLOAD)]))

    # payload for telling a joke
    # Telling a random joke
    elif payload == constant.payload.TELL_A_JOKE:

        context_manager.store_context(psid, constant.context.TOLD_JOKE_CONTEXT)

        sender_actions.inform_user_typing_on(psid)

        send_api.send_text_with_quick_reply(
            psid,
            icanhazdadjoke_helper.get_a_joke(),
            dict([
                (constant.message.TELL_ME_MORE, constant.payload.TELL_A_JOKE),
                (constant.message.EXIT, constant.payload.CANCEL_PAYLOAD)
            ])
        )

    # payload for chat cancelled
    # giving instructions to start again
    elif payload == constant.payload.CANCEL_PAYLOAD:
        context_manager.store_context(psid, constant.context.CANCEL_CONTEXT)
        for message in constant.message.CANCEL_SIMPLE_MESSAGES:
            send_api.send_simple_message(psid, message)
