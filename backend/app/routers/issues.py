"""
Issue CRUD endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Issue, IssueCategory, IssueStatus
from app.schemas import IssueCreate, IssueUpdate, IssueResponse
from app.utils import get_current_active_user, get_current_admin_user
from app.file_utils import save_uploaded_image, get_image_url, delete_image_file
from fastapi import Request

router = APIRouter()


@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    request: Request,
    title: str,
    description: str,
    category: IssueCategory,
    latitude: float,
    longitude: float,
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Create a new issue report
    
    - **title**: Title of the issue
    - **description**: Detailed description
    - **category**: Category (infrastructure, safety, environment, health, other)
    - **latitude**: Latitude coordinate
    - **longitude**: Longitude coordinate
    - **image**: Optional image file (jpg, png, gif)
    """
    # Create issue first
    new_issue = Issue(
        title=title,
        description=description,
        category=category,
        latitude=latitude,
        longitude=longitude,
        reporter_id=current_user.id
    )
    
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    
    # Handle image upload if provided
    if image:
        try:
            image_path = await save_uploaded_image(image, new_issue.id)
            new_issue.image_url = image_path
            
            db.commit()
            db.refresh(new_issue)
        except Exception as e:
            # If image upload fails, delete the issue
            db.delete(new_issue)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error uploading image: {str(e)}"
            )
    
    # Convert image path to full URL for response
    base_url = str(request.base_url).rstrip('/')
    if new_issue.image_url:
        new_issue.image_url = get_image_url(new_issue.image_url, base_url)
    
    return new_issue


@router.get("/", response_model=List[IssueResponse])
async def get_all_issues(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[IssueCategory] = None,
    status: Optional[IssueStatus] = None,
    db: Session = Depends(get_db)
):
    """
    Get all issues with optional filtering
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **category**: Filter by category
    - **status**: Filter by status
    """
    query = db.query(Issue)
    
    # Apply filters
    if category:
        query = query.filter(Issue.category == category)
    if status:
        query = query.filter(Issue.status == status)
    
    # Order by created_at descending (newest first)
    query = query.order_by(Issue.created_at.desc())
    
    # Apply pagination
    issues = query.offset(skip).limit(limit).all()
    
    # Convert image paths to full URLs
    base_url = str(request.base_url).rstrip('/')
    for issue in issues:
        if issue.image_url:
            issue.image_url = get_image_url(issue.image_url, base_url)
    
    return issues


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue_by_id(
    issue_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get a specific issue by ID
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    # Convert image path to full URL
    base_url = str(request.base_url).rstrip('/')
    if issue.image_url:
        issue.image_url = get_image_url(issue.image_url, base_url)
    
    return issue


@router.patch("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: int,
    issue_update: IssueUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update an issue
    
    Users can only update their own issues (except status).
    Only admins can update status.
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    # Check permissions
    from app.models import UserRole
    is_admin = current_user.role == UserRole.ADMIN
    is_owner = issue.reporter_id == current_user.id
    
    # Only admins can update status
    if issue_update.status is not None and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update issue status"
        )
    
    # Only owner or admin can update
    if not is_owner and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own issues"
        )
    
    # Track status change for notifications
    old_status = issue.status
    
    # Update fields
    update_data = issue_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(issue, field, value)
    
    db.commit()
    db.refresh(issue)
    
    # Create notification for status change
    if 'status' in update_data and old_status != issue.status:
        notify_issue_status_change(db, issue, old_status, issue.status)
    
    # Convert image path to full URL
    base_url = str(request.base_url).rstrip('/')
    if issue.image_url:
        issue.image_url = get_image_url(issue.image_url, base_url)
    
    return issue


@router.put("/{issue_id}/status", response_model=IssueResponse)
async def update_issue_status(
    issue_id: int,
    new_status: IssueStatus,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update issue status (Admin only)
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    old_status = issue.status
    issue.status = new_status
    db.commit()
    db.refresh(issue)
    
    # Create notification for status change
    if old_status != new_status:
        notify_issue_status_change(db, issue, old_status, new_status)
    
    # Convert image path to full URL
    base_url = str(request.base_url).rstrip('/')
    if issue.image_url:
        issue.image_url = get_image_url(issue.image_url, base_url)
    
    return issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Delete an issue (Admin only)
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    # Delete associated image if exists
    if issue.image_url:
        delete_image_file(issue.image_url)
    
    db.delete(issue)
    db.commit()
    
    return None

