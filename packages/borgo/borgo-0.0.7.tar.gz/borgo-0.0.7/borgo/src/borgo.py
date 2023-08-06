import socketio
import json
import uuid

socket_io = socketio.Client()
server_url = 'https://borgo-server.herokuapp.com/'

# Creates a client object for sending requests (and recieving responses)
# to the Borgo app. 
#
# For example:
# ```
# borgo_key = 'IzeJuLmd...' # <-- copied from Borgo app.
# with BorgoClient(borgo_key) as borgo_client:
#   request = BorgoRequest('Hello world?')
#   response = borgo_client.wait_for(request) # Sends "Hello world?" to app.
#   print(response.is_accepted) # True if user approved "Hello world?"
# ```
class BorgoClient:
  def __init__(self, key):
    self.key = key
    self.connected = False

  def __enter__(self):
    self.connect()
    return self
  
  def __exit__(self, exception_type, exception_value, traceback):
    self.disconnect()
  
  # Connects your code to the server (using your key) to send and recieve 
  # requests.
  #
  # If the key you passed in to the constructor is invalid or expired, this 
  # method will throw an exception.
  #
  # If the client is already connected, this method does nothing. 
  def connect(self):
    if (self.connected):
      return
    socket_io.connect(server_url)
    whitespace_removed_key = ''.join(self.key.split())
    socket_io.emit(
        'initialize',
        json.dumps({'key': whitespace_removed_key})
    )
    while 'initialized' not in responses:
      pass

    is_initialized = responses.pop('initialized')
    if (not is_initialized):
      error_message = 'Key provided is invalid or expired' + \
          ' - log in to https://borgo.app/ to get a new one.'
      raise Exception(error_message)
    self.connected = True

  # Disconnects your code from the server.
  def disconnect(self):
    socket_io.disconnect()
    self.connected = False
  
  # Sends request to the borgo app for the user to see, and halts until user 
  # responds to the given request.
  def wait_for(self, request):
    if (not self.connected):
      self.connect()
    request_id = str(uuid.uuid4())
    request_dict = {'id': request_id, 'body': request.to_dict()}
    socket_io.emit('request', json.dumps(request_dict))
    while request_id not in responses:
      pass
    response = responses.pop(request_id)
    return response

# The request that is sent to the Borgo app for the user to act on. 
#
# The `value` is the text that they will see. The user can either accept or
# reject the given `value`.
# 
# Optionally provide parameters for custom "accept" and "reject" labels.
# For example:
# ```
# BorgoRequest('Is a hot dog a sandwich?', 'Sandwich', 'Not Sandwich')
# ``` 
class BorgoRequest:
  def __init__(self, value, affirmative='Accept', negative='Reject'):
    self.value = value
    self.affirmative = affirmative
    self.negative = negative

  def to_dict(self):
    return {
        'value': self.value,
        'affirmative': self.affirmative,
        'negative': self.negative
    }

# Response from a user input on the borgo app. 
#
# Useful for telling if a request was accepted or rejected.
# For example:
# ```
# response = borgo_client.wait_for(BorgoRequest('Yes or no?'))
# if (response.is_accepted):
#   print('Yes')
# else
#   print('No')
class BorgoResponse:
  def __init__(self, status):
    self.status = status
    self.is_accepted = status == 'accepted'
    self.is_rejected = not self.is_accepted

responses = {}

@socket_io.on('response')
def on_message(data):
  response_id = data['data']['id']
  response = BorgoResponse(data['data']['body']['response'])
  responses[response_id] = response


@socket_io.on('initialized')
def on_message(data):
  responses['initialized'] = data
