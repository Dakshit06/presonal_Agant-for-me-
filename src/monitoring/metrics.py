"""
Monitoring and metrics setup
"""

from prometheus_client import Counter, Histogram, Gauge
from fastapi import FastAPI


# Define metrics
applications_submitted = Counter('applications_submitted_total', 'Total applications submitted')
applications_approved = Counter('applications_approved_total', 'Total applications approved')
job_search_duration = Histogram('job_search_duration_seconds', 'Time spent searching for jobs')
active_users = Gauge('active_users', 'Number of active users')


def setup_metrics(app: FastAPI):
    """Setup Prometheus metrics for the application"""
    
    # Metrics are automatically collected by prometheus_client
    pass
