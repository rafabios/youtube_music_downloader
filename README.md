# 🎵 Script de Download Automático de Músicas

Este script automatiza o download de músicas listadas em uma planilha do Google Sheets usando o **yt-dlp**.

## 📋 Como funciona

1. O script baixa uma planilha CSV hospedada no Google Sheets.
2. Cada linha deve conter as colunas:
   - **Nome** → Nome do arquivo (sem .mp3)
   - **URL** → Link do vídeo/música (YouTube, SoundCloud, etc.)
   - **Gênero** → Pasta onde a música será salva
3. Cada música baixada é registrada em `historico.txt`.
4. O script **não baixa novamente** arquivos que já estão no histórico.

## 🧰 Estrutura dos arquivos

```
musica_downloader/
├── main.py
├── requirements.txt
├── README.md
└── historico.txt  (gerado automaticamente)
```

---

## 💻 Instalação e uso

### 🔹 Windows

1. **Instale o Python** (versão 3.9 ou superior):
   - Baixe em [python.org/downloads](https://www.python.org/downloads/)
   - Durante a instalação, marque a opção **“Add Python to PATH”**

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script**
   ```bash
   python main.py
   ```

### 🔹 Linux / macOS

1. **Instale o Python e pip** (caso não tenha):
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script**
   ```bash
   python3 main.py
   ```

---

## 🧾 Histórico

O arquivo `historico.txt` é atualizado automaticamente sempre que uma música é baixada com sucesso.  
Ele contém apenas o nome dos arquivos já baixados, garantindo que não sejam baixados novamente.

---

## 🧩 Requisitos adicionais

- `ffmpeg` deve estar instalado no sistema (necessário para converter áudio).

### Instalação do ffmpeg

#### Windows
Baixe o executável em: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
Adicione a pasta `bin` do ffmpeg ao PATH.

#### Linux
```bash
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

---

## 🧠 Dica

Você pode automatizar o script para rodar periodicamente:
- **Windows:** usar o *Agendador de Tarefas*
- **Linux/macOS:** adicionar no `crontab`

Exemplo de crontab para rodar a cada hora:
```bash
0 * * * * /usr/bin/python3 /caminho/para/musica_downloader/main.py
```

---

Feito com ❤️ para automatizar seus downloads musicais!
