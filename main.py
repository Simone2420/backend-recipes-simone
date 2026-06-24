
from fastapi import FastAPI
from config.database import engine, Base
from routers import auth, recipes, ingredients, comments, users, roles

# Create tables (Alembic should handle migrations, but this is for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipes API", version="1.0.0", description="API for managing recipes with authentication")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["Recipes"])
app.include_router(ingredients.router, prefix="/api/v1/ingredients", tags=["Ingredients"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["Comments"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Roles & Permissions"])

@app.get("/")
def root():
    return {"message": "Recipes API is running!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

