from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import datetime

app = FastAPI()

# Укажи реальный путь, если хочешь лог в файл
LOG_FILE = "log.csv"


def resolve_redirect_url(ad_id: str, link_type: str) -> str:
    if link_type == "photos":
        return f"https://drive.google.com/drive/folders/{ad_id}"
    elif link_type == "map":
        return f"https://www.google.com/maps/search/?api=1&query={ad_id}"
    elif link_type == "contact":
        return "https://t.me/Oleg_apt_BA"
    return "https://google.com"


@app.get("/track")
async def track(request: Request, id: str = "", type: str = ""):
    ip = request.client.host
    now = datetime.datetime.now().isoformat()

    log_line = f"{now},{ip},{id},{type}\n"
    print(log_line)

    # лог в файл (опционально)
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    redirect_url = resolve_redirect_url(id, type)
    return RedirectResponse(url=redirect_url)
