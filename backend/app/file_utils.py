"""
File upload utilities for handling images
"""
import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import shutil
from dotenv import load_dotenv

load_dotenv()

# Configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "5242880"))  # 5MB default
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif"}

# Create upload directory if it doesn't exist
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file"""
    # Check file extension
    file_ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file content type. Only images are allowed."
        )


async def save_uploaded_image(file: UploadFile, issue_id: int) -> str:
    """
    Save uploaded image and return the file path relative to upload directory
    
    Args:
        file: Uploaded file
        issue_id: ID of the issue this image belongs to
    
    Returns:
        Relative file path (e.g., "issues/1/uuid-filename.jpg")
    """
    # Validate file
    validate_image_file(file)
    
    # Generate unique filename
    file_ext = file.filename.split(".")[-1].lower() if file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    
    # Create issue-specific directory
    issue_dir = Path(UPLOAD_DIR) / "issues" / str(issue_id)
    issue_dir.mkdir(parents=True, exist_ok=True)
    
    # Full file path
    file_path = issue_dir / unique_filename
    
    # Read and validate image
    try:
        # Read file content
        contents = await file.read()
        
        # Check file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
            )
        
        # Validate image with PIL
        from io import BytesIO
        image = Image.open(BytesIO(contents))
        image.verify()  # Verify it's a valid image
        
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        # Return relative path for database storage
        return f"issues/{issue_id}/{unique_filename}"
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up on error
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing image: {str(e)}"
        )


def get_image_url(image_path: str, base_url: str = "") -> str:
    """
    Get the full URL for an image
    
    Args:
        image_path: Relative path stored in database
        base_url: Base URL of the API (e.g., "http://localhost:8000")
    
    Returns:
        Full URL to access the image
    """
    if not image_path:
        return None
    
    if base_url:
        return f"{base_url.rstrip('/')}/api/images/{image_path}"
    return f"/api/images/{image_path}"


def delete_image_file(image_path: str) -> None:
    """
    Delete an image file from the filesystem
    
    Args:
        image_path: Relative path stored in database
    """
    if not image_path:
        return
    
    file_path = Path(UPLOAD_DIR) / image_path
    if file_path.exists():
        file_path.unlink()
        
        # Try to remove parent directory if empty
        parent_dir = file_path.parent
        if parent_dir.exists() and not any(parent_dir.iterdir()):
            parent_dir.rmdir()

