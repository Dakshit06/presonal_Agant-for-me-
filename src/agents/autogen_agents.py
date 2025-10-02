"""
AutoGen Multi-Agent System for Agentice
Implements autonomous job search, application, and career management agents
"""

# AutoGen is now autogen-agentchat
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat

from typing import List, Dict, Any, Optional
import structlog
from datetime import datetime

from src.config.settings import settings

# Import these models conditionally to avoid circular imports
# from src.services.llm_service import LLMService
# from src.models.opportunity import Opportunity
# from src.models.resume import Resume
# from src.models.application import Application

logger = structlog.get_logger()


class AgenticeMultiAgentSystem:
    """
    Orchestrates multiple specialized AI agents for autonomous career management
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.llm_service = LLMService()
        
        # Configure LLM for AutoGen
        self.llm_config = {
            "model": settings.DEFAULT_LLM_MODEL,
            "api_key": settings.OPENAI_API_KEY,
            "temperature": 0.7,
            "max_tokens": 2000,
        }
        
        # Initialize agents
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        
        # 1. User Proxy Agent - Represents the user and handles approvals
        self.user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            human_input_mode=settings.AUTOGEN_HUMAN_INPUT_MODE,
            max_consecutive_auto_reply=0,
            code_execution_config=False,
            system_message="You represent the user and handle approval decisions."
        )
        
        # 2. Job Researcher Agent - Searches and identifies opportunities
        self.job_researcher = autogen.AssistantAgent(
            name="JobResearcher",
            llm_config=self.llm_config,
            system_message="""You are an expert job researcher and career advisor.
            Your responsibilities:
            - Search job boards (Indeed, LinkedIn, Glassdoor) for relevant opportunities
            - Analyze job descriptions and extract requirements
            - Match opportunities with user's skills and career goals
            - Rank opportunities based on fit score
            - Identify skill gaps and learning opportunities
            
            Always be thorough and consider:
            - Job requirements vs. user qualifications
            - Salary range and location preferences
            - Company culture and growth potential
            - Remote work options and benefits
            """
        )
        
        # 3. Resume Optimizer Agent - Customizes resumes for each application
        self.resume_optimizer = autogen.AssistantAgent(
            name="ResumeOptimizer",
            llm_config=self.llm_config,
            system_message="""You are an expert resume writer and ATS optimization specialist.
            Your responsibilities:
            - Analyze job descriptions and extract key requirements
            - Customize resume bullet points to match job requirements
            - Optimize for ATS (Applicant Tracking Systems)
            - Maintain user's authentic voice and personal brand
            - Ensure measurable achievements and impact statements
            - Reorder skills based on job posting priorities
            
            Guidelines:
            - Use action verbs and quantifiable results
            - Keep bullet points concise (1-2 lines)
            - Include relevant keywords from job description
            - Never fabricate experience or skills
            - Preserve user's tone and style
            """
        )
        
        # 4. Cover Letter Writer Agent - Generates personalized cover letters
        self.cover_letter_writer = autogen.AssistantAgent(
            name="CoverLetterWriter",
            llm_config=self.llm_config,
            system_message="""You are an expert cover letter writer and communication specialist.
            Your responsibilities:
            - Write compelling, personalized cover letters for each application
            - Research the company and incorporate relevant details
            - Connect user's experience to job requirements
            - Demonstrate enthusiasm and cultural fit
            - Keep letters concise (250-400 words)
            
            Structure:
            1. Strong opening hook
            2. Relevant experience and achievements
            3. Why this company/role specifically
            4. Call to action
            
            Tone: Professional yet personable, enthusiastic, confident
            """
        )
        
        # 5. Application Manager Agent - Handles submission and tracking
        self.application_manager = autogen.AssistantAgent(
            name="ApplicationManager",
            llm_config=self.llm_config,
            system_message="""You are an application management and tracking specialist.
            Your responsibilities:
            - Coordinate the application process
            - Verify all materials are ready (resume, cover letter, portfolio)
            - Submit applications through appropriate channels
            - Track application status and follow-ups
            - Schedule interview preparation reminders
            - Manage application pipeline
            
            Always:
            - Double-check all materials before submission
            - Record submission details and confirmation
            - Set up follow-up reminders
            - Track application status changes
            """
        )
        
        # 6. Profile Updater Agent - Keeps professional profiles current
        self.profile_updater = autogen.AssistantAgent(
            name="ProfileUpdater",
            llm_config=self.llm_config,
            system_message="""You are a professional branding and profile optimization expert.
            Your responsibilities:
            - Keep LinkedIn, GitHub, and portfolio profiles up-to-date
            - Ensure consistency across all platforms
            - Optimize profile SEO for discoverability
            - Suggest profile improvements
            - Maintain personal brand integrity
            
            Platforms:
            - LinkedIn: headline, summary, experience, skills, recommendations
            - GitHub: bio, pinned repos, README profiles
            - Portfolio: projects, case studies, testimonials
            """
        )
        
        # 7. Content Creator Agent - Generates professional content
        self.content_creator = autogen.AssistantAgent(
            name="ContentCreator",
            llm_config=self.llm_config,
            system_message="""You are a content strategist and creator for professional branding.
            Your responsibilities:
            - Generate LinkedIn posts, articles, and updates
            - Create project documentation and case studies
            - Write technical blog posts
            - Develop presentation content
            - Adapt to trending topics and industry news
            
            Content types:
            - Thought leadership posts
            - Technical tutorials
            - Project showcases
            - Career insights
            - Industry commentary
            """
        )
        
        # 8. Task Orchestrator Agent - Coordinates all agents and workflows
        self.orchestrator = autogen.AssistantAgent(
            name="TaskOrchestrator",
            llm_config=self.llm_config,
            system_message="""You are the master coordinator of the Agentice system.
            Your responsibilities:
            - Coordinate between all specialist agents
            - Break down complex tasks into subtasks
            - Assign tasks to appropriate agents
            - Ensure workflow efficiency
            - Monitor progress and resolve blockers
            - Synthesize results and present to user
            
            Workflow:
            1. Understand user's goal
            2. Create execution plan
            3. Delegate to specialist agents
            4. Monitor and coordinate
            5. Quality check results
            6. Request user approval when needed
            7. Execute approved actions
            """
        )
        
        logger.info("Multi-agent system initialized", user_id=self.user_id)
    
    async def autonomous_job_search_and_apply(
        self,
        criteria: Dict[str, Any],
        max_applications: int = 10
    ) -> List[Application]:
        """
        Autonomous job search and application workflow
        
        Args:
            criteria: Job search criteria (title, location, salary, etc.)
            max_applications: Maximum number of applications to submit
            
        Returns:
            List of submitted applications
        """
        logger.info("Starting autonomous job search", criteria=criteria, max_applications=max_applications)
        
        # Create group chat for coordinated multi-agent workflow
        groupchat = autogen.GroupChat(
            agents=[
                self.orchestrator,
                self.job_researcher,
                self.resume_optimizer,
                self.cover_letter_writer,
                self.application_manager,
                self.user_proxy,
            ],
            messages=[],
            max_round=50,
        )
        
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)
        
        # Start the workflow
        initial_message = f"""
        AUTONOMOUS JOB APPLICATION WORKFLOW
        
        User ID: {self.user_id}
        Search Criteria: {criteria}
        Max Applications: {max_applications}
        
        TASK: Find and apply to relevant job opportunities
        
        WORKFLOW:
        1. JobResearcher: Search job boards and identify {max_applications} best-fit opportunities
        2. For each opportunity:
           a. ResumeOptimizer: Customize resume for the job
           b. CoverLetterWriter: Write personalized cover letter
           c. UserProxy: REQUIRE APPROVAL before submission
           d. ApplicationManager: Submit if approved
        3. Report results and next steps
        
        START NOW. JobResearcher, begin searching for opportunities.
        """
        
        self.user_proxy.initiate_chat(
            manager,
            message=initial_message
        )
        
        # Extract applications from conversation
        applications = self._extract_applications_from_chat(groupchat.messages)
        
        logger.info("Job search and application completed", applications_count=len(applications))
        
        return applications
    
    async def optimize_resume_for_job(
        self,
        job_description: str,
        current_resume: Resume
    ) -> Dict[str, Any]:
        """
        Optimize resume for a specific job
        
        Args:
            job_description: Target job description
            current_resume: User's current resume
            
        Returns:
            Optimized resume with diff and explanation
        """
        logger.info("Optimizing resume for job", resume_id=current_resume.id)
        
        message = f"""
        TASK: Optimize resume for specific job opportunity
        
        JOB DESCRIPTION:
        {job_description}
        
        CURRENT RESUME:
        {current_resume.to_text()}
        
        REQUIREMENTS:
        1. Analyze job requirements
        2. Identify matching and missing skills
        3. Reorder and rewrite bullet points to emphasize relevant experience
        4. Add keywords for ATS optimization
        5. Maintain authentic voice and truthfulness
        6. Provide before/after diff
        7. Explain changes
        
        Provide the optimized resume and detailed explanation.
        """
        
        response = self.user_proxy.initiate_chat(
            self.resume_optimizer,
            message=message
        )
        
        return self._parse_resume_optimization_response(response)
    
    async def generate_cover_letter(
        self,
        job_description: str,
        company_name: str,
        resume: Resume
    ) -> str:
        """
        Generate personalized cover letter
        
        Args:
            job_description: Job description
            company_name: Target company name
            resume: User's resume
            
        Returns:
            Cover letter text
        """
        logger.info("Generating cover letter", company=company_name)
        
        message = f"""
        TASK: Write a compelling cover letter
        
        COMPANY: {company_name}
        
        JOB DESCRIPTION:
        {job_description}
        
        MY BACKGROUND:
        {resume.to_text()}
        
        REQUIREMENTS:
        - Research the company (if possible) and mention specific details
        - Connect my experience to their requirements
        - Show enthusiasm for the role
        - Keep it concise (250-400 words)
        - Professional yet personable tone
        - Strong opening and call to action
        
        Write the cover letter now.
        """
        
        response = self.user_proxy.initiate_chat(
            self.cover_letter_writer,
            message=message
        )
        
        return self._extract_cover_letter_from_response(response)
    
    async def update_professional_profiles(
        self,
        new_experience: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update all professional profiles with new experience
        
        Args:
            new_experience: New skills, projects, or experiences
            
        Returns:
            Proposed updates for each platform
        """
        logger.info("Updating professional profiles", user_id=self.user_id)
        
        message = f"""
        TASK: Update professional profiles with new experience
        
        NEW EXPERIENCE:
        {new_experience}
        
        PLATFORMS TO UPDATE:
        1. LinkedIn (headline, summary, experience, skills)
        2. GitHub (bio, pinned repos, README)
        3. Portfolio (projects section)
        
        REQUIREMENTS:
        - Maintain consistent personal brand
        - Optimize for discoverability (SEO, keywords)
        - Quantify achievements when possible
        - Keep tone professional yet personable
        - Provide specific update recommendations for each platform
        
        Generate the updates now.
        """
        
        response = self.user_proxy.initiate_chat(
            self.profile_updater,
            message=message
        )
        
        return self._parse_profile_updates(response)
    
    async def create_professional_content(
        self,
        content_type: str,
        topic: str,
        context: Optional[str] = None
    ) -> str:
        """
        Generate professional content (posts, articles, etc.)
        
        Args:
            content_type: Type of content (linkedin_post, article, case_study, etc.)
            topic: Content topic
            context: Additional context
            
        Returns:
            Generated content
        """
        logger.info("Creating professional content", type=content_type, topic=topic)
        
        message = f"""
        TASK: Create {content_type}
        
        TOPIC: {topic}
        CONTEXT: {context or 'None'}
        
        REQUIREMENTS:
        - Engaging and professional
        - Demonstrate expertise
        - Include relevant hashtags (if LinkedIn post)
        - Proper structure and formatting
        - Call to action or discussion prompt
        - Length appropriate for platform
        
        Create the content now.
        """
        
        response = self.user_proxy.initiate_chat(
            self.content_creator,
            message=message
        )
        
        return self._extract_content_from_response(response)
    
    def _extract_applications_from_chat(self, messages: List[Dict]) -> List[Application]:
        """Extract application records from chat messages"""
        # Implementation to parse chat messages and extract application data
        applications = []
        # Parse logic here
        return applications
    
    def _parse_resume_optimization_response(self, response: Any) -> Dict[str, Any]:
        """Parse resume optimization response"""
        # Implementation to extract optimized resume and diff
        return {}
    
    def _extract_cover_letter_from_response(self, response: Any) -> str:
        """Extract cover letter from response"""
        # Implementation to extract cover letter text
        return ""
    
    def _parse_profile_updates(self, response: Any) -> Dict[str, Any]:
        """Parse profile update recommendations"""
        # Implementation to extract platform-specific updates
        return {}
    
    def _extract_content_from_response(self, response: Any) -> str:
        """Extract generated content from response"""
        # Implementation to extract content
        return ""


# Agent manager for creating and managing agent instances
class AgentManager:
    """Manages agent instances for different users"""
    
    _instances: Dict[str, AgenticeMultiAgentSystem] = {}
    
    @classmethod
    def get_agent_system(cls, user_id: str) -> AgenticeMultiAgentSystem:
        """Get or create agent system for user"""
        if user_id not in cls._instances:
            cls._instances[user_id] = AgenticeMultiAgentSystem(user_id)
        return cls._instances[user_id]
    
    @classmethod
    def remove_agent_system(cls, user_id: str):
        """Remove agent system for user"""
        if user_id in cls._instances:
            del cls._instances[user_id]
