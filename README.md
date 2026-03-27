# Video Downloader (VVD v1.2)

Aplicativo desktop em Python (Tkinter) para baixar videos com `yt-dlp`.

## Requisitos

- Python 3.10+
- `yt-dlp`
- `ffmpeg` (recomendado)

## Instalacao

```bash
pip install yt-dlp
```

## Como executar

```bash
cd VVD
python app.py
```

## Principais mudancas da v1.2 (comparada a v1.1)

- Adicionado sistema de temas (`light` e `dark`) com troca em tempo real.
- Adicionado botao de alternancia de tema na interface.
- Refatoracao de UI para manter mais widgets registrados e permitir atualizacao dinamica de cores.
- Ajustes visuais em secoes, labels e botoes da interface.
- Ajustes na logica de download/listagem com melhorias de mensagens e comentarios internos.
- Inclusao de `README.md` e `LICENSE` dentro da pasta `VVD`.

## Estrutura do projeto

- `app.py`: inicializacao e controle principal da aplicacao
- `ui_builder.py`: construcao da interface
- `downloader_logic.py`: logica de listagem e download
- `theme.py`: definicao de temas, cores e fontes

## Licenca

MIT. Consulte o arquivo `LICENSE`.
