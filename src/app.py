import uvicorn
from uvicorn.config import LOG_LEVELS

from src import env
from src.configs import configure_app
from src.core.utils import arg_util
from src.server import create_app

DEBUG_ARG = "DEBUG"

configure_app()
app = create_app()

if __name__ == "__main__":
    is_debug = arg_util.get_arg(DEBUG_ARG) == "True"

    if is_debug:
        log_level = LOG_LEVELS["debug"]
        reload = True
    else:
        log_level = LOG_LEVELS["info"]  # Default log level
        reload = False

    uvicorn.run(
        "src.app:app",
        host=env.SERVER_HOST,
        port=env.SERVER_PORT,
        reload=reload,
        log_level=log_level,
    )
