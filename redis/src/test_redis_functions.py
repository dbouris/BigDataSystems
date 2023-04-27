import redis_functions as rf
import redis

# Sample inputs and expected outputs for each function
# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)
# join_meeting
user_id = '1'
meeting_instance_id = 'meeting_instance:1'
# Delete the key if it exists
if r.exists(meeting_instance_id):
    r.delete(meeting_instance_id)
r.hset(meeting_instance_id, 'title', 'Meeting 1')
r.hset(meeting_instance_id, 'description', 'This is a test meeting')
r.hset(meeting_instance_id, 'isPublic', 'false')
r.hset(meeting_instance_id, 'audience', '2,3')
r.hset(meeting_instance_id, 'active', 'true')

result = rf.join_meeting(user_id, meeting_instance_id)
expected = "User is not allowed to join this meeting"
print(f"join_meeting: expected={expected}, result={result}")
assert result == expected

# Create the hash and set its fields
r.hset(meeting_instance_id, 'title', 'Meeting 1')
r.hset(meeting_instance_id, 'description', 'This is a test meeting')
r.hset(meeting_instance_id, 'isPublic', 'false')
r.hset(meeting_instance_id, 'audience', '1,2,3')
r.hset(meeting_instance_id, 'active', 'true')

result = rf.join_meeting(user_id, meeting_instance_id)
expected = "User joined meeting successfully"
print(f"join_meeting: expected={expected}, result={result}")
assert result == expected

# leave_meeting
result = rf.leave_meeting(user_id, meeting_instance_id)
expected = "User left meeting successfully"
print(f"leave_meeting: expected={expected}, result={result}")
assert result == expected

result = rf.leave_meeting(user_id, meeting_instance_id)
expected = "User is not a participant of this meeting"
print(f"leave_meeting: expected={expected}, result={result}")
assert result == expected

# end_meeting
result = rf.end_meeting(meeting_instance_id)
expected = "Meeting ended successfully"
print(f"end_meeting: expected={expected}, result={result}")
assert result == expected

# post_chat_message
r.delete(f"{meeting_instance_id}:chat_messages")
result = rf.post_chat_message(user_id, meeting_instance_id, "Hello, world!")
expected = "Chat message posted successfully"
print(f"post_chat_message: expected={expected}, result={result}")
assert result == expected

result = rf.show_chat_messages(meeting_instance_id)
expected = ['1: Hello, world!']
print(f"show_chat_messages: expected={expected}, result={result}")
assert result == expected

# show_user_chat_messages
result = rf.show_user_chat_messages(user_id, meeting_instance_id)
expected = ['1: Hello, world!']
print(f"show_user_chat_messages: expected={expected}, result={result}")
assert result == expected



