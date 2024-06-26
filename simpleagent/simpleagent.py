from utils import SendToOpenai, SendToGroq, SendToLLM
from random import randint
from agent_names import agent_firstnames,agent_lastnames

class Agent:
    def __init__(self, instructions, client: SendToLLM, number_of_turns = 5):
        self.instructions = instructions
        self.client = client
        self.prompt = self.generate_prompt_from_instructions(instructions)
        self.agent_name = self.generate_random_agent_name()
        if number_of_turns > 0:
            self.start_project(number_of_turns)

    def generate_random_agent_name(self):
        firstname = agent_firstnames[randint(0,len(agent_firstnames)-1)]
        lastname = agent_lastnames[randint(0,len(agent_lastnames)-1)]
        return f"{firstname} {lastname}"


    def generate_prompt_from_instructions(self, instructions):
        self.prompt_generation_prefix = """You are an administrator.  A user has given instructions for a task that must be completed.
        You are to generate a prompt that will be given to an AI agent.  The prompt should be generated from the instructions given by the user.
        The prompt should include instructions, and any other information that is necessary for the AI agent to complete the task.
        The prompt should be generated in a way that is clear and concise, and should be written in a way that is easy for the AI agent to understand.
        Please tell the agent to explain its reasoning for each step it takes.  This is the user's instructions: """

        self.agent_prompt_generation_prompt = self.prompt_generation_prefix + instructions

        prompt = self.client.send(self.agent_prompt_generation_prompt)
        return prompt

    def start_project(self, number_of_turns=5, history=None):
        self.history = history
        print("Project started for agent: ", self.agent_name)
        print("Instructions: ", self.instructions)
        message_to_llm = self.prompt
        for i in range(number_of_turns):
            response = self.client.send(message_to_llm)
            print(f"\n\n ---------------------------------------------- \n\n Response from agent {self.agent_name}: \n\n {response}\n\n")
            message_to_llm += response
        return message_to_llm

class Swarm:
    def __init__(self, instructions, client, number_of_agents,number_of_turns=5):
        self.agents_list = []
        for i in range(number_of_agents):
            self.agents_list.append(Agent(instructions, client, 0))
        self.start_project(number_of_turns)

    #Each agent has its own name and ai-generated instructions, told to work with n-1 number of other agents.
    def start_project(self,number_of_turns=5):
        chat_history = []
        for turn in range(number_of_turns):
            for agent in self.agents_list:
                agent_response = agent.start_project(number_of_turns=1, history = str(chat_history))
                chat_history += f"Response from {agent.agent_name}: "
                # print(f"Response from {agent.agent_name}: \n {agent_response}")
                chat_history += agent_response

#Something is wrong, it will have each agent talk 5 times before moving on to the next agent.        


        
