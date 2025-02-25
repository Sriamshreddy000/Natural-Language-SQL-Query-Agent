import re

def extract_action_input_and_observation(trace_file,full_trace=False):
    with open(trace_file, 'r') as file:
        content = file.read()
        if full_trace:
            return content    
    action_input = ''
    observation = ''
    observation_end_index = 0

    # Iterate through matches
    for match in re.finditer(r"Action Input: \"(.+?)\"\s*Observation: (.+?)\s*Thought:", content, re.DOTALL):
        action_input = match.group(1).strip()
        observation = match.group(2).strip()

        # Get the end index of the observation
        observation_end_index = match.end(2)
    final_thought=''
    for i in range(observation_end_index+1,len(content)):
        final_thought=final_thought+content[i]
        
    return action_input, observation,final_thought.replace('Thought:','')

def get_final_trace(full_trace=False):
    
    trace_file_path = "fulltrace.txt"
    if full_trace:
        fulltrace=extract_action_input_and_observation(trace_file_path,full_trace=True)
        return fulltrace
    action_input, observation, thought = extract_action_input_and_observation(trace_file_path)
    thought=thought.split('.')[0]+'.'
    return action_input,observation,thought
