from __future__ import annotations

import customtkinter as ctk

from models import FormatOption
from theme import FONTS


class MainView:
    def __init__(
        self,
        root: ctk.CTk,
        *,
        url_var: ctk.StringVar,
        output_var: ctk.StringVar,
        on_analyze,
        on_download_best,
        on_download_selected,
        on_browse_output,
        on_toggle_theme,
        on_open_repo,
    ) -> None:
        self.root = root
        self.url_var = url_var
        self.output_var = output_var
        self._on_analyze = on_analyze
        self._on_download_best = on_download_best
        self._on_download_selected = on_download_selected
        self._on_browse_output = on_browse_output
        self._on_toggle_theme = on_toggle_theme
        self._on_open_repo = on_open_repo
        self._format_options: list[FormatOption] = []
        self._build()

    def _build(self) -> None:
        self.root.geometry("860x760")
        self.root.minsize(760, 700)
        self.root.title("SimpleVideoDonwloader")

        self.topbar = ctk.CTkFrame(self.root, corner_radius=0, height=52)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.theme_btn = ctk.CTkButton(
            self.topbar,
            text="Tema: Escuro",
            width=140,
            font=FONTS["text_small"],
            command=self._on_toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=16, pady=10)

        self.header = ctk.CTkFrame(self.root, corner_radius=14)
        self.header.pack(fill="x", padx=18, pady=(14, 10))

        self.title_label = ctk.CTkLabel(
            self.header,
            text="SimpleVideoDonwloader",
            font=FONTS["title"],
            anchor="w",
        )
        self.title_label.pack(anchor="w", padx=18, pady=(14, 0))

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="YouTube, TikTok, Vimeo, Instagram e mais",
            font=FONTS["subtitle"],
            anchor="w",
        )
        self.subtitle_label.pack(anchor="w", padx=18, pady=(0, 14))

        self.content = ctk.CTkFrame(self.root, corner_radius=14)
        self.content.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        self._build_url_section()
        self._build_video_info_section()
        self._build_quality_section()
        self._build_output_section()
        self._build_actions_section()
        self._build_progress_section()
        self._build_log_section()
        self._build_footer()

    def _build_url_section(self) -> None:
        self.url_card = ctk.CTkFrame(self.content, corner_radius=12)
        self.url_card.pack(fill="x", padx=14, pady=(14, 10))

        self.url_label = ctk.CTkLabel(
            self.url_card,
            text="URL do video",
            font=FONTS["label"],
        )
        self.url_label.pack(anchor="w", padx=14, pady=(10, 4))

        row = ctk.CTkFrame(self.url_card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 12))

        self.url_entry = ctk.CTkEntry(
            row,
            textvariable=self.url_var,
            font=FONTS["text"],
            height=38,
            placeholder_text="Cole a URL aqui",
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.analyze_btn = ctk.CTkButton(
            row,
            text="Analisar",
            width=120,
            command=self._on_analyze,
            font=FONTS["button"],
        )
        self.analyze_btn.pack(side="right")

    def _build_video_info_section(self) -> None:
        self.info_card = ctk.CTkFrame(self.content, corner_radius=12)
        self.info_card.pack(fill="x", padx=14, pady=(0, 10))
        self.video_info_label = ctk.CTkLabel(
            self.info_card,
            text="Nenhum video analisado ainda.",
            font=FONTS["text_small"],
            justify="left",
            anchor="w",
        )
        self.video_info_label.pack(fill="x", padx=14, pady=10)

    def _build_quality_section(self) -> None:
        self.quality_card = ctk.CTkFrame(self.content, corner_radius=12)
        self.quality_card.pack(fill="x", padx=14, pady=(0, 10))

        self.quality_label = ctk.CTkLabel(
            self.quality_card,
            text="Qualidade",
            font=FONTS["label"],
        )
        self.quality_label.pack(anchor="w", padx=14, pady=(10, 4))

        self.quality_combo = ctk.CTkComboBox(
            self.quality_card,
            values=["Analise uma URL para listar os formatos"],
            state="readonly",
            font=FONTS["text"],
            height=38,
        )
        self.quality_combo.pack(fill="x", padx=14, pady=(0, 12))
        self.quality_combo.set("Analise uma URL para listar os formatos")

    def _build_output_section(self) -> None:
        self.output_card = ctk.CTkFrame(self.content, corner_radius=12)
        self.output_card.pack(fill="x", padx=14, pady=(0, 10))

        self.output_label = ctk.CTkLabel(
            self.output_card,
            text="Pasta de destino",
            font=FONTS["label"],
        )
        self.output_label.pack(anchor="w", padx=14, pady=(10, 4))

        row = ctk.CTkFrame(self.output_card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 12))

        self.output_entry = ctk.CTkEntry(
            row,
            textvariable=self.output_var,
            font=FONTS["text"],
            height=38,
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            row,
            text="Escolher",
            width=120,
            command=self._on_browse_output,
            font=FONTS["button"],
        )
        self.browse_btn.pack(side="right")

    def _build_actions_section(self) -> None:
        self.actions_card = ctk.CTkFrame(self.content, corner_radius=12)
        self.actions_card.pack(fill="x", padx=14, pady=(0, 10))

        self.smart_btn = ctk.CTkButton(
            self.actions_card,
            text="Download inteligente (melhor qualidade)",
            command=self._on_download_best,
            font=FONTS["button"],
            height=44,
        )
        self.smart_btn.pack(fill="x", padx=14, pady=(12, 8))

        self.selected_btn = ctk.CTkButton(
            self.actions_card,
            text="Baixar qualidade selecionada",
            command=self._on_download_selected,
            font=FONTS["button"],
            height=44,
        )
        self.selected_btn.pack(fill="x", padx=14, pady=(0, 12))

    def _build_progress_section(self) -> None:
        self.progress = ctk.CTkProgressBar(self.content, height=14)
        self.progress.pack(fill="x", padx=14, pady=(4, 6))
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self.content,
            text="Pronto.",
            font=FONTS["text_small"],
            anchor="w",
            justify="left",
        )
        self.status_label.pack(fill="x", padx=14, pady=(0, 10))

    def _build_log_section(self) -> None:
        self.log_card = ctk.CTkFrame(self.content, corner_radius=12)
        self.log_card.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        log_header = ctk.CTkFrame(self.log_card, fg_color="transparent")
        log_header.pack(fill="x", padx=14, pady=(10, 4))

        self.log_label = ctk.CTkLabel(log_header, text="Log de atividade", font=FONTS["label"])
        self.log_label.pack(side="left")

        self.clear_log_btn = ctk.CTkButton(
            log_header,
            text="Limpar",
            width=70,
            height=30,
            font=FONTS["text_small"],
            command=self.clear_log,
        )
        self.clear_log_btn.pack(side="right")

        self.log_text = ctk.CTkTextbox(self.log_card, font=FONTS["mono"], height=170)
        self.log_text.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self.log_text.configure(state="disabled")

    def _build_footer(self) -> None:
        self.footer = ctk.CTkFrame(self.root, corner_radius=10)
        self.footer.pack(fill="x", padx=18, pady=(0, 14))

        self.footer_left = ctk.CTkLabel(
            self.footer,
            text="Feito por valentisnoreply",
            font=FONTS["text_small"],
            cursor="hand2",
        )
        self.footer_left.pack(side="left", padx=14, pady=8)
        self.footer_left.bind("<Button-1>", lambda _: self._on_open_repo())

    def apply_theme(self, *, palette: dict[str, str], theme_name: str) -> None:
        self.root.configure(fg_color=palette["window"])

        self.topbar.configure(fg_color=palette["panel"])
        self.header.configure(fg_color=palette["panel"])
        self.content.configure(fg_color=palette["panel_alt"])
        self.footer.configure(fg_color=palette["panel"])

        for card in (
            self.url_card,
            self.info_card,
            self.quality_card,
            self.output_card,
            self.actions_card,
            self.log_card,
        ):
            card.configure(fg_color=palette["panel"])

        text_widgets = (
            self.title_label,
            self.url_label,
            self.quality_label,
            self.output_label,
            self.log_label,
            self.footer_left,
        )
        for widget in text_widgets:
            widget.configure(text_color=palette["text"])

        muted_widgets = (
            self.subtitle_label,
            self.video_info_label,
            self.status_label,
        )
        for widget in muted_widgets:
            widget.configure(text_color=palette["muted"])

        for entry in (self.url_entry, self.output_entry):
            entry.configure(
                fg_color=palette["input"],
                border_color=palette["border"],
                text_color=palette["text"],
                placeholder_text_color=palette["muted"],
            )

        self.quality_combo.configure(
            fg_color=palette["input"],
            border_color=palette["border"],
            button_color=palette["accent"],
            button_hover_color=palette["accent_hover"],
            text_color=palette["text"],
        )

        for primary in (
            self.analyze_btn,
            self.selected_btn,
            self.browse_btn,
            self.clear_log_btn,
            self.theme_btn,
        ):
            primary.configure(
                fg_color=palette["accent"],
                hover_color=palette["accent_hover"],
                text_color="#FFFFFF",
            )

        self.smart_btn.configure(
            fg_color=palette["secondary"],
            hover_color=palette["secondary_hover"],
            text_color="#FFFFFF",
        )
        self.progress.configure(progress_color=palette["progress"])
        self.log_text.configure(
            fg_color=palette["input"],
            border_color=palette["border"],
            text_color=palette["text"],
        )
        self.footer_left.configure(text_color=palette["link"])
        self.theme_btn.configure(text=f"Tema: {'Escuro' if theme_name == 'dark' else 'Claro'}")

    def set_busy(self, value: bool) -> None:
        state = "disabled" if value else "normal"
        for button in (
            self.analyze_btn,
            self.smart_btn,
            self.selected_btn,
            self.browse_btn,
            self.theme_btn,
        ):
            button.configure(state=state)

    def set_status(self, message: str) -> None:
        self.status_label.configure(text=message)

    def set_progress(self, percent: float) -> None:
        clamped = max(0.0, min(percent, 100.0))
        self.progress.set(clamped / 100.0)

    def set_video_info(self, text: str) -> None:
        self.video_info_label.configure(text=text)

    def append_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def clear_log(self) -> None:
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def set_formats(self, options: list[FormatOption]) -> None:
        self._format_options = options
        if not options:
            self.quality_combo.configure(values=["Nenhuma opcao de qualidade disponivel"])
            self.quality_combo.set("Nenhuma opcao de qualidade disponivel")
            return
        labels = [option.label for option in options]
        self.quality_combo.configure(values=labels)
        self.quality_combo.set(labels[0])

    def get_selected_format(self) -> FormatOption | None:
        if not self._format_options:
            return None
        selected = self.quality_combo.get()
        for option in self._format_options:
            if option.label == selected:
                return option
        return self._format_options[0]
