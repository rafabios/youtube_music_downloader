import os
import ssl
import pandas as pd
import yt_dlp
from tqdm import tqdm
import librosa
import numpy as np
import gc

# Configurações
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/1xZbHiiZdgzTNYUxG8Lzs-UwRupYu2_/export?format=csv"
OUTPUT_DIR = "output"
QUALITY_AUDIO = "320"
HISTORICO_FILE = "historico.txt"
BAIXADOS_FILE = "baixados.txt"

# Ignorar erros SSL
ssl._create_default_https_context = ssl._create_unverified_context
os.makedirs(OUTPUT_DIR, exist_ok=True)


def carregar_historico():
    if os.path.exists(HISTORICO_FILE):
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()


def salvar_historico(nome_musica):
    with open(HISTORICO_FILE, "a", encoding="utf-8") as f:
        f.write(nome_musica + "\n")


def salvar_baixados(lista):
    with open(BAIXADOS_FILE, "w", encoding="utf-8") as f:
        for item in lista:
            f.write(item + "\n")


def detectar_bpm(filepath):
    try:
        # Limita a leitura para os primeiros 120 segundos para reduzir uso de memória
        y, sr = librosa.load(filepath, sr=None, duration=120)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        if isinstance(tempo, (list, np.ndarray)):
            tempo = tempo[0] if len(tempo) > 0 else None

        if tempo:
            return int(round(float(tempo)))
        else:
            return None
    except Exception as e:
        print(f"⚠️ Não foi possível detectar BPM em {filepath}: {e}")
        return None


def baixar_musica(query, artist, title, genero, historico):
    safe_artist = artist.replace("/", "-")
    safe_title = title.replace("/", "-")
    safe_genero = genero.replace("/", "-") if genero else ""

    base_name = f"{safe_genero} - {safe_artist} - {safe_title}".strip(" -")
    filename = f"{base_name}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    if filename in historico:
        print(f"⏭️ Já existe no histórico: {filename}")
        return None

    genero_dir = os.path.join(OUTPUT_DIR, safe_genero if safe_genero else "Sem_Genero")
    os.makedirs(genero_dir, exist_ok=True)
    output_path = os.path.join(genero_dir, base_name + ".%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": QUALITY_AUDIO,
        }],
        "no_check_certificate": True,
        "embed_metadata": True,
        "add_metadata": True,
        "embed_thumbnail": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query}"])

        final_path = os.path.join(genero_dir, filename)
        if not os.path.exists(final_path):
            alt_path = final_path.replace(".mp3", ".mp3.mp3")
            if os.path.exists(alt_path):
                os.rename(alt_path, final_path)

        if not os.path.exists(final_path):
            print(f"❌ Arquivo não encontrado após download: {final_path}")
            return None

        bpm = detectar_bpm(final_path)
        if bpm:
            novo_nome = final_path.replace(".mp3", f" ({bpm} BPM).mp3")
            os.rename(final_path, novo_nome)
            final_path = novo_nome
            print(f"🎚️ BPM detectado: {bpm}")

        nome_final = os.path.basename(final_path)
        salvar_historico(nome_final)
        print(f"✅ Baixado: {nome_final}")

        # Libera memória após cada música
        gc.collect()

        return nome_final

    except Exception as e:
        print(f"❌ Erro ao baixar '{query}': {e}")
        return None


def main():
    print("🔄 Baixando planilha...")
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV)
    except Exception as e:
        print(f"❌ Erro ao baixar a planilha: {e}")
        return

    total = len(df)
    baixados = []
    historico = carregar_historico()

    print(f"🎵 {total} músicas encontradas na planilha.\n")

    for idx, row in tqdm(df.iterrows(), total=total, desc="Baixando músicas", unit="música"):
        artist = str(row.get("Artista", "")).strip()
        title = str(row.get("Musica", "")).strip()
        genero = str(row.get("(opcional) Tag/Genero", "")).strip()

        if not artist or not title:
            print(f"⚠️ Linha {idx+1} ignorada: dados incompletos")
            continue

        query = f"{artist} {title} extended"
        baixado = baixar_musica(query, artist, title, genero, historico)
        if baixado:
            baixados.append(baixado)

    salvar_baixados(baixados)
    print(f"\n🎉 Download concluído: {len(baixados)}/{total} músicas baixadas nesta execução.")
    print(f"📝 Lista salva em {BAIXADOS_FILE}")


if __name__ == "__main__":
    main()
