"""
Lógica principal da aplicação
Responsável por toda a funcionalidade de download
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import yt_dlp
import subprocess
import os
from pathlib import Path


class DownloaderLogic:
    """Classe responsável pela lógica de download e processamento de vídeos"""
    
    def __init__(self, gui):
        self.gui = gui
        self.downloading = False
        self.formatos_disponiveis = []
        self.video_info = None
        
    def check_ffmpeg(self):
        """Verifica se FFmpeg está instalado"""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True,
                timeout=5
            )
            self.log("✅ FFmpeg detectado! Qualidade máxima disponível")
        except:
            self.log("⚠️  FFmpeg não encontrado - Qualidade pode ser limitada")
    
    def log(self, message):
        """Registra mensagem no log"""
        self.gui.log_message(message)
    
    def escolher_pasta(self):
        """Abre diálogo para escolher pasta de destino"""
        pasta = filedialog.askdirectory()
        if pasta:
            self.gui.pasta_var.set(pasta)
    
    def download_inteligente(self):
        """Download automático na melhor qualidade possível"""
        url = self.gui.url_var.get().strip()
        if not url:
            messagebox.showwarning("Coloca uma URL ai pra nois baixar")
            return
        
        if self.downloading:
            return
        
        self.downloading = True
        self.gui.ui.widgets['smart_btn'].configure(
            state="disabled",
            text="⏳ BAIXANDO..."
        )
        self.gui.ui.widgets['download_btn'].configure(state="disabled")
        
        threading.Thread(
            target=self.executar_download_inteligente,
            daemon=True
        ).start()
    
    def executar_download_inteligente(self):
        """Executa o download inteligente em thread"""
        url = self.gui.url_var.get().strip()
        pasta = self.gui.pasta_var.get()
        
        Path(pasta).mkdir(parents=True, exist_ok=True)
        
        # Formato que SEMPRE funciona - tenta da melhor para pior qualidade
        formato_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'
        
        opcoes = {
            'format': formato_string,
            'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'no_warnings': True,
            'quiet': False,
            'noplaylist': True,
            'concurrent_fragment_downloads': 16,
            'http_chunk_size': 10485760,
        }
        
        try:
            self.log("⚡ Download Inteligente: Buscando melhor qualidade...")
            self.gui.update_status("Baixando na melhor qualidade disponível...")
            
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'video')
                altura = info.get('height', '?')
                
            self.log(f"✅ Download concluído: {titulo}")
            self.log(f"📹 Resolução: {altura}p")
            self.gui.update_status("Download concluído com sucesso!")
            messagebox.showinfo("Sucesso", f"Vídeo baixado: {titulo}\nResolução: {altura}p")
            
        except Exception as e:
            self.log(f"❌ Erro no download: {str(e)}")
            self.gui.update_status("Erro no download - veja o log")
            messagebox.showerror("Erro", f"Erro ao baixar vídeo:\n{str(e)}")
        
        finally:
            self.downloading = False
            self.gui.ui.widgets['smart_btn'].configure(
                state="normal",
                text="⚡ DOWNLOAD INTELIGENTE (Melhor Qualidade)"
            )
            self.gui.ui.widgets['download_btn'].configure(state="normal")
            self.gui.update_progress(0)
    
    def listar_qualidades(self):
        """Lista as qualidades disponíveis do vídeo"""
        url = self.gui.url_var.get().strip()
        if not url:
            messagebox.showwarning("Coloca uma URL ai pra nois baixar")
            return
        
        self.gui.ui.widgets['info_btn'].configure(state="disabled")
        threading.Thread(
            target=self.executar_listar_qualidades,
            args=(url,),
            daemon=True
        ).start()
    
    def executar_listar_qualidades(self, url):
        """Executa a listagem de qualidades em thread"""
        try:
            self.log("🔍 Buscando qualidades disponíveis...")
            self.gui.update_status("Analisando vídeo...")
            
            opcoes = {
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=False)
                self.video_info = info
                
                # Processar formatos
                formatos = self._process_formats(info.get('formats', []))
                
                if formatos:
                    self.formatos_disponiveis = formatos
                    self.gui.update_quality_list(formatos)
                    self.log(f"✅ {len(formatos)} qualidades encontradas")
                    self.gui.enable_download_button(True)
                else:
                    self.log("⚠️  Nenhuma qualidade específica encontrada")
                    self.gui.update_quality_list(["Qualidade padrão disponível"])
            
            self.gui.update_status("Qualidades carregadas!")
            
        except Exception as e:
            self.log(f"❌ Erro ao buscar qualidades: {str(e)}")
            self.gui.update_status("Erro ao buscar qualidades")
            messagebox.showerror("Erro", f"Erro ao buscar qualidades:\n{str(e)}")
        
        finally:
            self.gui.ui.widgets['info_btn'].configure(state="normal")
    
    def _process_formats(self, formats):
        """Processa e filtra formatos disponíveis"""
        qualidades = []
        formatos_dict = {}
        
        for fmt in formats:
            vcodec = fmt.get('vcodec', 'none')
            acodec = fmt.get('acodec', 'none')
            
            # Aceitar qualquer formato com vídeo (com ou sem áudio)
            if vcodec and vcodec != 'none':
                height = fmt.get('height')
                fps = fmt.get('fps', 30)
                ext = fmt.get('ext', 'mp4')
                format_id = fmt.get('format_id', '')
                tbr = fmt.get('tbr', 0)
                filesize = fmt.get('filesize', 0) or fmt.get('filesize_approx', 0)
                
                if height and height > 0:
                    # Identificar se tem áudio
                    tem_audio = "🔊" if acodec != 'none' else "🔇"
                    
                    # Codec
                    codec = 'h264' if 'avc' in vcodec else ('vp9' if 'vp9' in vcodec else 'av1' if 'av01' in vcodec else vcodec[:6])
                    
                    # Tamanho
                    size_mb = filesize / (1024*1024) if filesize else 0
                    size_str = f" - {size_mb:.1f}MB" if size_mb > 0 else ""
                    
                    # Chave única
                    chave = f"{height}_{fps}_{codec}_{tem_audio}"
                    
                    # Guardar melhor bitrate
                    if chave not in formatos_dict or tbr > formatos_dict[chave]['tbr']:
                        qualidade_str = f"{height}p @ {fps}fps {tem_audio} [{codec}] ({ext}){size_str}"
                        
                        formatos_dict[chave] = {
                            'qualidade': qualidade_str,
                            'format_id': format_id,
                            'height': height,
                            'fps': fps,
                            'tbr': tbr,
                            'tem_audio': tem_audio == "🔊",
                            'codec': codec
                        }
        
        # Converter para lista e ordenar
        qualidades = list(formatos_dict.values())
        qualidades.sort(key=lambda x: (x['height'], x['fps'], x['tbr']), reverse=True)
        
        # Guardar referência dos formatos para download
        self.formatos_disponiveis_detalhes = qualidades
        
        return [f"{q['qualidade']}" for q in qualidades[:20]]
    
    def start_download(self):
        """Inicia download da qualidade selecionada"""
        if not self.formatos_disponiveis:
            messagebox.showwarning("Meu fi, tem que selecionar a qualidade primeiro...")
            return
        
        url = self.gui.url_var.get().strip()
        if not url:
            messagebox.showwarning("Coloca uma URL ai pra nois baixar")
            return
        
        if self.downloading:
            return
        
        # Pegar índice selecionado do ComboBox
        selected = self.gui.ui.widgets['quality_listbox'].get()
        
        # Encontrar o formato correspondente
        format_index = None
        for idx, fmt in enumerate(self.formatos_disponiveis):
            if fmt == selected:
                format_index = idx
                break
        
        if format_index is None:
            messagebox.showwarning("Seleciona uma opção válida uai...")
            return
        
        self.downloading = True
        self.gui.ui.widgets['smart_btn'].configure(state="disabled")
        self.gui.ui.widgets['download_btn'].configure(
            state="disabled",
            text="⏳ BAIXANDO..."
        )
        
        threading.Thread(
            target=self.executar_download,
            args=(url, format_index),
            daemon=True
        ).start()
    
    def executar_download(self, url, format_index):
        """Executa o download da qualidade específica"""
        pasta = self.gui.pasta_var.get()
        
        Path(pasta).mkdir(parents=True, exist_ok=True)
        
        # Pegar detalhes do formato
        formato = self.formatos_disponiveis_detalhes[format_index]
        format_id = formato['format_id']
        tem_audio = formato['tem_audio']
        
        # Criar string de formato com fallbacks
        if not tem_audio:
            format_string = f"{format_id}+bestaudio[ext=m4a]/{format_id}+bestaudio/{format_id}"
        else:
            format_string = format_id
        
        opcoes = {
            'format': format_string,
            'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'no_warnings': True,
            'quiet': False,
            'noplaylist': True,
            'concurrent_fragment_downloads': 16,
            'http_chunk_size': 10485760,
        }
        
        try:
            self.log(f"⬇️  Baixando em {formato['height']}p...")
            self.gui.update_status(f"Baixando {formato['height']}p...")
            
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'video')
            
            self.log(f"✅ PURURIN! Download concluído: {titulo}")
            self.log(f"📹 Resolução: {formato['height']}p [{formato['codec']}]")
            self.gui.update_status("Download concluído com sucesso!")
            messagebox.showinfo("Pururin!", f"Vídeo baixado: {titulo}\nResolução: {formato['height']}p")
            
        except Exception as e:
            self.log(f"❌ Deu ruim: {str(e)}")
            self.gui.update_status("Deu ruim - veja o log")
            messagebox.showerror("Vish...", f" n deu pra baixar vídeo:\n{str(e)[:200]}")
        
        finally:
            self.downloading = False
            self.gui.ui.widgets['smart_btn'].configure(state="normal")
            self.gui.ui.widgets['download_btn'].configure(
                state="normal",
                text="⬇️  BAIXAR QUALIDADE SELECIONADA"
            )
            self.gui.update_progress(0)