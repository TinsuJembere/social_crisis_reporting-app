"""
Service for creating notifications
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Notification, Issue, IssueStatus


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    issue_id: Optional[int] = None
) -> Notification:
    """
    Create a new notification
    """
    notification = Notification(
        user_id=user_id,
        issue_id=issue_id,
        title=title,
        message=message,
        is_read=False
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def notify_issue_status_change(
    db: Session,
    issue: Issue,
    old_status: IssueStatus,
    new_status: IssueStatus
) -> None:
    """
    Create notification when issue status changes
    """
    if old_status == new_status:
        return
    
    status_messages = {
        IssueStatus.PENDING: "is pending review",
        IssueStatus.IN_PROGRESS: "is now in progress",
        IssueStatus.RESOLVED: "has been resolved",
        IssueStatus.CLOSED: "has been closed"
    }
    
    message = status_messages.get(new_status, f"status changed to {new_status.value}")
    
    create_notification(
        db=db,
        user_id=issue.reporter_id,
        title=f"Issue Status Update: {issue.title}",
        message=f"Your issue '{issue.title}' {message}.",
        issue_id=issue.id
    )

