# Mental Health Support AI Agent

A compassionate AI agent designed to provide mental health support and resources. This agent uses LangChain and OpenAI's GPT-4 to offer empathetic responses and relevant mental health resources while maintaining professional boundaries.

## ⚠️ Important Disclaimer

This AI agent is NOT a replacement for professional mental health care. It is designed to:
- Provide supportive responses
- Offer coping strategies
- Share mental health resources
- Encourage seeking professional help when appropriate

The agent will NEVER:
- Provide medical diagnoses
- Recommend specific treatments
- Replace professional mental health services

If you're in crisis, please contact emergency services or a mental health professional immediately.

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd microsoft_ai_agent_hackathon
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## 💻 Usage

1. **Start the agent**
   ```bash
   python main.py
   ```

2. **Interact with the agent**
   - The agent will start in interactive mode
   - Type your concerns or questions
   - Receive supportive responses with actionable steps
   - Type 'quit' to end the conversation

## 🛠️ Features

- **Interactive Support**: Direct conversation with the mental health support agent
- **Resource Tool**: Access to curated mental health resources and coping strategies
- **Action-Oriented Responses**: Each response includes clear steps to take
- **Safety Features**: 
  - Emergency resource recommendations
  - Professional help encouragement
  - Crisis hotline information (988, 911)
- **Conversation Memory**: Maintains context throughout the conversation
- **Safety Monitoring**: Detects crisis situations and provides appropriate resources

## 📚 Available Resources

The agent provides access to:
- General mental health resources
  - National Suicide Prevention Lifeline: 988
  - Crisis Text Line: Text HOME to 741741
  - NAMI Helpline: 1-800-950-NAMI (6264)
  - SAMHSA's National Helpline: 1-800-662-HELP (4357)
- Anxiety management strategies
  - ADAA resources
  - Mindfulness apps
  - Breathing exercises
  - Relaxation techniques
- Depression support
  - NIMH resources
  - DBSA support
  - Exercise recommendations
  - Sleep schedule guidance

## 🔧 Technical Details

- Built with LangChain and OpenAI's GPT-4
- Uses tool-calling agent for resource retrieval
- Implements Pydantic models for structured responses
- Features automatic emergency detection
- Includes response processing for clear action items
- Uses ConversationBufferMemory for maintaining context
- Implements safety checks for crisis situations

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add more mental health resources
- Improve the response templates
- Enhance the safety features
- Add new support tools
- Improve conversation memory handling
- Add more comprehensive safety checks

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4-turbo model
- LangChain for the framework
- Mental health organizations for their resources
