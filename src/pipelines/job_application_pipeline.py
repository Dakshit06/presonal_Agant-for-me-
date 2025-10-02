"""
Job Application Automation Pipeline
End-to-end workflow for autonomous job applications
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import structlog
import asyncio

from src.agents.simple_agents import AgentManager
from src.models.database import Opportunity, OpportunityStatus, Application, ApplicationStatus, Resume
from src.services.job_scraper_service import JobScraperService
from src.services.resume_service import ResumeService
from src.services.application_service import ApplicationService
from src.services.notification_service import NotificationService
from src.database.session import get_db

logger = structlog.get_logger()


class JobApplicationPipeline:
    """
    Orchestrates the end-to-end job application workflow:
    1. Search for opportunities
    2. Match with user profile
    3. Customize resume and cover letter
    4. Request approval
    5. Submit application
    6. Track status and follow-ups
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.agent_system = AgentManager.get_agent_system(user_id)
        self.job_scraper = JobScraperService()
        self.resume_service = ResumeService()
        self.application_service = ApplicationService()
        self.notification_service = NotificationService()
    
    async def run_daily_job_search(
        self,
        search_criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Daily automated job search and application workflow
        
        Args:
            search_criteria: Override default search criteria
            
        Returns:
            Summary of applications submitted
        """
        logger.info("Starting daily job search", user_id=self.user_id)
        
        try:
            # 1. Get user preferences and criteria
            criteria = search_criteria or await self._get_user_search_criteria()
            
            # 2. Search for opportunities across multiple platforms
            opportunities = await self._search_opportunities(criteria)
            logger.info(f"Found {len(opportunities)} opportunities")
            
            # 3. Score and rank opportunities
            ranked_opportunities = await self._rank_opportunities(opportunities)
            
            # 4. Filter to top N opportunities
            top_opportunities = ranked_opportunities[:criteria.get('max_applications_per_day', 10)]
            
            # 5. Process each opportunity
            applications = []
            for opportunity in top_opportunities:
                try:
                    application = await self._process_opportunity(opportunity)
                    if application:
                        applications.append(application)
                except Exception as e:
                    logger.error(f"Error processing opportunity", opportunity_id=opportunity.id, error=str(e))
                    continue
            
            # 6. Send summary to user
            await self._send_daily_summary(applications)
            
            return {
                "opportunities_found": len(opportunities),
                "applications_submitted": len(applications),
                "applications": [app.dict() for app in applications],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Error in daily job search", error=str(e))
            raise
    
    async def apply_to_specific_job(
        self,
        job_url: str,
        company_name: str,
        job_title: str,
        job_description: str,
        auto_submit: bool = False
    ) -> Application:
        """
        Apply to a specific job posting
        
        Args:
            job_url: URL of the job posting
            company_name: Company name
            job_title: Job title
            job_description: Full job description
            auto_submit: If True, submit without approval (requires user setting)
            
        Returns:
            Application record
        """
        logger.info("Applying to specific job", company=company_name, title=job_title)
        
        # Create opportunity record
        opportunity = Opportunity(
            user_id=self.user_id,
            source="manual",
            title=job_title,
            company=company_name,
            url=job_url,
            description=job_description,
            status=OpportunityStatus.IDENTIFIED
        )
        
        # Save opportunity
        async with get_db() as db:
            db.add(opportunity)
            await db.commit()
            await db.refresh(opportunity)
        
        # Process the opportunity
        application = await self._process_opportunity(opportunity, auto_submit=auto_submit)
        
        return application
    
    async def _search_opportunities(self, criteria: Dict[str, Any]) -> List[Opportunity]:
        """Search for job opportunities across multiple platforms"""
        
        all_opportunities = []
        
        # Search Indeed
        if criteria.get('search_indeed', True):
            indeed_jobs = await self.job_scraper.search_indeed(
                query=criteria.get('keywords', ''),
                location=criteria.get('location', ''),
                remote=criteria.get('remote_only', False)
            )
            all_opportunities.extend(indeed_jobs)
        
        # Search LinkedIn
        if criteria.get('search_linkedin', True):
            linkedin_jobs = await self.job_scraper.search_linkedin(
                query=criteria.get('keywords', ''),
                location=criteria.get('location', '')
            )
            all_opportunities.extend(linkedin_jobs)
        
        # Search Glassdoor
        if criteria.get('search_glassdoor', False):
            glassdoor_jobs = await self.job_scraper.search_glassdoor(
                query=criteria.get('keywords', ''),
                location=criteria.get('location', '')
            )
            all_opportunities.extend(glassdoor_jobs)
        
        # Remove duplicates
        unique_opportunities = self._deduplicate_opportunities(all_opportunities)
        
        return unique_opportunities
    
    async def _rank_opportunities(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """
        Rank opportunities based on fit score
        
        Scoring factors:
        - Skills match
        - Experience match
        - Salary range
        - Location preference
        - Company culture fit
        - Growth potential
        """
        
        # Get user profile and resume
        user_resume = await self.resume_service.get_current_resume(self.user_id)
        
        # Score each opportunity
        for opportunity in opportunities:
            score = await self._calculate_fit_score(opportunity, user_resume)
            opportunity.fit_score = score
        
        # Sort by fit score
        ranked = sorted(opportunities, key=lambda x: x.fit_score or 0, reverse=True)
        
        return ranked
    
    async def _process_opportunity(
        self,
        opportunity: Opportunity,
        auto_submit: bool = False
    ) -> Optional[Application]:
        """
        Process a single opportunity: customize materials, get approval, submit
        
        Args:
            opportunity: Opportunity to apply to
            auto_submit: Skip approval if enabled
            
        Returns:
            Application record if submitted, None otherwise
        """
        logger.info("Processing opportunity", opportunity_id=opportunity.id, company=opportunity.company)
        
        try:
            # 1. Get user's base resume
            base_resume = await self.resume_service.get_current_resume(self.user_id)
            
            # 2. Customize resume for this job
            logger.info("Customizing resume")
            customized_resume = await self.agent_system.optimize_resume_for_job(
                job_description=opportunity.description,
                current_resume=base_resume
            )
            
            # 3. Generate cover letter
            logger.info("Generating cover letter")
            cover_letter = await self.agent_system.generate_cover_letter(
                job_description=opportunity.description,
                company_name=opportunity.company,
                resume=base_resume
            )
            
            # 4. Create application record
            application = Application(
                user_id=self.user_id,
                opportunity_id=opportunity.id,
                resume_variant=customized_resume,
                cover_letter=cover_letter,
                status=ApplicationStatus.DRAFT,
                created_at=datetime.utcnow()
            )
            
            # Save draft application
            async with get_db() as db:
                db.add(application)
                await db.commit()
                await db.refresh(application)
            
            # 5. Request approval (unless auto_submit is enabled)
            if not auto_submit:
                approved = await self._request_approval(application)
                if not approved:
                    logger.info("Application not approved", application_id=application.id)
                    application.status = ApplicationStatus.REJECTED
                    await self.application_service.update_application(application)
                    return None
            
            # 6. Submit application
            logger.info("Submitting application", application_id=application.id)
            submission_result = await self._submit_application(application, opportunity)
            
            if submission_result['success']:
                application.status = ApplicationStatus.SUBMITTED
                application.submitted_at = datetime.utcnow()
                application.confirmation_number = submission_result.get('confirmation_number')
                
                # Update opportunity status
                opportunity.status = OpportunityStatus.APPLIED
                
                await self.application_service.update_application(application)
                
                # Schedule follow-up reminders
                await self._schedule_followups(application)
                
                logger.info("Application submitted successfully", application_id=application.id)
                return application
            else:
                logger.error("Application submission failed", error=submission_result.get('error'))
                application.status = ApplicationStatus.FAILED
                await self.application_service.update_application(application)
                return None
                
        except Exception as e:
            logger.error("Error processing opportunity", error=str(e))
            return None
    
    async def _calculate_fit_score(
        self,
        opportunity: Opportunity,
        resume: Resume
    ) -> float:
        """
        Calculate how well the opportunity matches the user's profile
        
        Returns:
            Float between 0.0 and 1.0
        """
        
        # Use LLM to calculate fit score
        prompt = f"""
        Analyze how well this job opportunity matches the candidate's profile.
        
        JOB OPPORTUNITY:
        Title: {opportunity.title}
        Company: {opportunity.company}
        Description: {opportunity.description}
        
        CANDIDATE RESUME:
        {resume.to_text()}
        
        Consider:
        - Skills match (required vs. candidate's skills)
        - Experience level match
        - Domain expertise
        - Education requirements
        - Location/remote preference
        
        Provide a fit score between 0.0 and 1.0, where:
        - 1.0 = Perfect match
        - 0.8-0.9 = Excellent match
        - 0.6-0.7 = Good match
        - 0.4-0.5 = Moderate match
        - Below 0.4 = Poor match
        
        Return only the numeric score.
        """
        
        # Get score from LLM
        # Implementation here
        score = 0.75  # Placeholder
        
        return score
    
    async def _request_approval(self, application: Application) -> bool:
        """
        Request user approval for application submission
        
        Returns:
            True if approved, False otherwise
        """
        
        # Send notification to user with application details
        await self.notification_service.send_approval_request(
            user_id=self.user_id,
            application_id=application.id,
            message=f"Review and approve application to {application.opportunity.company}"
        )
        
        # Wait for user response (timeout after 24 hours)
        approval = await self.application_service.wait_for_approval(
            application.id,
            timeout_hours=24
        )
        
        return approval
    
    async def _submit_application(
        self,
        application: Application,
        opportunity: Opportunity
    ) -> Dict[str, Any]:
        """
        Submit the application through the appropriate channel
        
        Returns:
            Submission result with success status and details
        """
        
        try:
            # Determine submission method based on source
            if opportunity.source == 'indeed':
                result = await self.job_scraper.submit_indeed_application(
                    job_url=opportunity.url,
                    resume_file=application.resume_variant['file_path'],
                    cover_letter=application.cover_letter
                )
            elif opportunity.source == 'linkedin':
                result = await self.job_scraper.submit_linkedin_application(
                    job_url=opportunity.url,
                    resume_file=application.resume_variant['file_path'],
                    cover_letter=application.cover_letter
                )
            else:
                # Manual application - just save materials
                result = {
                    'success': True,
                    'method': 'manual',
                    'message': 'Application materials prepared. Manual submission required.'
                }
            
            return result
            
        except Exception as e:
            logger.error("Application submission error", error=str(e))
            return {'success': False, 'error': str(e)}
    
    async def _schedule_followups(self, application: Application):
        """Schedule follow-up reminders for the application"""
        
        from src.config.settings import settings
        
        for days in settings.APPLICATION_FOLLOWUP_DAYS:
            await self.notification_service.schedule_reminder(
                user_id=self.user_id,
                application_id=application.id,
                days_from_now=days,
                message=f"Follow up on application to {application.opportunity.company}"
            )
    
    async def _send_daily_summary(self, applications: List[Application]):
        """Send daily summary of applications to user"""
        
        summary = f"""
        Daily Job Application Summary
        
        Applications Submitted: {len(applications)}
        
        Details:
        """
        
        for app in applications:
            summary += f"\n- {app.opportunity.title} at {app.opportunity.company}"
        
        await self.notification_service.send_email(
            user_id=self.user_id,
            subject="Your Daily Job Application Summary",
            body=summary
        )
    
    async def _get_user_search_criteria(self) -> Dict[str, Any]:
        """Get user's job search criteria from profile"""
        
        # Fetch from user preferences
        # Placeholder implementation
        return {
            'keywords': 'software engineer python',
            'location': 'Remote',
            'remote_only': True,
            'max_applications_per_day': 5,
            'search_indeed': True,
            'search_linkedin': True,
            'search_glassdoor': False
        }
    
    def _deduplicate_opportunities(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Remove duplicate opportunities based on URL and title"""
        
        seen = set()
        unique = []
        
        for opp in opportunities:
            key = (opp.url, opp.title, opp.company)
            if key not in seen:
                seen.add(key)
                unique.append(opp)
        
        return unique


# Celery task for automated daily job search
async def run_daily_job_search_for_all_users():
    """Run daily job search for all users with auto-apply enabled"""
    
    from src.models.database import User
    
    async with get_db() as db:
        # Get all users with auto-apply enabled
        users = await db.query(User).filter(User.auto_apply_enabled == True).all()
        
        for user in users:
            try:
                pipeline = JobApplicationPipeline(user.id)
                await pipeline.run_daily_job_search()
            except Exception as e:
                logger.error(f"Error in daily job search for user", user_id=user.id, error=str(e))
                continue
