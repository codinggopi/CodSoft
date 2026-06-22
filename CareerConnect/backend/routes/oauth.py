import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from datetime import timedelta
from urllib.parse import urlencode

import database, models, auth

router = APIRouter(prefix="/auth", tags=["OAuth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://careerconnect-online.netlify.app")
BACKEND_URL = os.getenv("BACKEND_URL", "https://careerconnect-navy.vercel.app")
OAUTH_REDIRECT_URI_BASE = BACKEND_URL

def get_frontend_redirect_url(token: str, role: str):
    return f"{FRONTEND_URL}/?token={token}&role={role}"

@router.get("/google")
def login_google():
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    redirect_uri = f"{OAUTH_REDIRECT_URI_BASE}/auth/google/callback"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(database.get_db)):
    redirect_uri = f"{OAUTH_REDIRECT_URI_BASE}/auth/google/callback"
    
    # Exchange code for token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }
    
    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=token_data)
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to authenticate with Google")
        
        access_token = token_res.json().get("access_token")
        
        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_res = await client.get(user_info_url, headers=headers)
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")
        
        user_data = user_res.json()
    
    email = user_data.get("email")
    name = user_data.get("name")
    picture = user_data.get("picture")
    google_id = user_data.get("sub")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email not provided by Google")
        
    return process_oauth_user(db, email, name, picture, "google", google_id)

@router.get("/linkedin")
def login_linkedin():
    if not LINKEDIN_CLIENT_ID:
        raise HTTPException(status_code=500, detail="LinkedIn OAuth not configured")
    
    redirect_uri = f"{OAUTH_REDIRECT_URI_BASE}/auth/linkedin/callback"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "r_liteprofile r_emailaddress",
    }
    url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/linkedin/callback")
async def linkedin_callback(code: str, db: Session = Depends(database.get_db)):
    redirect_uri = f"{OAUTH_REDIRECT_URI_BASE}/auth/linkedin/callback"
    
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }
    
    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=token_data)
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to authenticate with LinkedIn")
        
        access_token = token_res.json().get("access_token")
        
        # Get user profile
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_url = "https://api.linkedin.com/v2/me"
        profile_res = await client.get(profile_url, headers=headers)
        
        email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
        email_res = await client.get(email_url, headers=headers)
        
        if profile_res.status_code != 200 or email_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from LinkedIn")
            
        profile_data = profile_res.json()
        email_data = email_res.json()
        
    # Extract fields (LinkedIn API response structure depends on specific version/scopes, this is a common structure)
    try:
        email = email_data["elements"][0]["handle~"]["emailAddress"]
        first_name = profile_data["localizedFirstName"]
        last_name = profile_data["localizedLastName"]
        name = f"{first_name} {last_name}"
        linkedin_id = profile_data["id"]
        # Profile picture might be available via a different projection, omit for now or fetch if available
        picture = None 
    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="Unexpected LinkedIn profile data format")

    return process_oauth_user(db, email, name, picture, "linkedin", linkedin_id)

def process_oauth_user(db: Session, email: str, name: str, picture: str, provider: str, provider_id: str):
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if user:
        # Update existing user with OAuth info if needed
        if not user.oauth_provider:
            user.oauth_provider = provider
            user.oauth_id = provider_id
            if picture and not user.profile_picture:
                user.profile_picture = picture
            db.commit()
    else:
        # Create new user
        user = models.User(
            name=name,
            email=email,
            role="candidate", # Default role for new OAuth users
            oauth_provider=provider,
            oauth_id=provider_id,
            profile_picture=picture
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Generate token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    
    # Redirect to frontend with token
    redirect_url = get_frontend_redirect_url(access_token, user.role)
    return RedirectResponse(url=redirect_url)
