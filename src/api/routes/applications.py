"""
FastAPI router for job applications
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from src.pipelines.job_application_pipeline import JobApplicationPipeline
from src.models.database import Application, ApplicationStatus
from src.services.application_service import ApplicationService
from src.api.dependencies import get_current_user

router = APIRouter()


class JobSearchRequest(BaseModel):
    keywords: str
    location: Optional[str] = ""
    remote_only: bool = False
    max_applications_per_day: int = 10
    search_indeed: bool = True
    search_linkedin: bool = True
    search_glassdoor: bool = False


class JobApplicationRequest(BaseModel):
    job_url: str
    company_name: str
    job_title: str
    job_description: str
    auto_submit: bool = False


class ApplicationApprovalRequest(BaseModel):
    approved: bool
    notes: Optional[str] = None


@router.post("/auto-search")
async def start_autonomous_job_search(
    request: JobSearchRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """
    Start autonomous job search and application process
    """
    
    pipeline = JobApplicationPipeline(user_id=current_user.id)
    
    # Run in background
    background_tasks.add_task(
        pipeline.run_daily_job_search,
        search_criteria=request.dict()
    )
    
    return {
        "message": "Autonomous job search started",
        "status": "processing",
        "user_id": current_user.id
    }


@router.post("/apply")
async def apply_to_job(
    request: JobApplicationRequest,
    current_user = Depends(get_current_user)
):
    """
    Apply to a specific job posting
    """
    
    pipeline = JobApplicationPipeline(user_id=current_user.id)
    
    application = await pipeline.apply_to_specific_job(
        job_url=request.job_url,
        company_name=request.company_name,
        job_title=request.job_title,
        job_description=request.job_description,
        auto_submit=request.auto_submit
    )
    
    if not application:
        raise HTTPException(status_code=500, detail="Failed to create application")
    
    return {
        "application_id": application.id,
        "status": application.status,
        "message": "Application created successfully"
    }


@router.get("/applications")
async def get_applications(
    status: Optional[ApplicationStatus] = None,
    limit: int = 50,
    current_user = Depends(get_current_user)
):
    """
    Get user's applications
    """
    
    service = ApplicationService()
    applications = await service.get_user_applications(
        user_id=current_user.id,
        status=status,
        limit=limit
    )
    
    return {
        "applications": applications,
        "count": len(applications)
    }


@router.get("/applications/{application_id}")
async def get_application(
    application_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get specific application details
    """
    
    service = ApplicationService()
    application = await service.get_application(application_id)
    
    if not application or application.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application


@router.post("/applications/{application_id}/approve")
async def approve_application(
    application_id: str,
    request: ApplicationApprovalRequest,
    current_user = Depends(get_current_user)
):
    """
    Approve or reject an application
    """
    
    service = ApplicationService()
    application = await service.get_application(application_id)
    
    if not application or application.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if request.approved:
        # Approve and submit
        result = await service.approve_and_submit(application)
        return {
            "message": "Application approved and submitted",
            "application_id": application_id,
            "status": "submitted",
            "result": result
        }
    else:
        # Reject
        await service.reject_application(application, request.notes)
        return {
            "message": "Application rejected",
            "application_id": application_id,
            "status": "rejected"
        }


@router.get("/applications/{application_id}/status")
async def get_application_status(
    application_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get real-time application status
    """
    
    service = ApplicationService()
    status = await service.check_application_status(application_id)
    
    return {
        "application_id": application_id,
        "status": status,
        "last_updated": datetime.utcnow()
    }


@router.get("/stats")
async def get_application_stats(
    current_user = Depends(get_current_user)
):
    """
    Get user's application statistics
    """
    
    service = ApplicationService()
    stats = await service.get_user_stats(current_user.id)
    
    return stats
