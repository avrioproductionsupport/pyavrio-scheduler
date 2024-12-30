# PyAvrio Scheduler

A Python library for authentication and scheduling.

# Features

Authentication:

Supports both username/password and access token authentication.
Maintains session state using the UserState class.

Scheduler Management:

Choose which topic you want to list: python_notebook, sql_notebook or data_quality
List all available schedulers.
Trigger specific schedulers by name and ID.

## Installation

```bash
pip install pyavrio-scheduler
```

## Usage

### Authentication

You can authenticate using either username/password or an access token:

```python
from pyavrio_scheduler import Authentication

auth = Authentication()

# Using username and password
auth.authenticate({
    'method': 'password',
    'username': 'user@example.com',
    'password': 'secretpassword'
})

# Using access token
auth.authenticate({
    'method': 'access_token',
    'access_token': 'your-access-token'
})
```
The authentication state is maintained globally using the UserState singleton class.

Scheduler Operations:

Once authenticated, you can interact with the scheduler:
```python
# Get scheduler instance from session
scheduler = session.get_scheduler()

# List all schedulers
schedulers = scheduler.list_all(topic_name)

#Triggering a scheduler
scheduler.trigger_scheduler(scheduler_name, scheduler_id, topic_name)
```
