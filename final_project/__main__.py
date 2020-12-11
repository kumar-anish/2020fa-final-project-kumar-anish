import uvicorn as uv

if __name__ == "__main__":
    uv.run("QueryLog:app", host='127.0.0.1', port=8080, reload=True)
