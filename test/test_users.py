from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from routers import users
from common.conn import Base
from common.conn import engine, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:1234@localhost:3306/accountbook"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

@pytest.fixture(scope="session")
def test_db_session():
    sess = Session(bind=engine)
    try:
        yield sess
    finally:
        sess.close()

@pytest.fixture
def test_app() -> TestClient:
    with TestClient(app=app) as client:
        yield client

def test_create_user_fail(test_app: TestClient, test_db_session: Session):
    test_user = {
                    "email": "test@test.com",
                    "password1": "1234",
                    "password2": "1234"
                }
    test_db_session.add(test_user)
    test_db_session.commit()
    
    response = test_app.post(
        "/users/create",
        json={"email": "test@test.com", "password1": "1234", "password2": "12"},
    )  
    
    assert response.status_code == 422
    assert response.json() == {
                                "detail": [
                                    {
                                        "loc": [
                                            "body",
                                            "password2"
                                        ],
                                        "msg": "비밀번호가 일치하지 않습니다",
                                        "type": "value_error"
                                    }
                                ]
                            }
    
def test_create_user_success(test_app: TestClient, test_db_session: Session):
    test_user = {
                    "email": "test@test.com",
                    "password1": "1234",
                    "password2": "1234"
                }
    test_db_session.add(test_user)
    test_db_session.commit()
    
    response = test_app.post(
        "/users/create",
        json={"email": "test@test.com", "password1": "1234", "password2": "1234"},
    )
    
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["id"] == 1