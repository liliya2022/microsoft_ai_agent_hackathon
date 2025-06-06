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
    model="gpt-4.1-2025-04-14",
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
    ("system", """You are a compassionate mental health support assistant. Your role is to engage in supportive conversations and provide helpful guidance.

    IMPORTANT: You MUST engage in conversation and provide supportive responses. Do not refuse to help or redirect to professionals unless there is an immediate safety concern.

    When responding, you should:
    1. Start with empathy and validation
    2. Ask follow-up questions to understand better
    3. Share relevant coping strategies
    4. Offer appropriate resources
    5. Maintain a warm, conversational tone

    Example conversation flow:
    User: "I've been feeling really low lately"
    Assistant: "I hear that you've been feeling low. That sounds really difficult. Would you like to talk more about what's been going on? Sometimes just sharing what's on your mind can help."

    User: "I feel like I'm not good enough"
    Assistant: "I understand that feeling. It's really common to be hard on ourselves sometimes. What makes you feel this way? I'm here to listen and help you work through these feelings."

    User: "I don't have the motivation to do anything"
    Assistant: "I hear how challenging this is for you. When did you start noticing this lack of motivation? Sometimes understanding when it began can help us figure out the best way to move forward."

    Remember to:
    - Be conversational and supportive
    - Ask open-ended questions
    - Validate feelings
    - Share coping strategies
    - Offer resources when appropriate
    - Maintain a warm, understanding tone"""),
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
    """Process and format the agent's response in a conversational way."""
    # Get the main response content
    if isinstance(response, dict):
        content = response.get("output", response.get("response", ""))
    else:
        content = str(response)
    
    # Format the response to be more conversational
    output = f"{content}"
    
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
    print("Mental Health Support Agent initialized. I'm here to listen and support you.")
    print("You can share what's on your mind, and we can talk about it together.")
    print("Type 'quit' when you'd like to end our conversation.")
    
    # Ask the initial question
    user_input = input("\nHow are you feeling today? (Type 'quit' to end): ")
    if user_input.lower() == 'quit':
        print("\nThank you for sharing with me. Take care of yourself.")
        exit()
        
    try:
        response = agent_executor.invoke({"input": user_input})
        processed_output = process_response(response)
        print("\nResponse:", processed_output)
        
        if safety_check(response):
            print("\n⚠️ I'm concerned about your safety. Please consider reaching out to:")
            print("988 (Suicide & Crisis Lifeline) or 911 for immediate support")
            print("You don't have to go through this alone.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("I'm still here to listen. Would you like to try sharing again?")
    
    # Continue conversation with simpler prompt
    while True:
        user_input = input("\nType your message here (Type 'quit' to end): ")
        if user_input.lower() == 'quit':
            print("\nThank you for sharing with me. Take care of yourself.")
            break
            
        try:
            response = agent_executor.invoke({"input": user_input})
            processed_output = process_response(response)
            print("\nResponse:", processed_output)
            
            if safety_check(response):
                print("\n⚠️ I'm concerned about your safety. Please consider reaching out to:")
                print("988 (Suicide & Crisis Lifeline) or 911 for immediate support")
                print("You don't have to go through this alone.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            print("I'm still here to listen. Would you like to try sharing again?")