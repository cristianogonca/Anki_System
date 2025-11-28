# 🎴 Anki Deck Generator with Audio

Professional web application to automate Anki flashcard deck creation with dual audio support (word + context).

## ✨ Features

- 📁 **Excel Upload**: Drag & drop Excel files with automatic column detection
- 🎵 **Dual Audio Generation**: Creates separate MP3 files for words and context using Windows voices
- 👀 **Live Preview**: View all data and audio samples before generating
- 🎴 **Smart Deck Creation**: Automatic merge with existing decks, duplicate detection
- 📊 **Professional UI**: Clean interface matching English Study Tracker design
- ⬇️ **Easy Download**: Get .apkg file and updated Excel with audio links

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd "Anki Python"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser** at `http://localhost:8501`

### Deploy to Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click "New app"
- Select your repository
- Main file: `app.py`
- Click "Deploy"

## 📖 How to Use

### 1. Prepare Your Excel File

Create an Excel file (.xlsx) with 2-4 columns:

**Minimum (2 columns):**
| Word | Context |
|------|---------|
| batter | I need to prepare the batter for pancakes |
| bake | She loves to bake cookies on weekends |

**Full format (4 columns):**
| Word | Translation | Phonetic | Context |
|------|-------------|----------|---------|
| batter | massa | /ˈbætər/ | I need to prepare the batter for pancakes |
| bake | assar | /beɪk/ | She loves to bake cookies on weekends |

### 2. Configure Settings

- **Deck Name**: Name for your Anki deck
- **Audio Speed**: Adjust speech rate (100-250)
- **Voice for Word**: Select voice for single words
- **Voice for Context**: Select voice for full sentences

### 3. Upload & Process

1. Upload your Excel file
2. Review the data preview
3. Click "Generate Audio & Process"
4. Preview audio samples
5. Click "Create .apkg Deck"
6. Download your deck!

## 🔧 Technical Details

### Audio Generation
- Uses `pyttsx3` with Windows SAPI voices
- Generates two files per card:
  - `word_X.mp3` - Single word pronunciation
  - `context_X.mp3` - Full sentence/context

### Deck Features
- **6-field card model**: Word, Translation, Phonetic, Context, Audio_Word, Audio_Context
- **Front template**: Shows Word, Phonetic, and Word audio
- **Back template**: Adds Translation, Context, and Context audio
- **Merge support**: Detects existing decks and adds only new cards
- **Duplicate prevention**: Uses word|context as unique key

### Output Files
- `{deck_name}.apkg` - Anki deck ready to import
- `{deck_name}.xlsx` - Updated Excel with audio link columns
- `Audios_{deck_name}/` - Folder with all MP3 files

## 📦 Dependencies

```txt
streamlit==1.31.0
pandas==2.2.0
openpyxl==3.1.2
pyttsx3==2.90
genanki==0.13.1
```

## 🎨 Design

Built with professional UI matching English Study Tracker:
- Purple gradient background (#667eea → #764ba2)
- Clean white card-based layout
- Responsive metric cards
- Smooth animations and transitions

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

MIT License - Feel free to use for personal or educational purposes.

---

Made with ❤️ for English learners | English Study Tracker
- Clique em "🎵 Gerar Áudios"
- Aguarde a criação dos arquivos MP3

#### 4. Adicionar Links
- Vá para a aba "3️⃣ Links dos Áudios"
- Clique em "📝 Gerar Links"
- Os links dos áudios serão adicionados automaticamente
- Faça download do Excel atualizado se desejar

#### 5. Gerar Baralho
- Vá para a aba "4️⃣ Gerar Baralho"
- Configure o nome do baralho na sidebar
- Clique em "🚀 Gerar Baralho .apkg"
- Faça download do arquivo .apkg

#### 6. Importar no Anki
1. Abra o Anki
2. Clique em "Arquivo" → "Importar"
3. Selecione o arquivo .apkg baixado
4. Pronto! Seu baralho está importado

## ⚙️ Configurações

Na sidebar, você pode configurar:
- **Nome do Baralho**: Nome que aparecerá no Anki
- **Idioma do Áudio**: Idioma para geração dos áudios (inglês, português, etc.)

## 📁 Estrutura de Arquivos

```
.
├── app.py              # Aplicação Streamlit principal
├── utils.py            # Funções auxiliares
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Interface web interativa
- **Pandas**: Manipulação de dados Excel
- **gTTS**: Geração de áudios (Google Text-to-Speech)
- **genanki**: Criação de baralhos Anki
- **openpyxl**: Leitura/escrita de arquivos Excel

## 📝 Formato das Cartas

Cada carta no Anki terá:
- **Frente**: Frase em inglês + Áudio reproduzível
- **Verso**: Tradução/contexto em português

## ⚠️ Observações

- Certifique-se de ter conexão com a internet para gerar os áudios
- Os áudios são gerados usando o Google Text-to-Speech
- Os IDs do baralho e modelo devem ser únicos para evitar conflitos no Anki
- Arquivos temporários são criados durante o processo e podem ser limpos após

## 🐛 Solução de Problemas

### Erro ao gerar áudios
- Verifique sua conexão com a internet
- Confirme que as frases em inglês estão preenchidas corretamente

### Erro ao importar no Anki
- Verifique se o Anki está atualizado
- Tente usar IDs diferentes para o baralho

### Excel não é reconhecido
- Certifique-se de que o arquivo é .xlsx
- Verifique se há pelo menos 2 colunas preenchidas

## 📧 Suporte

Para dúvidas ou problemas, verifique se todas as dependências foram instaladas corretamente.

---

Desenvolvido para facilitar a criação de baralhos Anki com áudio 🎴
