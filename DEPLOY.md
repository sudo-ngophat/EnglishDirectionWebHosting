# Deploy lên GitHub Pages

Site là static HTML/CSS/JS, không cần build. Có thể host thẳng trên GitHub Pages.

## Bước 1 — Tạo repo và push

```bash
cd e:/ENGLISH_TECHER_TUNG/site
git init
git add .
git commit -m "initial: static learning site with pre-rendered vocab audio"
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

## Bước 2 — Bật GitHub Pages

1. Vào **Settings → Pages** của repo.
2. Source: **Deploy from a branch**.
3. Branch: `main`, folder: `/ (root)`.
4. Save. Sau 1–2 phút site sẽ ở `https://<user>.github.io/<repo>/`.

## Cấu trúc audio

- `audio/vocab/buoi-N/<word>.wav` — 173 file WAV Kokoro pre-render (đã có sẵn).
- `audio/vocab/manifest.json` — bản đồ `{ "buoi-N": { "<word>": "<url>" } }`.

Trình duyệt sẽ tự tải file WAV theo manifest. Nếu file lỗi hoặc thiếu, tự động rơi về:
1. `audio/human/manifest.json` (nếu có bản thu tay)
2. Web Speech API của trình duyệt (fallback cuối)

Không cần chạy Kokoro server khi đã deploy.

## Cập nhật thêm từ vựng

Khi thêm buổi mới vào `js/pronunciation-data.js`:

```bash
# 1. Bật Kokoro server local
cd ../kokoro-main/kokoro-main
.venv/Scripts/uvicorn teacher_tts.api.app:create_app --factory --host 127.0.0.1 --port 8000

# 2. Render WAV cho buổi mới (ví dụ buổi 21)
cd ../../site
python scripts/render_vocab_audio.py --only 21

# 3. Commit và push
git add audio/vocab/buoi-21 audio/vocab/manifest.json js/pronunciation-data.js
git commit -m "add vocab buoi-21"
git push
```

## Kiểm tra trên điện thoại

- Mở URL GitHub Pages trong Chrome/Safari điện thoại.
- Nhấn “Nghe” trong drill/pronunciation/review-mix — audio phát mượt qua WAV cache của trình duyệt.
- Nhận diện giọng nói (mic) chỉ hoạt động trên Chrome/Edge có mạng.
