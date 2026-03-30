#!/usr/bin/env python3

import argparse
import sys
import subprocess
import json
import os
import shutil

def run_yt_dlp(args):
    return subprocess.run(
        [sys.executable, "-m", "yt_dlp"] + args,
        capture_output=True,
        text=True
    )

def check_yt_dlp():
    try:
        result = run_yt_dlp(["--version"])
        if result.returncode != 0:
            raise Exception()
    except:
        print("📦 Instalando yt-dlp...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            check=True
        )

def find_ffmpeg():
    """Tenta localizar ffmpeg no sistema"""
    paths = [
        "ffmpeg",
        "ffmpeg.exe",
        os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe"),
        r"C:\Users\joel\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe",
    ]
    for path in paths:
        if shutil.which(path) or os.path.exists(path):
            return path
    return None

def normalize_url(url):
    """Corrige URLs de Shorts automaticamente"""
    if "youtube.com/shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def get_video_info(url):
    result = run_yt_dlp([
        "--dump-json",
        "--no-playlist",
        url
    ])
    if result.returncode != 0:
        raise Exception(result.stderr)
    return json.loads(result.stdout)

def convert_to_mp3(filepath, ffmpeg_path):
    """Converte qualquer arquivo de vídeo/áudio para MP3 usando ffmpeg diretamente"""
    mp3_path = os.path.splitext(filepath)[0] + ".mp3"

    print(f"\n🔄 Convertendo para MP3: {os.path.basename(mp3_path)}")

    result = subprocess.run(
        [ffmpeg_path, "-i", filepath, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", mp3_path, "-y"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"⚠️ Erro na conversão: {result.stderr}")
        return None

    os.remove(filepath)
    print(f"✅ MP3 salvo: {mp3_path}")
    return mp3_path

def find_downloaded_file(output_path, title):
    """Localiza o arquivo baixado mais recente na pasta de output"""
    files = [
        os.path.join(output_path, f)
        for f in os.listdir(output_path)
        if not f.endswith(".mp3") and not f.endswith(".part")
    ]
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def download_video(url, output_path="downloads", audio_only=False):
    check_yt_dlp()
    url = normalize_url(url)
    os.makedirs(output_path, exist_ok=True)

    ffmpeg_path = find_ffmpeg()

    if not ffmpeg_path:
        print("⚠️ FFmpeg não encontrado! Instale com: winget install ffmpeg")
        raise Exception("FFmpeg é obrigatório para converter para MP3")

    print(f"🎬 FFmpeg encontrado: {ffmpeg_path}")

    if audio_only:
        cmd = [
            "-f", "bestaudio",
            "--no-playlist",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            url
        ]
    else:
        cmd = [
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "--no-playlist",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            url
        ]

    print(f"\n📥 Downloading: {url}")
    print(f"📁 Output: {os.path.abspath(output_path)}\n")

    try:
        info = get_video_info(url)
        title = info.get("title", "")
        print(f"🎵 Title: {title}")
        print(f"📺 Channel: {info.get('uploader')}\n")

        result = run_yt_dlp(cmd)

        if result.returncode != 0:
            print(result.stderr)
            raise Exception("Falha no download")

        downloaded_file = find_downloaded_file(output_path, title)
        if not downloaded_file:
            raise Exception("Arquivo baixado não encontrado para conversão")

        mp3_file = convert_to_mp3(downloaded_file, ffmpeg_path)
        if not mp3_file:
            raise Exception("Falha na conversão para MP3")

        print("\n✅ Download + conversão para MP3 concluídos!")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-o", "--output", default="downloads")
    parser.add_argument("-a", "--audio-only", action="store_true")
    args = parser.parse_args()

    success = download_video(
        url=args.url,
        output_path=args.output,
        audio_only=args.audio_only
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()