from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import FRONTEND_URL, HOST, PORT, NODE_ENV

# Import routes
from routes import auth, products, orders

app = FastAPI(
    title="E-Commerce API",
    description="Modern E-Commerce API with FastAPI",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/api/health")
async def health_check():
    return {
        "status": "Server is running without issues",
        "environment": NODE_ENV
    }

# Include routes
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")

# 404 handler
@app.get("/api")
async def api_root():
    return {
        "message": "E-Commerce API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=(NODE_ENV == "development")
    )
