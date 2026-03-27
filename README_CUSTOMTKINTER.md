# Valentina's Video Downloader - v1.5

Versao com duas interfaces:

- `app.py`: interface Tkinter original
- `app_ctk.py`: interface CustomTkinter (moderna)

## Como executar

```bash
python app_ctk.py
```

Ou:

```bash
python app.py
```

## Dependencias

```bash
pip install customtkinter yt-dlp
```

## Principais mudancas da v1.5 (comparada a v1.4)

- Adicao da variante CustomTkinter (`app_ctk.py`, `ui_builder_ctk.py`, `downloader_logic_ctk.py`).
- Adicao de tela de splash (`splash.py`).
- Adicao de README especifico da variante CTk.
- Ajustes de tema (cores, tipografia, espacamento, dimensao da janela e tema padrao).
- Pequeno ajuste de mensagem na logica Tkinter.

## Requisitos

- Python 3.10+
- `yt-dlp`
- `customtkinter` (para versao moderna)
- `ffmpeg` (opcional, recomendado)
