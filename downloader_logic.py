"""Regras de download e listagem de formatos."""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import yt_dlp
import subprocess
import os
from pathlib import Path


class DownloaderLogic:
    """Controla download, formatos e status da interface."""
    
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
            self.log("Nisu, FFmpeg detectado! Qualidade Top disponível")
        except:
            self.log("Yerro! FFmpeg não encontrado - Qualidade pode ser limitada")
    
    def log(self, message):
        """Registra mensagem no log"""
        self.gui.ui.widgets['log_text'].insert(tk.END, message + "\n")
        self.gui.ui.widgets['log_text'].see(tk.END)
        self.gui.root.update()
    
    def escolher_pasta(self):
        """Abre diálogo para escolher pasta de destino"""
        pasta = filedialog.askdirectory()
        if pasta:
            self.gui.pasta_var.set(pasta)
    
    def download_inteligente(self):
        """Download automático na melhor qualidade poss­vel"""
        url = self.gui.url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL")
            return
        
        if self.downloading:
            return
        
        self.downloading = True
        self.gui.ui.widgets['smart_btn'].config(
            state=tk.DISABLED,
            text="â³ BAIXANDO..."
        )
        self.gui.ui.widgets['download_btn'].config(state=tk.DISABLED)
        self.gui.ui.widgets['progress'].start(10)
        
        threading.Thread(
            target=self.executar_download_inteligente,
            daemon=True
        ).start()
    
    def executar_download_inteligente(self):
        """Executa o download inteligente em thread"""
        url = self.gui.url_var.get().strip()
        pasta = self.gui.pasta_var.get()
        
        Path(pasta).mkdir(parents=True, exist_ok=True)
        
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
            self.log("Download Inteligente: Buscando melhor qualidade...")
            self.gui.ui.widgets['status_label'].config(
                text="Baixando na melhor qualidade disponÃ­vel..."
            )
            
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'video')
                altura = info.get('height', '?')
            
            self.log("Download concluído!")
            self.log(f"“¹ resolução: {altura}p")
            self.log(f"ðŸ“ Salvo em: {os.path.abspath(pasta)}")
            self.gui.ui.widgets['status_label'].config(
                text="Download concluído!"
            )
            
            messagebox.showinfo(
                "Sucesso",
                f"Vídeo baixado!\n\n{titulo}.mp4\nResolução: {altura}p"
            )
            
        except Exception as e:
            self.log(f"âŒ Erro: {str(e)}")
            self.gui.ui.widgets['status_label'].config(
                text="Erro no download"
            )
            messagebox.showerror(
                "Erro",
                f"Erro ao baixar vÃ­deo:\n{str(e)}"
            )
        
        finally:
            self.downloading = False
            self.gui.ui.widgets['smart_btn'].config(
                state=tk.NORMAL,
                text="âš¡ DOWNLOAD INTELIGENTE (Melhor Qualidade)"
            )
            self.gui.ui.widgets['download_btn'].config(
                state=tk.NORMAL if self.formatos_disponiveis else tk.DISABLED
            )
            self.gui.ui.widgets['progress'].stop()
    
    def listar_qualidades(self):
        """Lista as qualidades disponiveis de um vÃ­deo"""
        url = self.gui.url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL")
            return
        
        self.log("ðŸ” Analisando formatos disponiveis...")
        self.gui.ui.widgets['status_label'].config(
            text="Obtendo qualidades disponiveis..."
        )
        self.gui.ui.widgets['quality_listbox'].delete(0, tk.END)
        
        threading.Thread(
            target=self._fetch_formats,
            args=(url,),
            daemon=True
        ).start()
    
    def _fetch_formats(self, url):
        """Busca os formatos disponiveis em thread"""
        try:
            opcoes = {
                'quiet': True,
                'no_warnings': True,
                'listformats': True,
            }
            
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=False)
                
                self.video_info = info
                titulo = info.get('title', 'Desconhecido')
                duracao = info.get('duration', 0)
                
                msg = f"ðŸ“¹ {titulo}\nâ±ï¸ {duracao//60}:{duracao%60:02d}"
                self.gui.ui.widgets['info_frame'].pack(
                    padx=20,
                    pady=(0, 15),
                    fill=tk.X
                )
                self.gui.ui.widgets['info_label'].config(text=msg)
                
                self._process_formats(info.get('formats', []))
                
        except Exception as e:
            self.log(f"âŒ Erro: {str(e)}")
            self.gui.ui.widgets['status_label'].config(
                text="Erro ao obter qualidades"
            )
    
    def _process_formats(self, formatos):
        """Processa e filtra os formatos disponiveis"""
        self.formatos_disponiveis = []
        formatos_video = []
        formatos_unicos = {}
        
        for f in formatos:
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')
            
            if vcodec and vcodec != 'none':
                height = f.get('height', 0)
                
                if height and height > 0:
                    fps = f.get('fps', 30)
                    ext = f.get('ext', 'mp4')
                    filesize = f.get('filesize', 0) or f.get('filesize_approx', 0)
                    format_id = f.get('format_id', '')
                    tbr = f.get('tbr', 0)
                    
                    codec_display = self._get_codec_name(vcodec)
                    size_mb = filesize / (1024*1024) if filesize else 0
                    tem_audio = "ðŸ”Š" if acodec != 'none' else "ðŸ”‡"
                    
                    chave = f"{height}_{fps}_{codec_display}_{tem_audio}"
                    
                    if chave not in formatos_unicos or tbr > formatos_unicos.get(chave, {}).get('tbr', 0):
                        formato_info = {
                            'id': format_id,
                            'height': height,
                            'fps': fps,
                            'ext': ext,
                            'size': size_mb,
                            'audio': tem_audio,
                            'codec': codec_display,
                            'tbr': tbr,
                            'display': f"{height}p @ {fps}fps {tem_audio} [{codec_display}] ({ext})" + 
                                      (f" - {size_mb:.1f}MB" if size_mb > 0 else "")
                        }
                        formatos_unicos[chave] = formato_info
        
        formatos_video = list(formatos_unicos.values())
        formatos_video.sort(
            key=lambda x: (x['height'], x['fps'], x['tbr']),
            reverse=True
        )
        
        self.formatos_disponiveis = formatos_video
        
        if formatos_video:
            for idx, fmt in enumerate(formatos_video):
                self.gui.ui.widgets['quality_listbox'].insert(
                    tk.END,
                    f"{idx+1}. {fmt['display']}"
                )
            
            self.gui.ui.widgets['quality_listbox'].select_set(0)
            self.gui.ui.widgets['download_btn'].config(state=tk.NORMAL)
            self.log(f"âœ… {len(formatos_video)} qualidades encontradas!")
            self.gui.ui.widgets['status_label'].config(
                text=f"âœ… {len(formatos_video)} qualidades - Selecione e clique em Baixar"
            )
        else:
            self.gui.ui.widgets['quality_listbox'].insert(
                tk.END,
                "Nenhum formato encontrado"
            )
            self.log("âš ï¸  Nenhum formato de vídeo encontrado")
            self.gui.ui.widgets['status_label'].config(
                text="Nenhum formato disponÃ­vel"
            )
    
    @staticmethod
    def _get_codec_name(vcodec):
        """Retorna o nome do codec de forma legível"""
        if 'avc' in vcodec:
            return 'h264'
        elif 'vp9' in vcodec:
            return 'vp9'
        elif 'av01' in vcodec:
            return 'av1'
        else:
            return vcodec[:6]
    
    def start_download(self):
        """Inicia o download da qualidade selecionada"""
        if self.downloading:
            return
        
        selection = self.gui.ui.widgets['quality_listbox'].curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione uma qualidade")
            return
        
        self.downloading = True
        self.gui.ui.widgets['download_btn'].config(
            state=tk.DISABLED,
            text="â³ BAIXANDO..."
        )
        self.gui.ui.widgets['smart_btn'].config(state=tk.DISABLED)
        self.gui.ui.widgets['progress'].start(10)
        
        threading.Thread(
            target=self.download_video,
            args=(selection[0],),
            daemon=True
        ).start()
    
    def download_video(self, format_index):
        """Executa o download de um vÃ­deo em thread"""
        url = self.gui.url_var.get().strip()
        pasta = self.gui.pasta_var.get()
        
        Path(pasta).mkdir(parents=True, exist_ok=True)
        
        formato_escolhido = self.formatos_disponiveis[format_index]
        format_id = formato_escolhido['id']
        tem_audio = formato_escolhido['audio'] == "ðŸ”Š"
        
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
            self.log(f"â¬‡ï¸  Baixando em {formato_escolhido['height']}p...")
            self.gui.ui.widgets['status_label'].config(
                text=f"Baixando {formato_escolhido['height']}p..."
            )
            
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'video')
            
            self.log("âœ… Download concluÃ­do!")
            self.log(
                f"ðŸ“¹ ResoluÃ§Ã£o: {formato_escolhido['height']}p [{formato_escolhido['codec']}]"
            )
            self.log(f"ðŸ“ Salvo em: {os.path.abspath(pasta)}")
            self.gui.ui.widgets['status_label'].config(
                text="Download concluÃ­do!"
            )
            
            messagebox.showinfo(
                "Sucesso",
                f"VÃ­deo baixado!\n\n{titulo}.mp4\nResoluÃ§Ã£o: {formato_escolhido['height']}p"
            )
            
        except Exception as e:
            self.log(f"âŒ Erro: {str(e)}")
            self.gui.ui.widgets['status_label'].config(
                text="Erro - Tente Download Inteligente"
            )
            messagebox.showerror(
                "Erro",
                f"NÃ£o foi possÃ­vel baixar neste formato.\n\nTente usar o DOWNLOAD INTELIGENTE "
                f"ou selecione outra qualidade.\n\nErro: {str(e)[:150]}"
            )
        
        finally:
            self.downloading = False
            self.gui.ui.widgets['download_btn'].config(
                state=tk.NORMAL,
                text="â¬‡ï¸  BAIXAR QUALIDADE SELECIONADA"
            )
            self.gui.ui.widgets['smart_btn'].config(state=tk.NORMAL)
            self.gui.ui.widgets['progress'].stop()



