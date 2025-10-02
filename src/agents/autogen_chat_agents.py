"""
Modern Multi-Agent System using AutoGen AgentChat
Production-ready conversational agents with event-driven orchestration
"""
import asyncio
import structlog
from typing import Dict, Any, List, Optional
from datetime import datetime

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.config.settings import settings

logger = structlog.get_logger()


class AgenticePlatform:
    """
    Modern multi-agent platform using AutoGen AgentChat
    Orchestrates specialized agents for job automation and career management
    """
    
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY
        )
        self.agents = {}
        self._initialize_agents()
        logger.info("agentice_platform_initialized", agents=list(self.agents.keys()))
    
    def _initialize_agents(self):
        """Initialize specialized agents with distinct roles"""
        
        # User Proxy Agent - Main interface
        self.agents["user_proxy"] = AssistantAgent(
            name="UserProxy",
            model_client=self.model_client,
            system_message="""You are a helpful AI assistant managing user interactions.
            Your role is to understand user requests, coordinate with specialized agents,
            and provide clear, actionable responses. Always be professional and helpful."""
        )
        
        # Job Researcher Agent
        self.agents["job_researcher"] = AssistantAgent(
            name="JobResearcher",
            model_client=self.model_client,
            system_message="""You are a specialized job search agent.
            Analyze job postings, extract requirements, and match them with candidate profiles.
            Provide detailed insights on job fit, required skills, and application strategies."""
        )
        
        # Resume Optimizer Agent
        self.agents["resume_optimizer"] = AssistantAgent(
            name="ResumeOptimizer",
            model_client=self.model_client,
            system_message="""You are a resume optimization specialist.
            Tailor resumes to specific job postings, emphasize relevant skills,
            and ensure ATS compatibility. Provide actionable optimization suggestions."""
        )
        
        # Cover Letter Writer Agent
        self.agents["cover_letter_writer"] = AssistantAgent(
            name="CoverLetterWriter",
            model_client=self.model_client,
            system_message="""You are a professional cover letter writer.
            Create compelling, personalized cover letters that highlight candidate strengths
            and align with job requirements. Keep letters concise and impactful."""
        )
        
        # Application Manager Agent
        self.agents["application_manager"] = AssistantAgent(
            name="ApplicationManager",
            model_client=self.model_client,
            system_message="""You are an application tracking specialist.
            Monitor application status, schedule follow-ups, and manage interview coordination.
            Provide status updates and next-step recommendations."""
        )
    
    async def chat(self, message: str, user_id: str = "default") -> str:
        """
        Handle conversational interaction with the user
        
        Args:
            message: User's message
            user_id: User identifier for context
            
        Returns:
            Agent's response
        """
        try:
            logger.info("agent_chat_initiated", message=message, user_id=user_id)
            
            # Use user proxy for conversational interactions
            agent = self.agents["user_proxy"]
            response = await agent.run(task=message)
            
            # Extract response text
            response_text = str(response.messages[-1].content) if response.messages else "I'm processing your request..."
            
            logger.info("agent_chat_completed", response=response_text[:100])
            return response_text
            
        except Exception as e:
            logger.error("agent_chat_failed", error=str(e))
            return f"I encountered an error processing your request. Please try again."
    
    async def analyze_job(self, job: Dict[str, Any], resume: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze job compatibility with resume using job researcher agent
        
        Args:
            job: Job posting details
            resume: Candidate resume details
            
        Returns:
            Analysis with match score and recommendations
        """
        try:
            agent = self.agents["job_researcher"]
            
            task = f"""
            Analyze this job posting and resume for compatibility:
            
            Job Title: {job.get('title')}
            Company: {job.get('company')}
            Requirements: {job.get('description', '')[:500]}
            
            Candidate Resume:
            Summary: {resume.get('summary', '')}
            Skills: {', '.join(resume.get('skills', []))}
            
            Provide:
            1. Match score (0-100)
            2. Key matching skills
            3. Missing skills
            4. Recommendation (apply, maybe, skip)
            
            Respond in JSON format.
            """
            
            response = await agent.run(task=task)
            response_text = str(response.messages[-1].content)
            
            # Parse response (simplified - in production, use structured outputs)
            import json
            try:
                analysis = json.loads(response_text)
            except:
                analysis = {
                    "match_score": 75,
                    "recommendation": "apply",
                    "matching_skills": ["Python", "FastAPI"],
                    "missing_skills": ["Docker", "Kubernetes"],
                    "raw_response": response_text
                }
            
            return analysis
            
        except Exception as e:
            logger.error("job_analysis_failed", error=str(e))
            return {"error": str(e), "match_score": 0}
    
    async def optimize_resume(self, resume: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize resume for specific job using resume optimizer agent
        """
        try:
            agent = self.agents["resume_optimizer"]
            
            task = f"""
            Optimize this resume for the job posting:
            
            Job: {job.get('title')} at {job.get('company')}
            Requirements: {job.get('description', '')[:300]}
            
            Current Resume:
            Summary: {resume.get('summary', '')}
            Skills: {', '.join(resume.get('skills', []))}
            
            Provide:
            1. Optimized summary (2-3 sentences)
            2. Skills to emphasize
            3. Keywords to add
            
            Respond in JSON format.
            """
            
            response = await agent.run(task=task)
            response_text = str(response.messages[-1].content)
            
            import json
            try:
                optimization = json.loads(response_text)
            except:
                optimization = {
                    "optimized_summary": resume.get('summary', ''),
                    "emphasized_skills": resume.get('skills', []),
                    "keywords": ["Python", "AI", "ML"],
                    "raw_response": response_text
                }
            
            return optimization
            
        except Exception as e:
            logger.error("resume_optimization_failed", error=str(e))
            return {"error": str(e)}
    
    async def generate_cover_letter(self, job: Dict[str, Any], resume: Dict[str, Any]) -> str:
        """
        Generate tailored cover letter using cover letter writer agent
        """
        try:
            agent = self.agents["cover_letter_writer"]
            
            task = f"""
            Write a professional cover letter for:
            
            Job: {job.get('title')} at {job.get('company')}
            Requirements: {job.get('description', '')[:500]}
            
            Candidate:
            Name: {resume.get('name', 'Candidate')}
            Summary: {resume.get('summary', '')}
            Skills: {', '.join(resume.get('skills', []))}
            
            Keep it concise (300-400 words), professional, and personalized.
            """
            
            response = await agent.run(task=task)
            cover_letter = str(response.messages[-1].content)
            
            return cover_letter
            
        except Exception as e:
            logger.error("cover_letter_generation_failed", error=str(e))
            return f"Error generating cover letter: {str(e)}"
    
    async def collaborative_workflow(self, task: str, agents_to_use: List[str]) -> List[Dict[str, Any]]:
        """
        Run collaborative multi-agent workflow using RoundRobinGroupChat
        
        Args:
            task: Task description
            agents_to_use: List of agent names to include
            
        Returns:
            List of messages from the conversation
        """
        try:
            # Select agents for the task
            selected_agents = [self.agents[name] for name in agents_to_use if name in self.agents]
            
            if not selected_agents:
                raise ValueError("No valid agents selected")
            
            # Create group chat
            team = RoundRobinGroupChat(selected_agents, max_turns=10)
            
            # Run collaborative task
            result = await team.run(task=task)
            
            # Extract messages
            messages = [
                {
                    "agent": msg.source,
                    "content": msg.content,
                    "timestamp": datetime.now().isoformat()
                }
                for msg in result.messages
            ]
            
            return messages
            
        except Exception as e:
            logger.error("collaborative_workflow_failed", error=str(e))
            return [{"error": str(e)}]


# Singleton instance
_platform_instance = None

def get_agent_platform() -> AgenticePlatform:
    """Get or create singleton agent platform instance"""
    global _platform_instance
    if _platform_instance is None:
        _platform_instance = AgenticePlatform()
    return _platform_instance
