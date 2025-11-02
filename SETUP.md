# Quick Start Guide

## Initial Setup

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Set up Backend**:
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Set up Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Create Admin User** (optional):
   ```bash
   cd backend
   python scripts/create_admin.py
   ```

## First Steps

1. Open `http://localhost:3000` in your browser
2. Register a new user account
3. Login with your credentials
4. (If you created an admin) You'll see admin controls for managing sweets
5. (If regular user) Browse and purchase sweets

## Testing

Run backend tests:
```bash
cd backend
pytest -v
```

## Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.8+

### Frontend won't start
- Ensure Node.js 16+ is installed
- Try deleting `node_modules` and running `npm install` again
- Check that backend is running on port 8000

### Database issues
- Delete `backend/sweet_shop.db` to reset the database
- Restart the backend server

### CORS errors
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend/app/main.py`

