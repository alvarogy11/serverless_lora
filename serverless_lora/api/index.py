from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
try:
  #from . import PyMongoVectorDatabase
  #from . import assistant_functions
  from . import polling_functions
except:
  #import PyMongoVectorDatabase
  #import assistant_functions
  import polling_functions

load_dotenv()

app = Flask(__name__)
CORS(app) 

api_key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key = api_key)

# Create new assistant or load existing
#assistant_id = assistant_functions.create_assistant(client)
assistant_id = os.getenv("ASSISTANT_ID")

#* Start conversation thread each time a new chat is opened, a new thread is created as well
@app.route('/api/start', methods=['GET'])
def start_conversation():
  print("Starting a new conversation...")  # Debugging line
  thread = client.beta.threads.create()
  print(f"New thread created with ID: {thread.id}")  # Debugging line
  return jsonify({"thread_id": thread.id})

#* Generate response every time the frontend polls a chat answer - Polling
@app.route('/api/polling', methods=['POST'])
def polling():
  # Posted data is fetch and saved into thread_id and user_input variables 
  data = request.get_json()
  
  run_id = data.get('run_id', '') 
  thread_id = data.get('thread_id')
  user_input = data.get('message', '')
  tool_outputs = data.get('tool_outputs', [])
  
  # The first message will always have 'start' status so this section will be executed
  if data.get('status') == 'start':
    response_json = polling_functions.startPolling(client, user_input, thread_id, assistant_id, tool_outputs)
    return response_json
  
  elif data.get('status') == 'action_completed':
    #Notifies the llm that the action has been processed
    response_json = polling_functions.actionCompleted(client, run_status, thread_id, run_id, tool_outputs)
    return response_json
  
  # This section will be executed on all of the following situations
  else:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    print(f"Run status: {run_status.status}")
    
    if run_status.status == 'requires_action' and run_status.required_action is not None:
      response_json = polling_functions.requiredActions(client, run_status, tool_outputs, thread_id, run_id)
      return response_json
        
    elif run_status.status == 'completed':
      response_json, response_og = polling_functions.responseCompleted(client, run_status, user_input, tool_outputs, thread_id, run_id)
      # The costs of the conversation (message response pair) are sent to the databese
      #assistant_functions.MonitorConversationCosts(thread_id=thread_id, user_input=user_input, response=response_og, tool_outputs=tool_outputs)
      return response_json
    
    elif run_status.status == 'cancelled' or run_status.status == 'cancelling':
      print("Response being cancelled...")
      return jsonify({'status':run_status.status, 'response': 'Cancelled Response...', 'thread_id' : thread_id, 'run_id' : run_id, "tool_outputs":tool_outputs})
    
    else:
      print("Waiting for the Assistant to process...")
      return jsonify({'status':run_status.status, 'response': 'Generating Response...', 'thread_id' : thread_id, 'run_id' : run_id, "tool_outputs":tool_outputs})        

#* Only used to verify the backend is up and runing
@app.route('/api/test', methods=['GET'])
def test():
  return 'Hello World :D'

if __name__ == '__main__':
  #runs the app
  app.run()
