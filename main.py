from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from agent_logger import AgentLogger

# Load environment variables
load_dotenv()

# Initialize logger
logger = AgentLogger()

# Initialize the LLM with better parameters
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000,
    frequency_penalty=0.5,  # Reduce repetition
    presence_penalty=0.5    # Encourage diversity in responses
)

# Create conversation memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

# Create the prompt template with memory
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a compassionate mental health support assistant. Your role is to:
    1. Listen actively and empathetically to users' concerns
    2. Provide supportive responses and coping strategies
    3. Identify when professional help is needed
    4. Offer appropriate mental health resources using the get_mental_health_resources tool
    5. NEVER provide medical diagnoses or treatment recommendations
    6. ALWAYS encourage seeking professional help for serious concerns
    
    Remember to:
    - Be non-judgmental and supportive
    - Validate the user's feelings
    - Maintain professional boundaries
    - Prioritize user safety
    - Suggest professional help when appropriate
    - Always use the get_mental_health_resources tool when providing resources
    - Take action by suggesting specific resources and next steps
    - Consider previous conversation context when responding"""),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}"),
])

# Define response model with additional fields
class MentalHealthResponse(BaseModel):
    response: str = Field(description="The supportive response to the user's concern")
    resources: Optional[List[str]] = Field(description="List of relevant mental health resources or coping strategies")
    emergency: bool = Field(description="Whether the situation requires immediate professional help")
    follow_up_questions: Optional[List[str]] = Field(description="Suggested follow-up questions to better understand the user's needs")
    safety_check: bool = Field(description="Whether to perform an additional safety check", default=False)

# Create output parser
parser = PydanticOutputParser(pydantic_object=MentalHealthResponse)

# Enhanced mental health resources
def get_mental_health_resources(query: str) -> str:
    """Get relevant mental health resources based on the query."""
    resources = {
        "general": [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "NAMI Helpline: 1-800-950-NAMI (6264)",
            "SAMHSA's National Helpline: 1-800-662-HELP (4357)",
            "Veterans Crisis Line: 988 then press 1",
            "Trevor Project (LGBTQ+): 1-866-488-7386"
        ],
        "anxiety": [
            "Anxiety and Depression Association of America (ADAA)",
            "Mindfulness meditation apps like Headspace or Calm",
            "Deep breathing exercises",
            "Progressive muscle relaxation techniques",
            "Grounding techniques for panic attacks",
            "Cognitive Behavioral Therapy (CBT) resources"
        ],
        "depression": [
            "National Institute of Mental Health (NIMH) resources",
            "Depression and Bipolar Support Alliance (DBSA)",
            "Regular exercise and physical activity",
            "Maintaining a consistent sleep schedule",
            "Social connection strategies",
            "Professional therapy options"
        ],
        "trauma": [
            "National Center for PTSD",
            "RAINN (Rape, Abuse & Incest National Network): 1-800-656-HOPE",
            "Trauma-focused therapy resources",
            "Support groups for trauma survivors",
            "Self-care strategies for trauma recovery"
        ]
    }
    return "\n".join(resources.get(query.lower(), resources["general"]))

# Create tools with enhanced descriptions
tools = [
    Tool(
        name="get_mental_health_resources",
        func=get_mental_health_resources,
        description="""Useful for finding mental health resources and coping strategies. 
        Always use this tool when providing resources to users. 
        The tool returns curated lists of resources based on the user's specific needs."""
    )
]

# Create the agent with memory
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Create the agent executor with enhanced configuration
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

def process_response(response):
    """Process and format the agent's response with clear actions."""
    output = response.get("output", "")
    
    # Add clear action items if not present
    if "Here are some steps you can take" not in output:
        output += "\n\nHere are some steps you can take:"
        output += "\n1. Consider reaching out to a mental health professional"
        output += "\n2. Try some of the coping strategies mentioned"
        output += "\n3. Connect with support groups or trusted friends"
        output += "\n4. Practice self-care and be kind to yourself"
    
    # Add follow-up questions if available
    if response.get("follow_up_questions"):
        output += "\n\nTo better support you, I'd like to ask:"
        for i, question in enumerate(response["follow_up_questions"], 1):
            output += f"\n{i}. {question}"
    
    return output

def safety_check(response):
    """Perform additional safety checks on the response."""
    emergency_keywords = [
        "suicide", "kill myself", "end it all", "want to die",
        "self-harm", "hurt myself", "overdose", "no reason to live"
    ]
    
    user_input = response.get("input", "").lower()
    if any(keyword in user_input for keyword in emergency_keywords):
        return True
    return response.get("emergency", False)

if __name__ == "__main__":
    print("Mental Health Support Agent initialized. Type 'quit' to exit.")
    print("Note: This agent maintains conversation context to provide better support.")
    
    while True:
        user_input = input("\nHow can I help you today? (Type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            print("\nSession Summary:")
            print(logger.export_session())
            break
            
        try:
            response = agent_executor.invoke({"input": user_input})
            processed_output = process_response(response)
            print("\nResponse:", processed_output)
            
            # Log the interaction
            logger.log_interaction(user_input, response)
            
            # Perform safety check
            if safety_check(response):
                print("\n⚠️ IMPORTANT: Based on your input, we strongly recommend seeking immediate professional help.")
                print("Please contact emergency services or a mental health professional right away.")
                print("You can call 988 (Suicide & Crisis Lifeline) or 911 for immediate assistance.")
                print("You are not alone, and help is available.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or seek immediate professional help if you're in crisis.")