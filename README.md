🎵 Music Downloader Automático (via Google Sheets)
==================================================

Baixe suas músicas de qualquer lugar do mundo 🌍 — direto da nuvem!
Este script conecta-se a uma planilha do Google Sheets, lê as faixas que você cadastrou (com nome do artista, música e gênero) e faz o download automático do áudio com qualidade de estúdio (320 kbps).
Perfeito para quem quer manter sua coleção de músicas sempre atualizada — seja no seu computador, NAS, ou até direto no seu servidor.

--------------------------------------------------
🚀 Funcionalidades
--------------------------------------------------


- Baixa músicas do YouTube automaticamente (via `yt_dlp`)  
- Lê a lista diretamente de uma planilha Google pública  
- Cria subpastas por **gênero musical** dentro da pasta `output/`  
- Detecta automaticamente o **BPM** (batidas por minuto)  
- Mantém um histórico das músicas baixadas para evitar duplicatas  
- Funciona em Windows, Linux ou macOS
--------------------------------------------------
🧩 Estrutura da planilha no Google Sheets
--------------------------------------------------

Crie uma planilha com as seguintes colunas:


| Artista | Musica | (opcional) Tag/Genero |
|---------|--------|----------------------|
| Adam Port | Afro House | House |
| Vintage Culture | It Is What It Is | Tech House |
| Illusionize | Groove Delight | Bass House |

--------------------------------------------------
☁️ Como criar e compartilhar a planilha no Google Sheets
--------------------------------------------------

1. Vá para https://sheets.google.com e crie uma nova planilha.
2. Copie a estrutura acima (3 colunas: Artista, Musica, (opcional) Tag/Genero).
3. Após preencher suas músicas, clique em:
   - Arquivo → Compartilhar → Publicar na Web
   - Escolha o tipo “Planilha inteira” e o formato “Valores separados por vírgulas (.csv)”.
4. Após publicar, copie o link gerado.
   Ele terá formato parecido com este:

   https://docs.google.com/spreadsheets/d/1ABCdEfGhIJKlmnopQRstuVWxyz/export?format=csv

5. Substitua a URL no seu main.py nesta linha:

   GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/1ABCdEfGhIJKlmnopQRstuVWxyz/export?format=csv"

--------------------------------------------------
💻 Instalação e uso
--------------------------------------------------

🔧 Requisitos:
- Python 3.8 ou superior
- FFmpeg instalado (necessário para extrair áudio)

📦 Instalar dependências

Windows:
1. Abra o Prompt de Comando na pasta do projeto.
2. Execute:
   pip install -r requirements.txt

Linux/macOS:
   sudo apt install ffmpeg -y
   pip install -r requirements.txt

--------------------------------------------------
▶️ Executando o script
--------------------------------------------------

Windows:
   python main.py

Linux/macOS:
   python3 main.py

Durante a execução, o script irá:
1. Baixar os dados da planilha pública.
2. Criar uma pasta "output/" (com subpastas por gênero).
3. Baixar as músicas, renomeando com BPM quando possível.
4. Registrar os nomes baixados no "historico.txt" (para evitar duplicatas futuras).

--------------------------------------------------
📁 Estrutura gerada
--------------------------------------------------
```
musica_downloader/
│
├── main.py
├── requirements.txt
├── historico.txt
├── baixados.txt
├── output/
│   ├── House/
│   │   └── Adam Port - Afro House (122 BPM).mp3
│   ├── Tech House/
│   │   └── Vintage Culture - It Is What It Is (124 BPM).mp3
│   └── Sem_Genero/
│       └── Artista - Musica.mp3
```
--------------------------------------------------
💡 Dica
--------------------------------------------------

Você pode deixar o script rodando de hora em hora (por exemplo, para baixar automaticamente novas faixas adicionadas na planilha).

Linux/macOS: use o crontab
Windows: use o Agendador de Tarefas

Exemplo no macOS/Linux:
   crontab -e

E adicione:
   0 * * * * /usr/bin/python3 /caminho/para/main.py

Isso fará o script rodar automaticamente a cada 1 hora. ⏱️

--------------------------------------------------
🧠 Créditos
--------------------------------------------------

Desenvolvido com ❤️ para DJs, produtores e colecionadores que querem uma forma prática de gerenciar downloads musicais pela nuvem.
A inteligência do script garante que você nunca baixe duas vezes a mesma faixa — e que tudo fique organizado por gênero e BPM.
