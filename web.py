"""
To run the web app:
1. open terminal
2. cd into the same directory as this file
3. run "pyenv activate DisasterResponse"
4. run "uvicorn web:app --reload"
"""
from app import create_app
app = create_app()    
