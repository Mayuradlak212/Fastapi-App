from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import requests
import asyncio
import aiohttp
from typing import Optional

routes = APIRouter(prefix="/api", tags=["data"])


@routes.get("/posts")
async def get_posts():
    """Fetch all posts from DummyJSON API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://dummyjson.com/posts",
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Posts fetched successfully",
                        "data": data.get("posts", []),
                        "total": data.get("total", 0)
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch posts: {response.status}",
                        "data": []
                    })
                    
    except aiohttp.ClientError as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Network error: {str(e)}",
            "data": []
        })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": []
        })


@routes.get("/posts/{post_id}")
async def get_post_by_id(post_id: int):
    """Fetch a specific post by ID"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://dummyjson.com/posts/{post_id}",
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Post fetched successfully",
                        "data": data
                    })
                elif response.status == 404:
                    return JSONResponse({
                        "status_code": 404,
                        "success": False,
                        "message": "Post not found",
                        "data": None
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch post: {response.status}",
                        "data": None
                    })
                    
    except aiohttp.ClientError as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Network error: {str(e)}",
            "data": None
        })
    except ValueError:
        return JSONResponse({
            "status_code": 400,
            "success": False,
            "message": "Invalid post ID",
            "data": None
        })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": None
        })


@routes.get("/products")
async def get_products(limit: Optional[int] = None, skip: Optional[int] = None):
    """Fetch all products from DummyJSON API with optional pagination"""
    try:
        url = "https://dummyjson.com/products"
        params = {}
        
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
            
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=params,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Products fetched successfully",
                        "data": data.get("products", []),
                        "total": data.get("total", 0),
                        "skip": data.get("skip", 0),
                        "limit": data.get("limit", 30)
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch products: {response.status}",
                        "data": []
                    })
                    
    except aiohttp.ClientError as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Network error: {str(e)}",
            "data": []
        })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": []
        })


@routes.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    """Fetch a specific product by ID"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://dummyjson.com/products/{product_id}",
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Product fetched successfully",
                        "data": data
                    })
                elif response.status == 404:
                    return JSONResponse({
                        "status_code": 404,
                        "success": False,
                        "message": "Product not found",
                        "data": None
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch product: {response.status}",
                        "data": None
                    })
                    
    except aiohttp.ClientError as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Network error: {str(e)}",
            "data": None
        })
    except ValueError:
        return JSONResponse({
            "status_code": 400,
            "success": False,
            "message": "Invalid product ID",
            "data": None
        })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": None
        })


@routes.get("/users")
async def get_users(limit: Optional[int] = None, skip: Optional[int] = None):
    """Fetch all users from DummyJSON API with optional pagination"""
    try:
        url = "https://dummyjson.com/users"
        params = {}
        
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
            
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=params,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Users fetched successfully",
                        "data": data.get("users", []),
                        "total": data.get("total", 0),
                        "skip": data.get("skip", 0),
                        "limit": data.get("limit", 30)
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch users: {response.status}",
                        "data": []
                    })
                    
    except aiohttp.ClientError as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Network error: {str(e)}",
            "data": []
        })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": []
        })


@routes.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    """Fetch a specific user by ID"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://dummyjson.com/users/{user_id}",
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "User fetched successfully",
                        "data": data
                    })
                elif response.status == 404:
                    return JSONResponse({
                        "status_code": 404,
                        "success": False,
                        "message": "User not found",
                        "data": None
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch user: {response.status}",
                        "data": None
                    })
                    
    except aiohttp.ClientError as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Network error: {str(e)}",
            "data": None
        })
    except ValueError:
        return JSONResponse({
            "status_code": 400,
            "success": False,
            "message": "Invalid user ID",
            "data": None
        })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": None
        })