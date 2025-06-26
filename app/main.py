from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
import qrcode

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, QR Generator!"}

class QRRequest(BaseModel):
    payload: str

@app.post("/generate")
async def generate_qr(request: QRRequest):
    if not request.payload.strip():
        raise HTTPException(status_code=400, detail="`payload` must be a non-empty string")

    img = qrcode.make(request.payload)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
