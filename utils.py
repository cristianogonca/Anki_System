import os
import pandas as pd
from gtts import gTTS
import genanki
from pathlib import Path
import sqlite3
import zipfile
import tempfile
import shutil


def criar_audios(df, audio_folder_name, speed=1.0):
    """
    Cria arquivos de áudio MP3 para Word e Context do DataFrame usando gTTS (Google Text-to-Speech).
    
    Args:
        df: DataFrame com colunas 'Word', 'Phonetic' (opcional), 'Context'
        audio_folder_name: Nome da pasta onde os áudios serão salvos
        speed: Velocidade da fala (0.5 = lento, 1.0 = normal, 2.0 = rápido)
    
    Returns:
        Caminho da pasta onde os áudios foram salvos
    """
    # Criar diretório de áudios usando tempfile para compatibilidade com Streamlit Cloud
    audio_dir = os.path.join(tempfile.gettempdir(), audio_folder_name)
    os.makedirs(audio_dir, exist_ok=True)
    
    # Verificar se existe coluna Word
    if 'Word' not in df.columns:
        raise ValueError("DataFrame deve ter coluna 'Word'")
    
    # Verificar se existe coluna Context
    if 'Context' not in df.columns:
        raise ValueError("DataFrame deve ter coluna 'Context'")
    
    # Gerar áudios para Word
    palavras = df['Word'].tolist()
    for i, palavra in enumerate(palavras):
        if pd.notna(palavra):
            try:
                filename = os.path.join(audio_dir, f"word_{i+1}.mp3")
                tts = gTTS(text=str(palavra), lang='en', slow=(speed < 0.8))
                tts.save(filename)
            except Exception as e:
                print(f"Erro ao criar áudio Word {i+1}: {str(e)}")
                continue
    
    # Gerar áudios para Context
    contextos = df['Context'].tolist()
    for i, contexto in enumerate(contextos):
        if pd.notna(contexto):
            try:
                filename = os.path.join(audio_dir, f"context_{i+1}.mp3")
                tts = gTTS(text=str(contexto), lang='en', slow=(speed < 0.8))
                tts.save(filename)
            except Exception as e:
                print(f"Erro ao criar áudio Context {i+1}: {str(e)}")
                continue
    
    return audio_dir


def gerar_links_audios(df, audio_dir, excel_path, deck_name=None):
    """
    Adiciona colunas 'Audio_Word' e 'Audio_Context' ao DataFrame.
    
    Args:
        df: DataFrame com as palavras e contextos
        audio_dir: Diretório onde estão os arquivos de áudio
        excel_path: Caminho do arquivo Excel original para atualizar
        deck_name: Nome do baralho (usado para criar arquivo atualizado)
    
    Returns:
        DataFrame com colunas de áudio adicionadas
    """
    import os
    
    print(f"🔍 Debug - Audio dir: {audio_dir}")
    print(f"🔍 Debug - Número de linhas: {len(df)}")
    
    # Criar listas de nomes de arquivos
    audio_word = []
    audio_context = []
    word_encontrados = 0
    context_encontrados = 0
    
    for i in range(len(df)):
        # Áudio Word
        audio_file_word = f"word_{i+1}.mp3"
        audio_path_word = os.path.join(audio_dir, audio_file_word)
        if os.path.exists(audio_path_word):
            audio_word.append(audio_file_word)
            word_encontrados += 1
        else:
            audio_word.append("")
            print(f"⚠️ Áudio Word não encontrado: {audio_path_word}")
        
        # Áudio Context
        audio_file_ctx = f"context_{i+1}.mp3"
        audio_path_ctx = os.path.join(audio_dir, audio_file_ctx)
        if os.path.exists(audio_path_ctx):
            audio_context.append(audio_file_ctx)
            context_encontrados += 1
        else:
            audio_context.append("")
            print(f"⚠️ Áudio Context não encontrado: {audio_path_ctx}")
    
    print(f"✅ Áudios Word encontrados: {word_encontrados}/{len(df)}")
    print(f"✅ Áudios Context encontrados: {context_encontrados}/{len(df)}")
    
    # Adicionar colunas ao DataFrame
    df_copy = df.copy()
    df_copy['Audio_Word'] = audio_word
    df_copy['Audio_Context'] = audio_context
    
    print(f"✅ DataFrame com {len(df_copy)} linhas e colunas: {df_copy.columns.tolist()}")
    
    return df_copy


