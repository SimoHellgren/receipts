import os

import uvicorn
from backend.app.api import app


if __name__ == '__main__':
    os.environ['MODE'] = 'DEV'
    uvicorn.run("run_api_dev_mode:app", host="0.0.0.0", port=8000, reload=True)
    del os.environ['MODE']
