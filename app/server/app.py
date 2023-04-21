from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from server.models.user import UserSchema, ChangePassword, ResponseModel, ErrorResponseModel
from server.routes.project import router as ProjectRouter
from server.routes.items import router as ItemRouter
from server.helper.login import *
from server.user_database import add_user, get_users, change_password

app = FastAPI()
app.include_router(ProjectRouter, tags=["Project"], prefix="/project")
app.include_router(ItemRouter, tags=["Item"], prefix="/item")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/", tags=["Root"])
async def read_root(token: str = Depends(oauth2_scheme)):
    return {"message":"Welcome to Constuction Cost estimator", "token": token}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/user/register")
async def add_user_data(user: UserSchema = Body(...)):
    user.hashed_password=get_hashed_password(user.hashed_password)
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    if new_user:
        return ResponseModel(new_user, "New user added successfully.")
    return ErrorResponseModel(
        "An error occured",
        404,
        "There was an error adding the user",)

@app.get("/user/me", response_model=UserSchema)
async def read_user(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user

@app.put("/user/changepass")
async def update_password(new_pass: ChangePassword = Body(...), current_user: UserSchema = Depends(get_current_active_user)):
    if new_pass.username == current_user.username:
        new_pass.new_password=get_hashed_password(new_pass.new_password)
        if verify_password(new_pass.old_password, current_user.hashed_password):
            new_user = await change_password(new_pass.new_password, current_user.username)
            if new_user:
                return ResponseModel("Success!", "Password changed successfully")
            return ErrorResponseModel(
            "An error occured",
            404,
            "There was an error with helper function",)
        return ErrorResponseModel(
        "An error occured",
        404,
        "Incorrect password",)
    return ErrorResponseModel(
    "An error occured",
    404,
    "There was an error changing the password",)
