# Redis Key-Value Store for Teams/Zoom-like Environment
## Project Description
This project is designed to simulate a Teams/Zoom-like environment, where admins can create meetings and users can join/leave meetings, post chat messages, etc. Redis is used as the key-value store for storing the database.

The database consists of the following elements:

* users (userID, name, age, gender, email)
* meetings (meetingID, title, description, isPublic, audience)
* meeting_instances (meetingID, orderID, fromdatetime, todatetime)
* eventsLog (event_id, userID, event_type, timestamp)

## Requirements
* Python/Java
* Redis

## Functions

* `join_meeting(user_id, meeting_instance_id)`<br>
This function allows a user to join an active meeting instance. If the meeting is public, any user can join. If the meeting is private, the user can join only if their email is in the audience list. The function updates the eventsLog with a join event. If successful, the function returns "User joined meeting successfully".

* `leave_meeting(user_id, meeting_instance_id)`<br>
This function allows a user to leave a meeting they have already joined. The function updates the eventsLog with a leave event. If successful, the function returns "User left meeting successfully".

* `show_current_participants(meeting_instance_id)`<br>
This function returns a list of current participants for a given meeting instance.

* `show_active_meetings()`<br>
This function returns a list of active meeting titles.

* `end_meeting(meeting_instance_id)`<br>
This function ends a meeting by removing all participants from the participants set and updating the eventsLog with a leave event for each participant. The meeting instance is then set to inactive. If successful, the function returns "Meeting ended successfully".

* `post_chat_message(user_id, meeting_instance_id, message)`<br>
This function allows a user to post a chat message for a given meeting instance. The function checks if the message has already been posted and if not, it adds the message to the chat_messages list for the meeting instance. If successful, the function returns "Chat message posted successfully".

* `show_chat_messages(meeting_instance_id)`<br>
This function returns a list of chat messages for a given meeting instance in chronological order.

* `show_participant_join_times(meeting_instance_id)`
This function returns a dictionary of participant join times for a given meeting instance.

* `show_user_chat_messages(user_id, meeting_instance_id)`<br>
This function returns a list of chat messages for a given user in a given meeting instance

## Installation and Setup
To use this project, you will need to have Redis installed and running on your local machine. You can download and install Redis from the official website: https://redis.io/download

Once Redis is downloaded, you can start the Redis server using the following command:

```
sudo service redis-server start
```

To use the functions provided in this project, you will also need to install the Redis Python library. You can do this using pip:

```
pip install redis
```

Once Redis is installed and running and the Redis Python library is installed, you can clone this repository using:

```
git clone https://github.com/yourusername/redis-meetings.git
```

## Usage
To use the functions provided in this project, import the redis_functions module into your Python code:

```
import redis_functions as rf
```
You can then call any of the functions provided by redis_functions. For example:

```
result = rf.join_meeting(user_id, meeting_instance_id)
```

## Tests
Tests have been provided in the test_functions.py file to ensure that the functions are working correctly.
You can run the tests by running the following command from the project directory:

```
python test_functions.py
```
The tests cover the following scenarios:

* join_meeting with a public meeting
* leave_meeting with a public meeting
* join_meeting with a private meeting (user is not allowed to join)
* join_meeting with a private meeting (user is allowed to join)
* leave_meeting with a private meeting (user is a participant)
* leave_meeting with a private meeting (user is not a participant)
* end_meeting
* post_chat_message
* show_chat_messages
* show_user_chat_messages
* show_current_participants with an empty set
* post_chat_message with a message that has already been posted

For each test, the expected output is compared to the actual output of the function using an assert statement.
If the expected and actual outputs do not match, an error message is printed indicating which test failed and what the expected and actual outputs were. If all tests pass, no output is printed to the console

## Acknowledgements

This project was created as part of **Big Data Management Systems** course at Department of Management Science & Technology in Athens University of Economics and Business
