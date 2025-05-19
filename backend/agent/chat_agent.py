from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from agent.tools import get_max_altitude, first_gps_loss_time
from agent.tools import detect_anomalies

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # "gpt-4o"

tools = [get_max_altitude, first_gps_loss_time]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)

from agent.tools import (
    get_max_altitude,
    first_gps_loss_time,
    get_max_voltage,
    get_max_current,
    get_max_temp,
    get_flight_duration,
    list_critical_errors,
    detect_anomalies,
)

tools = [
    get_max_altitude,
    first_gps_loss_time,
    get_max_voltage,
    get_max_current,
    get_max_temp,
    get_flight_duration,
    list_critical_errors,
    detect_anomalies,
]
