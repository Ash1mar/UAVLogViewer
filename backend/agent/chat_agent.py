from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from agent.tools import get_max_altitude, first_gps_loss_time

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4o")  # "gpt-4o"

tools = [get_max_altitude, first_gps_loss_time]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "prefix": (
            "You are an expert UAV flight log analyst.\n"
            "You are given access to tools to summarize telemetry and detect anomalies.\n"
            "⚠️ IMPORTANT: When the user asks about suspicious behavior, or requests summary or anomaly detection,\n"
            "you MUST call tools like `describe_flight_summary` or `detect_anomalies` to analyze the data before responding.\n"
            "Do NOT just explain—ALWAYS call a tool if data analysis is required."
        )
    }
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
    first_rc_loss_time,
    describe_flight_summary,
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
    first_rc_loss_time,
    describe_flight_summary,
]
