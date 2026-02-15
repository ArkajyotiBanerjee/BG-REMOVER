from rembg import remove

def remove_background(image_bytes: bytes) -> bytes:
    """
    Removes background from image bytes and returns PNG bytes.
    The model is cached internally by rembg after first load.
    """
    return remove(image_bytes)
