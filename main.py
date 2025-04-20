from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from agent_logger import AgentLogger

# Load environment variables
load_dotenv()

# Initialize logger
logger = AgentLogger()

# Define response model
class MentalHealthResponse(BaseModel):
    response: str = Field(description="The supportive response to the user's concern")
    resources: Optional[List[str]] = Field(description="List of relevant mental health resources or coping strategies")
    emergency: bool = Field(description="Whether the situation requires immediate professional help")

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)  # Using GPT-4 with slightly higher temperature for more empathetic responses

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a compassionate mental health support assistant. Your role is to:
    1. Listen actively and empathetically to users' concerns
    2. Provide supportive responses and coping strategies
    3. Identify when professional help is needed
    4. Offer appropriate mental health resources
    5. NEVER provide medical diagnoses or treatment recommendations
    6. ALWAYS encourage seeking professional help for serious concerns
    
    Remember to:
    - Be non-judgmental and supportive
    - Validate the user's feelings
    - Maintain professional boundaries
    - Prioritize user safety
    - Suggest professional help when appropriate"""),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}"),
])

# Create output parser
parser = PydanticOutputParser(pydantic_object=MentalHealthResponse)

# Define tools for the agent
def get_mental_health_resources(query: str) -> str:
    """Get relevant mental health resources based on the query."""
    # This could be expanded to include a database of resources
    resources = {
        "general": [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "NAMI Helpline: 1-800-950-NAMI (6264)",
            "SAMHSA's National Helpline: 1-800-662-HELP (4357)"
        ],
        "anxiety": [
            "Anxiety and Depression Association of America (ADAA)",
            "Mindfulness meditation apps like Headspace or Calm",
            "Deep breathing exercises",
            "Progressive muscle relaxation techniques"
        ],
        "depression": [
            "National Institute of Mental Health (NIMH) resources",
            "Depression and Bipolar Support Alliance (DBSA)",
            "Regular exercise and physical activity",
            "Maintaining a consistent sleep schedule"
        ]
    }
    return "\n".join(resources.get(query.lower(), resources["general"]))

# Create tools
tools = [
    Tool(
        name="get_mental_health_resources",
        func=get_mental_health_resources,
        description="Useful for finding mental health resources and coping strategies"
    )
]

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
if __name__ == "__main__":
    print("Mental Health Support Agent initialized. Type 'quit' to exit.")
    print("Note: All conversations are logged for quality improvement purposes.")
    
    while True:
        user_input = input("\nHow can I help you today? (Type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            # Print session summary before exiting
            print("\nSession Summary:")
            print(logger.export_session())
            break
            
        try:
            response = agent_executor.invoke({"input": user_input})
            print("\nResponse:", response["output"])
            
            # Log the interaction
            logger.log_interaction(user_input, response)
            
            # If emergency flag is set, show additional warning
            if response.get("emergency", False):
                print("\n⚠️ IMPORTANT: Based on your input, we strongly recommend seeking immediate professional help.")
                print("Please contact emergency services or a mental health professional right away.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or seek immediate professional help if you're in crisis.")