# Video Downloader (SVD v1.1)

Aplicativo desktop em Python (Tkinter) para baixar vídeos com `yt-dlp`.

## Requisitos

- Python 3.10 ou superior
- `yt-dlp`
- `ffmpeg` (opcional, mas recomendado para melhor compatibilidade)

## Instalação

```bash
pip install yt-dlp
```

## Como executar

```bash
cd VVD
python app.py
```

## Funcionalidades

- Download inteligente na melhor qualidade disponível
- Listagem de qualidades antes de baixar
- Escolha de pasta de destino
- Exibição de status e log durante o processo

## Estrutura do projeto

- `VVD/app.py`: inicialização da aplicação
- `VVD/ui_builder.py`: construção da interface
- `VVD/downloader_logic.py`: lógica de listagem e download
- `VVD/theme.py`: cores e estilos da interface

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE`.
