from fastapi import FastAPI

from backend.routers import config, rtls, authentication, simulator

app = FastAPI(
    title="TFM",
    version="0.1",
    description="Indoor positioning web services for the master thesis project",
    docs_url="/docs",
)

app.include_router(config.router, tags=["config"])
app.include_router(rtls.router, tags=["rtls"])
app.include_router(authentication.router, tags=["authentication"])
app.include_router(simulator.router, tags=["simulator"])

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    import os
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 9999))
    log_level = os.getenv("LOG_LEVEL", "debug").lower()

    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level=log_level)
