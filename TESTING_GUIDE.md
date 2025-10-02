# 🎉 Agentice - Modern AI-Powered Career Assistant

## ✨ What's New

### 🚀 Modern Interactive UI
- **Glass-morphism Design**: Beautiful, modern UI with translucent cards and gradient backgrounds
- **Real-time WebSocket Chat**: Bidirectional communication with AI agents
- **Voice Assistant**: Speech-to-text and text-to-speech capabilities
- **Live Agent Status**: See your AI agents working in real-time
- **Today's Activity Stats**: Track applications, interviews, and success rate

### 🤖 AI Agent Platform (AutoGen Framework)
- **Job Researcher**: Finds the best job opportunities
- **Resume Optimizer**: Enhances your resume for maximum impact
- **Cover Letter Writer**: Creates personalized cover letters
- **Application Manager**: Tracks and manages all applications
- **User Proxy**: Your personal interface to the agent team

## 🎯 How to Use

### 1. **Chat with AI Assistant**
- Type your message in the chat input
- Or click the microphone button to use voice
- Ask about job search, resume optimization, cover letters, or application status

### 2. **Quick Actions**
- **Search Jobs**: Find relevant job opportunities
- **Optimize Resume**: Get AI-powered resume improvements
- **Write Cover Letter**: Generate personalized cover letters
- **View Status**: Check your application progress

### 3. **Voice Assistant** 🎤
- Click the **microphone button** (circular button with pulse animation)
- Speak your request clearly
- The AI will respond with both text and voice

### 4. **Auto-Apply Mode**
- Toggle the **Auto-Apply Mode** switch in the right panel
- AI agents will autonomously find and apply to matching jobs
- Monitor progress in real-time through the dashboard

## 🔧 Technical Features

### Backend
- **FastAPI**: High-performance async web framework
- **AutoGen AgentChat**: Modern multi-agent orchestration
- **OpenAI GPT-4o**: Latest AI model for intelligent responses
- **WebSocket**: Real-time bidirectional communication
- **SQLAlchemy**: Robust database ORM

### Frontend
- **Bootstrap 5**: Responsive, mobile-first design
- **Web Speech API**: Browser-native voice recognition
- **Speech Synthesis API**: Text-to-speech responses
- **WebSocket Client**: Real-time agent communication
- **Font Awesome**: Beautiful icon library

## 🧪 Testing Guide

### Test the Chat
1. Open http://localhost:8000
2. Type: "Search for Python developer jobs in Remote"
3. Click send or press Enter
4. Watch the AI agents collaborate to find jobs

### Test Voice Assistant
1. Click the microphone button (should pulse)
2. Say: "Help me optimize my resume"
3. AI will transcribe, process, and respond with voice

### Test Quick Actions
1. Click "Search Jobs" quick action button
2. Click "Optimize Resume" to analyze your resume
3. Click "Write Cover Letter" for cover letter assistance
4. Click "View Status" to see application progress

### Test Auto-Apply
1. Toggle the Auto-Apply Mode switch (right panel)
2. Configure job preferences (keywords, location, salary)
3. AI agents will automatically find and apply to matching jobs
4. Monitor progress in Today's Activity stats

## 📊 Dashboard Features

### Today's Activity (Top Right)
- **Applications**: Jobs applied to today
- **Interviews**: Interview invitations
- **Responses**: Company responses received
- **Success Rate**: Application acceptance percentage

### Active AI Agents (Right Panel)
- **Job Researcher**: Finding opportunities...
- **Resume Optimizer**: Ready to optimize
- **Cover Letter Writer**: Standing by
- **Application Manager**: Monitoring applications

## 🔑 Configuration

### OpenAI API Key (Required)
Set your OpenAI API key in environment variables or `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### WebSocket Connection
The frontend automatically connects to:
```
ws://localhost:8000/api/v1/ws/chat/{clientId}
```

## 🐛 Troubleshooting

### Voice Not Working?
- **Chrome/Edge**: Voice works natively
- **Firefox**: Limited Web Speech API support
- **Safari**: Requires HTTPS for voice features
- **Solution**: Use Chrome or Edge for best experience

### WebSocket Not Connecting?
- Check if server is running: `http://localhost:8000`
- Verify WebSocket endpoint: `/api/v1/ws/chat/{clientId}`
- Check browser console for errors
- Ensure no firewall blocking port 8000

### AI Not Responding?
- Verify OpenAI API key is set correctly
- Check API key has sufficient credits
- View server logs for error messages
- Ensure `OPENAI_MODEL=gpt-4o` in settings

## 🎨 UI Features

### Glass-morphism Cards
- Semi-transparent backgrounds
- Backdrop blur effects
- Subtle shadows and borders
- Smooth transitions and animations

### Chat Interface
- User messages: Purple gradient bubbles (right)
- AI messages: White bubbles with borders (left)
- Typing indicator: Animated dots when AI is thinking
- Auto-scroll to latest message

### Voice Button Animation
- **Idle**: Purple gradient, subtle shadow
- **Hover**: Scale up, stronger shadow
- **Listening**: Pulsing animation
- **Active**: Continuous pulse effect

## 📈 Next Steps

1. **Add Your OpenAI API Key** to enable AI responses
2. **Upload Your Resume** for personalization
3. **Set Job Preferences** (keywords, location, salary)
4. **Enable Auto-Apply Mode** for autonomous job applications
5. **Monitor Dashboard** for real-time progress

## 🚀 Running the Application

```bash
# Start the server
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Or use the start script
./start.sh

# Access the UI
http://localhost:8000
```

## 🎯 Example Conversations

### Job Search
**You**: "Find me Python developer jobs in San Francisco with salary above $150k"
**AI**: *Searches multiple job boards, filters by criteria, presents top matches*

### Resume Optimization
**You**: "Optimize my resume for AI/ML positions"
**AI**: *Analyzes resume, suggests improvements, highlights key skills*

### Cover Letter
**You**: "Write a cover letter for Senior Data Engineer at Google"
**AI**: *Generates personalized, compelling cover letter*

### Application Status
**You**: "What's my application status?"
**AI**: *Shows pending applications, interview schedules, responses*

## 🌟 Key Features Summary

✅ Modern glass-morphism UI design
✅ Real-time WebSocket chat
✅ Voice assistant (speech-to-text, text-to-speech)
✅ 5 specialized AI agents (AutoGen)
✅ Live activity dashboard
✅ Quick action buttons
✅ Auto-apply automation
✅ Responsive mobile design
✅ Real-time typing indicators
✅ Beautiful animations

---

**Built with ❤️ using FastAPI, AutoGen, OpenAI GPT-4o, Bootstrap 5, and Web Speech API**
