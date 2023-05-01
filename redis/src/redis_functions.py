import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def join_meeting(user_id, meeting_instance_id):
    # Check if meeting instance is active
    if r.hget(meeting_instance_id, 'active') == 'false':
        return "Meeting instance is not active"
    
    # Check if meeting is public or user is allowed to join
    is_public = r.hget(meeting_instance_id, 'isPublic').decode('utf-8') == 'true'
    if is_public:
        audience = []
    else:
        audience = r.hget(meeting_instance_id, 'audience')
        if audience is None:
            return "Audience list is missing for this meeting"
        audience = audience.decode('utf-8').split(',')
    
    if not is_public and user_id not in audience:
        return "User is not allowed to join this meeting"
    
    # Add user to participants set
    r.sadd(f"{meeting_instance_id}:participants", user_id)
    
    # Log join event
    r.rpush('eventsLog', f"{user_id} joined {meeting_instance_id} at {time.time()}")
    
    return "User joined meeting successfully"


def leave_meeting(user_id, meeting_instance_id):
    # Check if user is a participant
    if not r.sismember(f"{meeting_instance_id}:participants", user_id):
        return "User is not a participant of this meeting"
    
    # Remove user from participants set
    r.srem(f"{meeting_instance_id}:participants", user_id)
    
    # Log leave event
    r.rpush('eventsLog', f"{user_id} left {meeting_instance_id} at {time.time()}")
    
    return "User left meeting successfully"


def show_current_participants(meeting_instance_id):
    # Get set of participants
    participants = r.smembers(f"{meeting_instance_id}:participants")
    
    # Return list of participants as strings
    return [participant.decode('utf-8') for participant in participants]


def show_active_meetings():
    # Get all meeting instance IDs
    meeting_instance_ids = r.keys('meeting_instance:*')
    
    # Filter by active meetings
    active_meeting_instance_ids = [id.decode('utf-8') for id in meeting_instance_ids if r.hget(id, 'active') == 'true']
    
    # Get meeting titles
    meeting_titles = [r.hget(id, 'title') for id in active_meeting_instance_ids]
    
    # Return list of active meeting titles
    return list(meeting_titles)

def end_meeting(meeting_instance_id):
    # Get participants set
    participants = r.smembers(f"{meeting_instance_id}:participants")
    
    # Remove participants from set
    for participant in participants:
        r.srem(f"{meeting_instance_id}:participants", participant)
        
        # Log leave event for each participant
        r.rpush('eventsLog', f"{participant} left {meeting_instance_id} at {time.time()}")
        
    # Set meeting instance to inactive
    r.hset(meeting_instance_id, 'active', 'false')
    
    return "Meeting ended successfully"

def post_chat_message(user_id, meeting_instance_id, message):
    # Check if message has already been posted
    messages = show_chat_messages(meeting_instance_id)
    for m in messages:
        if m.split(": ", 1)[1] == message:
            return "Error: Message has already been posted"
    
    # Add chat message to meeting instance list
    r.rpush(f"{meeting_instance_id}:chat_messages", f"{user_id}: {message}")
    
    return "Chat message posted successfully"

def show_chat_messages(meeting_instance_id):
    # Get chat messages list
    chat_messages = r.lrange(f"{meeting_instance_id}:chat_messages", 0, -1)
    
    # Return list of chat messages as strings
    return [message.decode('utf-8') for message in chat_messages]

def show_participant_join_times(meeting_instance_id):
    # Get participants set
    participants = r.smembers(f"{meeting_instance_id}:participants")

    # Create dictionary of participant join times
    join_times = {}
    for participant in participants:
        # Get join event from eventsLog
        join_event = r.lrange('eventsLog', 0, -1, f"*{participant.decode('utf-8')} joined {meeting_instance_id}*")
        if join_event:
            # Extract timestamp from join event
            timestamp = float(join_event[0].split()[-1])

            # Add timestamp to dictionary
            join_times[participant.decode('utf-8')] = timestamp

    # Return dictionary of join times
    return join_times


def show_user_chat_messages(user_id, meeting_instance_id):
    # Get chat messages list
    chat_messages = r.lrange(f"{meeting_instance_id}:chat_messages", 0, -1)
    
    # Filter chat messages by user ID
    user_chat_messages = [message.decode('utf-8') for message in chat_messages if message.decode('utf-8').startswith(f"{user_id}:")]
    
    # Return list of user's chat messages
    return user_chat_messages
