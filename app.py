from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    url = request.form.get("url")

    if not url or url.strip() == "":
        return "❌ Enter a valid URL"

    return "✅ Link looks good!"


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    if not url or url.strip() == "":
        return "❌ Please enter a valid video URL"

    unique_id = str(uuid.uuid4())
    output = os.path.join(DOWNLOAD_FOLDER, f"%(title)s_{unique_id}.%(ext)s")

    # 🔥 FIX: NO FFMPEG NEEDED
    ydl_opts = {
        'format': 'best[ext=mp4]/best',   # ✅ single file (no merge)
        'outtmpl': output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        title = info.get("title", "video") + "." + info.get("ext", "mp4")

        return send_file(
            filename,
            as_attachment=True,
            download_name=title
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"


# 🚀 DEPLOY READY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
