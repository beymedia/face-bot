import io
import numpy as np
import face_recognition
from PIL import Image

# Eyni şəxs üçün tipik məsafə ~0.6-dan aşağıdır. Daha ciddi yoxlama üçün 0.5 seçin.
MATCH_THRESHOLD = 0.5


def extract_single_embedding(image_bytes: bytes) -> tuple[list[float] | None, str]:
    """
    Şəkildən tam bir üz çıxarır.
    Qayıdır: (embedding, xəta mesajı). Uğurlu olarsa xəta mesajı boşdur.
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(img)

    locations = face_recognition.face_locations(arr, model="hog")

    if len(locations) == 0:
        return None, "Şəkildə üz tapılmadı."
    if len(locations) > 1:
        return None, "Şəkildə bir neçə üz var. Yalnız öz üzünüzün olduğu şəkil göndərin."

    encodings = face_recognition.face_encodings(arr, known_face_locations=locations)
    return encodings[0].tolist(), ""


def is_same_person(stored: list[float], candidate: list[float]) -> tuple[bool, float]:
    dist = face_recognition.face_distance(
        [np.array(stored)], np.array(candidate)
    )[0]
    return bool(dist <= MATCH_THRESHOLD), float(dist)
