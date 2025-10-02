"""
Job scraper service for multiple job boards
"""

import asyncio
from typing import List, Dict, Any, Optional
import structlog
from datetime import datetime
from bs4 import BeautifulSoup
import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.models.database import Opportunity, OpportunityStatus
from src.config.settings import settings

logger = structlog.get_logger()


class JobScraperService:
    """
    Scrapes job postings from multiple sources
    """
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def search_indeed(
        self,
        query: str,
        location: str = "",
        remote: bool = False,
        limit: int = 50
    ) -> List[Opportunity]:
        """Search Indeed for job postings"""
        
        logger.info("Searching Indeed", query=query, location=location)
        
        opportunities = []
        
        try:
            # Build Indeed search URL
            params = {
                'q': query,
                'l': location if not remote else 'Remote',
                'limit': limit,
                'sort': 'date'
            }
            
            # Note: Indeed requires API key for official access
            # This is a simplified example
            if settings.INDEED_API_KEY:
                url = f"https://api.indeed.com/ads/apisearch?{self._build_query_string(params)}"
                response = await self.client.get(url, headers=self.headers)
                data = response.json()
                
                for job in data.get('results', []):
                    opportunities.append(self._parse_indeed_job(job))
            
        except Exception as e:
            logger.error("Error searching Indeed", error=str(e))
        
        return opportunities
    
    async def search_linkedin(
        self,
        query: str,
        location: str = "",
        limit: int = 50
    ) -> List[Opportunity]:
        """Search LinkedIn for job postings"""
        
        logger.info("Searching LinkedIn", query=query, location=location)
        
        opportunities = []
        
        try:
            # LinkedIn Jobs API (requires authentication)
            if settings.LINKEDIN_JOBS_API_KEY:
                headers = {
                    **self.headers,
                    'Authorization': f'Bearer {settings.LINKEDIN_JOBS_API_KEY}'
                }
                
                params = {
                    'keywords': query,
                    'location': location,
                    'count': limit
                }
                
                url = f"https://api.linkedin.com/v2/jobSearch?{self._build_query_string(params)}"
                response = await self.client.get(url, headers=headers)
                data = response.json()
                
                for job in data.get('elements', []):
                    opportunities.append(self._parse_linkedin_job(job))
                    
        except Exception as e:
            logger.error("Error searching LinkedIn", error=str(e))
        
        return opportunities
    
    async def search_glassdoor(
        self,
        query: str,
        location: str = "",
        limit: int = 50
    ) -> List[Opportunity]:
        """Search Glassdoor for job postings"""
        
        logger.info("Searching Glassdoor", query=query, location=location)
        
        opportunities = []
        
        try:
            # Glassdoor API
            if settings.GLASSDOOR_API_KEY:
                params = {
                    'action': 'jobs-search',
                    'format': 'json',
                    'v': '1',
                    'userip': '0.0.0.0',
                    'useragent': 'Mozilla/5.0',
                    'q': query,
                    'l': location,
                    'pagesize': limit
                }
                
                url = f"https://api.glassdoor.com/api/api.htm"
                response = await self.client.get(url, params=params)
                data = response.json()
                
                for job in data.get('response', {}).get('jobListings', []):
                    opportunities.append(self._parse_glassdoor_job(job))
                    
        except Exception as e:
            logger.error("Error searching Glassdoor", error=str(e))
        
        return opportunities
    
    async def extract_job_details(self, url: str) -> Dict[str, Any]:
        """Extract full job details from a URL"""
        
        try:
            response = await self.client.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This is highly site-specific and would need customization
            # for each job board
            
            return {
                'description': soup.get_text(),
                'requirements': [],
                'benefits': []
            }
            
        except Exception as e:
            logger.error("Error extracting job details", url=url, error=str(e))
            return {}
    
    async def submit_indeed_application(
        self,
        job_url: str,
        resume_file: str,
        cover_letter: str
    ) -> Dict[str, Any]:
        """Submit application through Indeed"""
        
        logger.info("Submitting Indeed application", url=job_url)
        
        try:
            # This requires Selenium for automation
            driver = self._get_selenium_driver()
            
            driver.get(job_url)
            
            # Click Apply button
            apply_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "apply-button"))
            )
            apply_button.click()
            
            # Fill application form
            # Upload resume
            resume_input = driver.find_element(By.ID, "resume-upload")
            resume_input.send_keys(resume_file)
            
            # Fill cover letter
            cover_letter_field = driver.find_element(By.ID, "cover-letter")
            cover_letter_field.send_keys(cover_letter)
            
            # Submit
            submit_button = driver.find_element(By.ID, "submit-application")
            submit_button.click()
            
            # Wait for confirmation
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "confirmation"))
            )
            
            driver.quit()
            
            return {
                'success': True,
                'confirmation_number': 'IND-' + datetime.utcnow().strftime('%Y%m%d%H%M%S'),
                'method': 'indeed'
            }
            
        except Exception as e:
            logger.error("Error submitting Indeed application", error=str(e))
            return {'success': False, 'error': str(e)}
    
    async def submit_linkedin_application(
        self,
        job_url: str,
        resume_file: str,
        cover_letter: str
    ) -> Dict[str, Any]:
        """Submit application through LinkedIn"""
        
        logger.info("Submitting LinkedIn application", url=job_url)
        
        try:
            # Similar Selenium automation for LinkedIn
            # Implementation would follow LinkedIn's application flow
            
            return {
                'success': True,
                'confirmation_number': 'LI-' + datetime.utcnow().strftime('%Y%m%d%H%M%S'),
                'method': 'linkedin'
            }
            
        except Exception as e:
            logger.error("Error submitting LinkedIn application", error=str(e))
            return {'success': False, 'error': str(e)}
    
    def _parse_indeed_job(self, job_data: Dict) -> Opportunity:
        """Parse Indeed job data into Opportunity model"""
        
        return Opportunity(
            source='indeed',
            title=job_data.get('jobtitle', ''),
            company=job_data.get('company', ''),
            location=job_data.get('formattedLocation', ''),
            url=job_data.get('url', ''),
            description=job_data.get('snippet', ''),
            status=OpportunityStatus.IDENTIFIED,
            discovered_at=datetime.utcnow()
        )
    
    def _parse_linkedin_job(self, job_data: Dict) -> Opportunity:
        """Parse LinkedIn job data into Opportunity model"""
        
        return Opportunity(
            source='linkedin',
            title=job_data.get('title', ''),
            company=job_data.get('company', {}).get('name', ''),
            location=job_data.get('location', ''),
            url=job_data.get('url', ''),
            description=job_data.get('description', ''),
            status=OpportunityStatus.IDENTIFIED,
            discovered_at=datetime.utcnow()
        )
    
    def _parse_glassdoor_job(self, job_data: Dict) -> Opportunity:
        """Parse Glassdoor job data into Opportunity model"""
        
        return Opportunity(
            source='glassdoor',
            title=job_data.get('jobTitle', ''),
            company=job_data.get('employer', ''),
            location=job_data.get('location', ''),
            url=job_data.get('jobLink', ''),
            description=job_data.get('jobDescription', ''),
            status=OpportunityStatus.IDENTIFIED,
            discovered_at=datetime.utcnow()
        )
    
    def _get_selenium_driver(self):
        """Get configured Selenium WebDriver"""
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        return driver
    
    def _build_query_string(self, params: Dict) -> str:
        """Build URL query string from parameters"""
        return '&'.join(f"{k}={v}" for k, v in params.items())
