<<<<<<< HEAD
# Sweet Shop Management System

A full-stack application for managing a sweet shop, built with TDD principles. This system allows users to browse, search, and purchase sweets, while administrators can manage inventory.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (can be easily configured for PostgreSQL)
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest, pytest-asyncio

### Frontend
- **Framework**: React with TypeScript
- **Styling**: CSS Modules / Modern CSS
- **State Management**: React Hooks
- **HTTP Client**: Axios

## Project Structure

```
.
├── backend/          # FastAPI backend application
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── sweets.py
│   │   │   └── inventory.py
│   │   └── tests/
│   └── requirements.txt
├── frontend/         # React frontend application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

5. (Optional) Create an admin user:
```bash
python scripts/create_admin.py
```

This will prompt you to enter username, email, and password for an admin user who can manage sweets and inventory.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `GET /api/auth/me` - Get current authenticated user information

### Sweets (Protected)
- `POST /api/sweets` - Add a new sweet (Admin)
- `GET /api/sweets` - List all sweets
- `GET /api/sweets/search` - Search sweets by name, category, or price range
- `PUT /api/sweets/{id}` - Update a sweet (Admin)
- `DELETE /api/sweets/{id}` - Delete a sweet (Admin)

### Inventory (Protected)
- `POST /api/sweets/{id}/purchase` - Purchase a sweet (decrease quantity)
- `POST /api/sweets/{id}/restock` - Restock a sweet (Admin)

## Running Tests

### Backend Tests
```bash
cd backend
pytest
```

To run with verbose output:
```bash
pytest -v
```

To run a specific test file:
```bash
pytest app/tests/test_auth.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Test Coverage

The backend includes comprehensive test coverage for:
- Authentication (registration, login, token validation)
- Sweet CRUD operations (create, read, update, delete)
- Search functionality (by name, category, price range)
- Inventory management (purchase, restock)
- Admin-only endpoints and authorization
- Error handling and edge cases

Test coverage reports can be generated using pytest-cov (add to requirements.txt if needed):
```bash
pytest --cov=app --cov-report=html
```

## My AI Usage

### AI Tools Used
- **Cursor AI** - Used in the development process for assisstance in code, refactoring, and debugging
- **GitHub Copilot** - Assisted with boilerplate code, test generation, and code suggestions

### How AI Was Used

1. **Project Structure Setup**: Used AI to generate the initial project structure  for FastAPI and React applications.

2. **Test Generation**: Leveraged AI to generate comprehensive test cases following TDD principles, including:
   - Authentication endpoint tests
   - CRUD operation tests for sweets
   - Inventory management tests
   - Edge cases and error handling tests

3. **Code Implementation**: AI assisted with:
   - FastAPI route handlers and dependency injection
   - Database models and schemas
   - JWT authentication implementation
   - React components and hooks
   - API service layer for frontend-backend communication

4. **Debugging**: Used AI to identify and fix bugs in:
   - JWT token handling
   - Database queries
   - Frontend state management
   - API response handling

5. **Documentation**: AI helped generate:
   - README structure and content
   - Code comments and docstrings
   - API documentation

### Reflection on AI Impact

AI tools significantly accelerated the development process by:
- **Reducing Boilerplate**: Quickly generating repetitive code structures, allowing focus on business logic
- **Test Coverage**: Ensuring comprehensive test cases that might have been overlooked
- **Best Practices**: Suggesting modern patterns and following framework conventions
- **Learning**: Providing explanations for complex concepts and suggesting alternative approaches

However, it was crucial to:
- **Review all generated code** to ensure it fits the specific requirements
- **Understand the logic** behind AI suggestions before accepting them
- **Maintain code quality** by refactoring AI-generated code when needed
- **Follow TDD principles** by writing tests first, even when AI could generate implementation

The use of AI was a powerful augmentation tool, but the architecture decisions, business logic understanding, and overall system design were human-driven, ensuring the solution meets the specific requirements of the Sweet Shop Management System.

## Screenshots

<img width="1874" height="888" alt="Sweet-shop1" src="https://github.com/user-attachments/assets/12fd6079-e1f8-46df-80e0-df1d413ce4ac" />
<img width="1796" height="835" alt="Register1" src="https://github.com/user-attachments/assets/ca8fd51c-7dec-4ec2-8626-a1237a97c121" />
<img width="1800" height="880" alt="Register 2" src="https://github.com/user-attachments/assets/9e9d5ce1-c827-454c-98fc-32d4d312bad3" />
<img width="1802" height="787" alt="SS-Login" src="https://github.com/user-attachments/assets/a93b5840-22e6-487f-bfed-bb103788d1ce" />
<img width="1805" height="767" alt="Login 2" src="https://github.com/user-attachments/assets/c65872b1-52f7-49d1-91de-49831493d52c" />
<img width="1800" height="852" alt="Login 3" src="https://github.com/user-attachments/assets/1281c287-ede2-4012-bd64-645548f9dc59" />
<img width="1831" height="881" alt="Create sweet" src="https://github.com/user-attachments/assets/65f20c9e-cc26-459f-a5d2-512664715eab" />
<img width="1802" height="843" alt="Creation successfull" src="https://github.com/user-attachments/assets/8fbd2235-d4c6-4b92-85a3-235299e892c1" />
 <img width="1799" height="852" alt="Search Sweet" src="https://github.com/user-attachments/assets/5c1bdc8a-2119-4a3a-813d-2ac8817407c4" />
<img width="1800" height="840" alt="Sweet search successful" src="https://github.com/user-attachments/assets/44b34428-3c2a-405a-bd64-41fdac6ad084" />
<img width="1801" height="741" alt="Sweets" src="https://github.com/user-attachments/assets/43a0e1d0-5c13-420e-9cf8-32cd12c5b1ba" />
<img width="1799" height="496" alt="Get sweet" src="https://github.com/user-attachments/assets/6d40e690-26d3-483a-99d4-c915857e815c" />
<img width="1793" height="741" alt="Get sweet successful" src="https://github.com/user-attachments/assets/5d5e77b9-855f-4165-a1cf-c681e87600a7" />
<img width="1795" height="861" alt="Update sweet" src="https://github.com/user-attachments/assets/e46a9855-94d8-49b6-9380-6b2cf2dbe61e" />
<img width="1799" height="675" alt="Update Response" src="https://github.com/user-attachments/assets/85c2f672-4fce-4aff-939b-257f39118a78" />
<img width="1800" height="616" alt="Delete sweet" src="https://github.com/user-attachments/assets/c23d6d0a-8786-442f-8b07-31b1e4e7d622" />
<img width="1799" height="711" alt="Delete sweet (2)" src="https://github.com/user-attachments/assets/af5a1dcb-49a3-406b-8f6f-f93100e0cb42" />
<img width="1803" height="861" alt="Purchase sweet" src="https://github.com/user-attachments/assets/7e871554-9293-4663-a60e-95af039b7221" />
<img width="1800" height="766" alt="Restock sweet" src="https://github.com/user-attachments/assets/0f9e3596-b495-4543-8423-4aba493bf7af" />





## Future Enhancements

- User role management UI
- Sweet categories management
- Order history
- Shopping cart functionality
- Payment integration
- Admin analytics dashboard



=======
# Sweet-Shop
The goal of this kata is to design, build, and test a full-stack Sweet Shop Management  System. This project involves API development, database management,  frontend implementation, testing, and modern development workflows.
>>>>>>> 0c0bcdb44305acc4240a4e54440781b778bdde46
