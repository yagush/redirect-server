from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# === Google Sheets Авторизация ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gs_client = gspread.authorize(creds)

# === Конфигурация Google Таблицы ===
SPREADSHEET_ID = "1EZuVAZPEWcTNsGWV2pN2I5YiXWaNb08non20fO2ST_0"

@app.get("/track")
async def track_click(id: str = "", type: str = "", sheet: str = "Sheet_1", request: Request = None):
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # Текущее время в Аргентине
    argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    timestamp = datetime.now(argentina_tz).strftime("%Y-%m-%d %H:%M:%S")

    try:
        worksheet = gs_client.open_by_key(SPREADSHEET_ID).worksheet(sheet)
    except Exception as e:
        return {"error": f"Ошибка при доступе к листу '{sheet}': {str(e)}"}

    # 🔹 Запись строки в таблицу
    worksheet.append_row([
        timestamp,
        ip,
        type,
        id,
        user_agent
    ])

    # 🔁 Редирект по типу ссылки
    if type == "map":
        return RedirectResponse(f"https://www.google.com/maps/search/?api=1&query={id}")
    elif type == "photos":
        return RedirectResponse(id)
    elif type == "contact":
        return RedirectResponse(id if id.startswith("http") else "https://t.me/Oleg_apt_BA")

    # 🔁 Запасной редирект
    return RedirectResponse("https://google.com")
