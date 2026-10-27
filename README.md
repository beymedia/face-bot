# face-bot

Telegram bot ilə razılığa əsaslanan üz yoxlaması. İstifadəçi yalnız öz üzünü qeydiyyatdan keçirir və öz şəkli ilə yoxlama aparır.

## Komandalar

- `/start` - məlumat
- `/register` - öz üzünüzü qeydiyyatdan keçirin
- `/verify` - öz şəklinizlə yoxlayın
- `/delete` - saxlanılan məlumatı silin

## Texnologiyalar

- Python 3.11
- python-telegram-bot
- face_recognition (dlib)
- Render (hosting)

## Quraşdırma

1. Telegram-da @BotFather-dən token alın.
2. Render-də Web Service yaradın və bu repo-nu bağlayın.
3. Environment Variables bölməsinə əlavə edin:
   - `BOT_TOKEN` - BotFather tokeni
   - `PUBLIC_URL` - Render-in verdiyi URL
4. Deploy edin.

## Məxfilik

Şəkillər saxlanılmır. Yalnız rəqəmsal üz xüsusiyyətləri (embedding) saxlanılır. İstifadəçi `/delete` ilə məlumatını silə bilər.
