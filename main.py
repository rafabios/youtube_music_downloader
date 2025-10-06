import os
import ssl
import pandas as pd
import yt_dlp
from tqdm import tqdm

# Configurações
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/1xZbHiiZdgzTNYUxG8Lzs-UwRupYu2_/export?format=csv"
OUTPUT_DIR = "output"
HISTORICO_FILE = "historico.txt"

# Corrige SSL (caso necessário)
ssl._create_default_https_context = ssl._create_unverified_context

def carregar_historico():
    if os.path.exists(HISTORICO_FILE):
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()

def salvar_historico(musica):
    with open(HISTORICO_FILE, "a", encoding="utf-8") as f:
        f.write(musica + "\n")

def baixar_musica(url, genero, nome_arquivo, historico):
    filename = f"{nome_arquivo}.mp3"
    if filename in historico:
        print(f"⏭️ Já existe no histórico: {filename}")
        return None

    genero_dir = os.path.join(OUTPUT_DIR, genero)
    os.makedirs(genero_dir, exist_ok=True)
    filepath = os.path.join(genero_dir, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "bestaudio/best",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Baixado: {genero} - {filename}")
        salvar_historico(filename)
    except Exception as e:
        print(f"❌ Erro ao baixar {nome_arquivo}: {e}")

def processar_documentos():
    print("🔄 Baixando planilha...")
    df = pd.read_csv(GOOGLE_SHEET_CSV)
    historico = carregar_historico()
    print(f"🎵 {len(df)} músicas encontradas na planilha.")

    for _, row in tqdm(df.iterrows(), total=len(df)):
        nome = row.get("Nome", "").strip()
        url = row.get("URL", "").strip()
        genero = row.get("Gênero", "Outros").strip()
        if not url or not nome:
            continue
        baixar_musica(url, genero, nome, historico)

if __name__ == "__main__":
    processar_documentos()
