# Design Document

## Overview

This design configures a Flask API with an HTML frontend for deployment on Vercel. The solution uses Vercel's serverless functions for the API backend while serving the HTML frontend as a static file. The key challenge is ensuring proper routing between the frontend and API endpoints while maintaining CORS compatibility.

## Architecture

### Deployment Structure
```
├── api/
│   └── index.py          # Vercel serverless function (Flask app)
├── public/
│   └── index.html        # Frontend moved to public directory
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── [existing files]      # Matching/, JSONs/, etc.
```

### Request Flow
1. User accesses root URL → Vercel serves `public/index.html`
2. Frontend makes API calls to `/api/*` → Vercel routes to `api/index.py`
3. Flask app processes requests and returns JSON responses
4. Frontend displays results

## Components and Interfaces

### Vercel Configuration (`vercel.json`)
- **Purpose**: Define routing rules and build settings
- **Routes**: 
  - Static files served from `public/`
  - API routes prefixed with `/api/` routed to serverless function
- **Build**: Specify Python runtime and dependencies

### Serverless Function (`api/index.py`)
- **Purpose**: Wrap Flask application for Vercel compatibility
- **Handler**: Export Flask app as `app` variable for Vercel
- **CORS**: Configure to allow frontend domain requests
- **File Handling**: Adapt for serverless environment constraints

### Frontend Updates (`public/index.html`)
- **API Endpoints**: Update fetch URLs to use `/api/` prefix
- **Error Handling**: Maintain existing error handling logic
- **File Uploads**: Ensure FormData compatibility with serverless functions

### Dependencies Management
- **requirements.txt**: Include Flask, Flask-CORS, and existing dependencies
- **Vercel Runtime**: Use Python 3.9+ runtime
- **Package Installation**: Automatic via Vercel build process

## Data Models

### Request/Response Format
- Maintain existing API contract:
  - `POST /api/match_vaga` with FormData containing `descricao`
  - `POST /api/match_vagas` with FormData containing `file`
- Response format remains JSON as currently implemented

### File Upload Handling
- **Temporary Storage**: Use Vercel's `/tmp` directory for file processing
- **Memory Limits**: Consider Vercel's 1024MB memory limit for large files
- **Processing Time**: Ensure operations complete within 10-second timeout

## Error Handling

### CORS Issues
- **Solution**: Implement Flask-CORS with appropriate origins
- **Development**: Allow localhost origins for local testing
- **Production**: Configure specific domain origins

### Serverless Constraints
- **Cold Starts**: Optimize imports and initialization
- **Memory Management**: Handle large JSON files efficiently
- **Timeout Handling**: Implement appropriate error responses for long operations

### File Upload Errors
- **Size Limits**: Validate file sizes before processing
- **Format Validation**: Ensure JSON files are properly formatted
- **Error Messages**: Provide clear feedback for upload failures

## Testing Strategy

### Local Development
1. **Flask Development Server**: Test API endpoints locally
2. **Static File Serving**: Use local server to test frontend
3. **Integration Testing**: Verify API calls work with local setup

### Vercel Deployment Testing
1. **Preview Deployments**: Use Vercel preview URLs for testing
2. **API Endpoint Testing**: Verify all routes work in serverless environment
3. **File Upload Testing**: Test with various file sizes and formats
4. **CORS Validation**: Ensure cross-origin requests work correctly

### Performance Testing
1. **Cold Start Optimization**: Measure and optimize function startup time
2. **Memory Usage**: Monitor memory consumption with large files
3. **Response Times**: Ensure acceptable performance for matching operations