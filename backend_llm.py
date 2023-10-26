from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import langchain
from langchain.agents import AgentType, ZeroShotAgent
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
import llm_memory



import llm_tools
import llm_prompt




#set variables
model_path = "./Model/speechless-llama2-hermes-orca-platypus-wizardlm-13b.Q8_0.gguf"
temperature = 0.4
n_gpu_layer = 100
n_batch = 40
max_tokens = 4192
Debug = True



memory = llm_memory.Memory_System("SIA")
memory.clear_Memory()






# load model
if Debug:
    callback = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path=model_path,
        temperature=temperature,
        n_gpu_layers=n_gpu_layer,
        n_batch=n_batch,
        max_tokens=max_tokens,
        top_p=1,
        callback_manager=callback,
        verbose=Debug,
        n_ctx=max_tokens,


    )
else:
    llm = LlamaCpp(
        model_path=model_path,
        temperature=temperature,
        n_gpu_layers=n_gpu_layer,
        n_batch=n_batch,
        max_tokens=max_tokens,
        top_p=1,
        verbose=Debug,
        n_ctx=max_tokens,

    )



# load tools
tools = llm_tools.load_tools(llm)


# create agent

agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=Debug, agent_kwargs={"ai_prefix": "SIA"})


agent.agent.llm_chain.prompt.template = llm_prompt.generate_prompt(tools)
agent.agent.llm_chain.prompt.input_variables = ['user_name', 'input', 'short_memory', 'agent_scratchpad']
agent.agent.ai_prefix = "SIA"








def call_Model(input:str, user="Unknown", mood="neutral"):
    answer = agent.invoke({"user_name": user, "input": input, "short_memory": memory.load_Memory()})
    if Debug:
        print(answer)
    memory.add_Memory(user, input, answer['output'])

    call_Model.counter += 1
    if Debug:
        print(f"\n\n\n\n\n\n\n{call_Model.counter}")
    return answer['output']