def criar_baralho_anki(df, audio_dir, deck_name, deck_id, model_id):
    """
    Cria um baralho Anki (.apkg) com as cartas e áudios.
    Se o baralho já existir, adiciona as novas cartas ao baralho existente.
    
    Args:
        df: DataFrame com colunas 'Word', 'Translation' (opcional), 'Phonetic' (opcional), 'Context', 'Audio_Word', 'Audio_Context'
        audio_dir: Diretório onde estão os arquivos de áudio
        deck_name: Nome do baralho
        deck_id: ID único do baralho
        model_id: ID único do modelo
    
    Returns:
        Tuple (caminho do arquivo .apkg criado, número de cartas adicionadas, total de cartas)
    """
    output_filename = f"{deck_name}.apkg"
    output_path = os.path.join(os.getcwd(), output_filename)
    
    # Verificar se o baralho já existe
    cartas_existentes = []
    if os.path.exists(output_path):
        print(f"📦 Baralho existente encontrado: {output_filename}")
        print("🔄 Carregando cartas existentes...")
        cartas_existentes = extrair_cartas_existentes(output_path)
        print(f"✅ {len(cartas_existentes)} cartas já existem no baralho")
    
    # Criar modelo do cartão
    my_model = genanki.Model(
        model_id,
        'Anki Model with Translation and Phonetic',
        fields=[
            {'name': 'Word'},
            {'name': 'Translation'},
            {'name': 'Phonetic'},
            {'name': 'Context'},
            {'name': 'Audio_Word'},
            {'name': 'Audio_Context'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
                    <div style="font-size: 28px; font-weight: bold; text-align: center; margin: 20px;">
                        {{Word}}
                    </div>
                    {{#Phonetic}}
                    <div style="font-size: 18px; color: #666; text-align: center; margin: 10px; font-style: italic;">
                        [{{Phonetic}}]
                    </div>
                    {{/Phonetic}}
                    <div style="text-align: center; margin-top: 15px;">
                        {{Audio_Word}}
                    </div>
                ''',
                'afmt': '''
                    {{FrontSide}}
                    <hr id="answer">
                    {{#Translation}}
                    <div style="font-size: 22px; color: #4CAF50; font-weight: bold; text-align: center; margin: 15px;">
                        {{Translation}}
                    </div>
                    {{/Translation}}
                    <div style="font-size: 20px; text-align: center; color: #2196F3; margin: 20px;">
                        {{Context}}
                    </div>
                    <div style="text-align: center; margin-top: 10px;">
                        {{Audio_Context}}
                    </div>
                ''',
            },
        ],
        css='''
            .card {
                font-family: arial;
                font-size: 20px;
                text-align: center;
                color: black;
                background-color: white;
            }
        '''
    )
    
    # Criar baralho
    my_deck = genanki.Deck(deck_id, deck_name)
    
    # Lista para arquivos de mídia
    audio_files = []
    cartas_novas = 0
    cartas_duplicadas = 0
    
    # Adicionar cartas ao baralho
    for index, row in df.iterrows():
        word = str(row['Word']) if pd.notna(row['Word']) else ""
        translation = str(row['Translation']) if 'Translation' in row and pd.notna(row['Translation']) else ""
        phonetic = str(row['Phonetic']) if 'Phonetic' in row and pd.notna(row['Phonetic']) else ""
        context = str(row['Context']) if pd.notna(row['Context']) else ""
        
        # Verificar se a carta já existe (comparar Word + Context)
        carta_key = f"{word.strip().lower()}|{context.strip().lower()}"
        if carta_key in cartas_existentes:
            cartas_duplicadas += 1
            print(f"⏭️  Carta duplicada ignorada: {word}")
            continue
        
        audio_word_file = str(row['Audio_Word']) if pd.notna(row['Audio_Word']) else ""
        audio_context_file = str(row['Audio_Context']) if pd.notna(row['Audio_Context']) else ""
        
        # Processar áudio Word
        if audio_word_file:
            audio_path = os.path.join(audio_dir, audio_word_file)
            if os.path.exists(audio_path):
                audio_files.append(audio_path)
                audio_word_tag = f'[sound:{audio_word_file}]'
            else:
                audio_word_tag = ""
        else:
            audio_word_tag = ""
        
        # Processar áudio Context
        if audio_context_file:
            audio_path = os.path.join(audio_dir, audio_context_file)
            if os.path.exists(audio_path):
                audio_files.append(audio_path)
                audio_context_tag = f'[sound:{audio_context_file}]'
            else:
                audio_context_tag = ""
        else:
            audio_context_tag = ""
        
        # Criar nota
        my_note = genanki.Note(
            model=my_model,
            fields=[word, translation, phonetic, context, audio_word_tag, audio_context_tag]
        )
        
        # Adicionar nota ao baralho
        my_deck.add_note(my_note)
        cartas_novas += 1
    
    # Se o baralho já existia, fazer merge dos arquivos de áudio antigos
    if os.path.exists(output_path) and cartas_novas > 0:
        print(f"🔗 Mesclando com baralho existente...")
        audio_files_antigos = extrair_audios_existentes(output_path)
        audio_files.extend(audio_files_antigos)
    
    # Criar pacote com arquivos de mídia
    my_package = genanki.Package(my_deck)
    my_package.media_files = audio_files
    
    # Salvar arquivo .apkg
    my_package.write_to_file(output_path)
    
    total_cartas = len(cartas_existentes) + cartas_novas
    
    print(f"\n📊 Resumo:")
    print(f"  ✅ Cartas novas adicionadas: {cartas_novas}")
    print(f"  ⏭️  Cartas duplicadas ignoradas: {cartas_duplicadas}")
    print(f"  📦 Total de cartas no baralho: {total_cartas}")
    
    return output_path, cartas_novas, total_cartas


def extrair_cartas_existentes(apkg_path):
    """
    Extrai as cartas existentes de um arquivo .apkg para verificar duplicatas.
    
    Args:
        apkg_path: Caminho do arquivo .apkg
    
    Returns:
        Set com chaves das cartas (word|context em lowercase)
    """
    cartas = set()
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Extrair o .apkg (é um arquivo ZIP)
        with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Ler o banco de dados SQLite
        db_path = os.path.join(temp_dir, 'collection.anki2')
        if not os.path.exists(db_path):
            db_path = os.path.join(temp_dir, 'collection.anki21')
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Buscar todas as notas (campo 'flds' contém os campos separados por \x1f)
            cursor.execute("SELECT flds FROM notes")
            rows = cursor.fetchall()
            
            for row in rows:
                fields = row[0].split('\x1f')
                if len(fields) >= 4:
                    word = fields[0].strip().lower()
                    # translation em fields[1], phonetic em fields[2] (não usados na chave)
                    context = fields[3].strip().lower()
                    carta_key = f"{word}|{context}"
                    cartas.add(carta_key)
                elif len(fields) >= 3:
                    word = fields[0].strip().lower()
                    # phonetic em fields[1] (não usado na chave)
                    context = fields[2].strip().lower()
                    carta_key = f"{word}|{context}"
                    cartas.add(carta_key)
                elif len(fields) >= 2:  # Compatibilidade com baralhos antigos
                    word = fields[0].strip().lower()
                    context = fields[1].strip().lower()
                    carta_key = f"{word}|{context}"
                    cartas.add(carta_key)
            
            conn.close()
    
    except Exception as e:
        print(f"⚠️ Erro ao ler baralho existente: {str(e)}")
    
    finally:
        # Limpar diretório temporário
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    return cartas


def extrair_audios_existentes(apkg_path):
    """
    Extrai os arquivos de áudio de um .apkg existente para preservá-los no merge.
    
    Args:
        apkg_path: Caminho do arquivo .apkg
    
    Returns:
        Lista com caminhos dos arquivos de áudio extraídos
    """
    audio_files = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Extrair o .apkg
        with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Copiar arquivos de áudio (.mp3)
        for file in os.listdir(temp_dir):
            if file.endswith('.mp3'):
                source = os.path.join(temp_dir, file)
                # Copiar para diretório temporário permanente
                dest = os.path.join(os.getcwd(), 'temp_audio_merge', file)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(source, dest)
                audio_files.append(dest)
    
    except Exception as e:
        print(f"⚠️ Erro ao extrair áudios: {str(e)}")
    
    finally:
        # Limpar diretório temporário de extração
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    return audio_files


def validar_excel(file_path):
    """
    Valida se o arquivo Excel tem o formato correto.
    
    Args:
        file_path: Caminho do arquivo Excel
    
    Returns:
        Tuple (bool, mensagem): True se válido, False caso contrário
    """
    try:
        df = pd.read_excel(file_path)
        
        if len(df.columns) < 2:
            return False, "O arquivo deve ter pelo menos 2 colunas"
        
        if len(df) == 0:
            return False, "O arquivo está vazio"
        
        return True, "Arquivo válido"
        
    except Exception as e:
        return False, f"Erro ao ler arquivo: {str(e)}"


def limpar_arquivos_temporarios():
    """
    Remove arquivos temporários criados durante o processo.
    """
    temp_files = ['temp_excel.xlsx', 'excel_com_audios.xlsx']
    temp_dirs = ['temp_audio_merge']
    
    for temp_file in temp_files:
        temp_path = os.path.join(os.getcwd(), temp_file)
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
    
    for temp_dir in temp_dirs:
        temp_path = os.path.join(os.getcwd(), temp_dir)
        if os.path.exists(temp_path):
            try:
                shutil.rmtree(temp_path, ignore_errors=True)
            except:
                pass
