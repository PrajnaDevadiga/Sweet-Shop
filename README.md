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
- **Cursor AI** - Used throughout the development process for code generation, refactoring, and debugging
- **GitHub Copilot** - Assisted with boilerplate code, test generation, and code suggestions

### How AI Was Used

1. **Project Structure Setup**: Used AI to generate the initial project structure and boilerplate code for FastAPI and React applications.

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

_Screenshots will be added once the application is fully implemented and running._

## Future Enhancements

- User role management UI
- Sweet categories management
- Order history
- Shopping cart functionality
- Payment integration
- Admin analytics dashboard

## License

This project is created as part of an assessment.

=======
# Sweet-Shop
The goal of this kata is to design, build, and test a full-stack Sweet Shop Management  System. This project involves API development, database management,  frontend implementation, testing, and modern development workflows.
>>>>>>> 0c0bcdb44305acc4240a4e54440781b778bdde46
