from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from routers import bets, user, results

app = FastAPI()

# Include routers
app.include_router(user.router)
app.include_router(bets.router)
app.include_router(results.router)

# Allow all origins
origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


# CUSTOMIZE OPENAPI
# https://fastapi.tiangolo.com/advanced/extending-openapi/

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="F1 BETTING",
        version="1.0.0",
        description="An API to do bets with your friends about F1 race results!",
        license_info={
            "name": "MIT",
            "url": "https://github.com/niek-o/F1Betting/blob/main/LICENSE.md"
        },
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/New_era_F1_logo.png"
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# SET FUNCTION NAME AS OPERATION ID
# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid

def function_name_as_operation_id(fast_api: FastAPI):
    for route in fast_api.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


function_name_as_operation_id(app)

app.openapi = custom_openapi
