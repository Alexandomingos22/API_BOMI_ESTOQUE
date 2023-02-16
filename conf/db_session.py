from typing import Optional
import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

__async_engine: Optional[AsyncEngine] = None

def create_engine() -> AsyncEngine:
    global __async_engine
    
    if __async_engine:
        return
    
    conn_str = "postgresql+asyncpg://{}:postgres@pgsql.{}.com:5432/{}"
    __async_engine = create_async_engine(url=conn_str, echo=False) 
    
    return __async_engine

def create_session() -> AsyncSession:
    global __async_engine
    

    if not __async_engine:
        create_async_engine()
        
    __async_session = sessionmaker(__async_engine, expire_on_commit=False, class_=AsyncSession)
    
    session: AsyncSession = __async_session()
    
    return session