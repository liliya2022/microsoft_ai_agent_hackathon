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
   - Type your concerns or questions
   - The agent will respond with supportive messages and relevant resources
   - Type 'quit' to end the conversation

## 🛠️ Features

- **Empathetic Responses**: The agent provides supportive and understanding responses
- **Resource Database**: Access to various mental health resources and coping strategies
- **Safety Features**: 
  - Emergency resource recommendations
  - Professional help encouragement
  - Crisis hotline information

## 📚 Available Resources

The agent can provide information about:
- General mental health resources
- Anxiety management strategies
- Depression support resources
- Crisis intervention services
- Professional help options

## 🔧 Technical Details

- Built with LangChain and OpenAI's GPT-4
- Uses Pydantic for response validation
- Implements tool-calling for resource retrieval
- Maintains conversation context

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add more mental health resources
- Improve the response templates
- Enhance the safety features
- Add new support tools

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 model
- LangChain for the framework
- Mental health organizations for their resources