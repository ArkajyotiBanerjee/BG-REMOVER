from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
import asyncio

from api.bg_remover import remove_background

app = FastAPI(title="Background Remover API")

# -------------------------
# Health check
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Background removal
# -------------------------
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    image_bytes = await file.read()

    try:
        output_bytes = await asyncio.wait_for(
            asyncio.to_thread(remove_background, image_bytes),
            timeout=120  # give ML enough time
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Image processing timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Response(
        content=output_bytes,
        media_type="image/png"
    )
