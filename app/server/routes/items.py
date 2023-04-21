from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from server.models.user import UserSchema
from server.helper.login import *
from server.helper.statement import *

from server.project_database import(
    get_project,
    update_project,
)

from server.models.project import(
    ErrorResponseModel,
    ResponseModel,
    Item,
)

router = APIRouter()


@router.post("/add", response_description="Item data added to the project")
async def add_item_data(project_name: str, item: Item = Body(...), current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
            item_list.append(item)
        else:
            item_list=[item]
        data = {"items": item_list}
        data = jsonable_encoder(data)
        updated_project = await update_project(project_name, data, current_user.username)
        if updated_project:
            return ResponseModel(project, "Item data added successfully.")
        return ErrorResponseModel(
        "An error occured",
        404,
        "There was an error updating the project",
        )
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )

@router.get("/showall", response_description="Items retrieved")
async def get_all_items(project_name: str, current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
        else:
            item_list=[]
        return ResponseModel(item_list, "Items retrieved successfully")
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )

@router.get("/statement", response_description="Final statement")
async def get_statement(project_name: str, current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
        else:
            item_list=[]
        statement=get_statement_details(item_list)
        return ResponseModel(statement, "Statement retrieved successfully")
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )

@router.get("/statement/category", response_description="Category-wise statement")
async def get_statement_categorywise(project_name: str, current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
        else:
            item_list=[]
        statement=get_statement_categorywise_details(item_list)
        return ResponseModel(statement, "Statement retrieved successfully")
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )

@router.get("/statement/one_category", response_description="Category-wise statement")
async def get_statement_one_category(project_name: str, category: str, current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
        else:
            item_list=[]
        statement=get_statement_one_category_details(item_list, category)
        return ResponseModel(statement, "Statement retrieved successfully")
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )

@router.delete("/delete", response_description="Item data deleted")
async def delete_item_data(project_name: str, item_index: int, current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
            if item_index<len(item_list):
                item_list.pop(item_index)
            else:
                return ErrorResponseModel(
            "An error occured",
            404,
            "No such item to delete",
            )
        else:
            return ErrorResponseModel(
            "An error occured",
            404,
            "No such item to delete",
            )
        data = {"items": item_list}
        data = jsonable_encoder(data)
        updated_project = await update_project(project_name, data, current_user.username)
        if updated_project:
            return ResponseModel(project, "Item data deleted successfully.")
        return ErrorResponseModel(
        "An error occured",
        404,
        "There was an error updating the project",
        )
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )

@router.put("/update", response_description="Item details updated")
async def update_item_data(project_name: str, item_index: int, item: Item = Body(...), current_user: UserSchema = Depends(get_current_user)):
    project = await get_project(project_name, current_user.username)
    if project:
        item_list=None
        if "items" in project.keys():
            item_list=project["items"]
            if item_index<len(item_list):
                item_list.pop(item_index)
                item_list.append(item)
            else:
                return ErrorResponseModel(
            "An error occured",
            404,
            "No such item to update",
            )
        else:
            return ErrorResponseModel(
            "An error occured",
            404,
            "No such item to update",
            )
        data = {"items": item_list}
        data = jsonable_encoder(data)
        updated_project = await update_project(project_name, data, current_user.username)
        if updated_project:
            return ResponseModel(project, "Item data updated successfully.")
        return ErrorResponseModel(
        "An error occured",
        404,
        "There was an error updating the project",
        )
    return ErrorResponseModel(
        "An error occured",
        404,
        "Project not found",
    )