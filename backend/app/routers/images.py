"""
Image serving endpoint
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

router = APIRouter()


@router.get("/{file_path:path}")
async def get_image(file_path: str):
    """
    Serve uploaded images
    
    Security: Only serves files from the uploads directory
    """
    # Prevent directory traversal attacks
    if ".." in file_path or file_path.startswith("/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file path"
        )
    
    file_full_path = Path(UPLOAD_DIR) / file_path
    
    # Ensure file is within upload directory
    try:
        file_full_path.resolve().relative_to(Path(UPLOAD_DIR).resolve())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if not file_full_path.exists() or not file_full_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return FileResponse(file_full_path)

