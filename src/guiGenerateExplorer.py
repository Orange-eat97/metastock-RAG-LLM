from __future__ import annotations

import ctypes
import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


# Make Tkinter sharper on Windows high-DPI displays.
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


REPO_ROOT = Path(r"C:\GitHub\metastock-RAG-LLM")


class MetaStockLLMGui:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.tk.call("tk", "scaling", 1.25)

        self.root.title("MetaStock LLM Automator")
        self.root.geometry("980x760")
        self.root.minsize(820, 620)

        self.output_queue: queue.Queue[str] = queue.Queue()
        self.worker: threading.Thread | None = None
        self.process: subprocess.Popen | None = None

        self.prompt_var = tk.StringVar()

        # LLM / storage options
        self.save_excel_var = tk.BooleanVar(value=True)
        self.save_supabase_var = tk.BooleanVar(value=True)
        self.use_supabase_cache_var = tk.BooleanVar(value=True)
        self.cache_any_model_var = tk.BooleanVar(value=False)

        # Automator options
        self.run_automator_var = tk.BooleanVar(value=False)
        self.automator_dry_run_var = tk.BooleanVar(value=True)
        self.instruments_var = tk.StringVar(value="all")

        self._build_ui()
        self._poll_output_queue()

    def run(self) -> None:
        self.root.mainloop()

    # ============================================================
    # UI
    # ============================================================

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text="MetaStock LLM Automator",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w", pady=(0, 12))

        # ------------------------------------------------------------
        # Prompt
        # ------------------------------------------------------------

        prompt_frame = ttk.LabelFrame(main, text="Prompt", padding=10)
        prompt_frame.pack(fill="x", pady=(0, 12))

        self.prompt_entry = ttk.Entry(prompt_frame, textvariable=self.prompt_var)
        self.prompt_entry.pack(fill="x", pady=(0, 8))
        self.prompt_entry.bind("<Return>", lambda _event: self._on_start_clicked())

        hint = ttk.Label(
            prompt_frame,
            text=(
                "Example: Find stocks where RSI is below 30 and close is above "
                "50 day moving average"
            ),
            foreground="#555555",
        )
        hint.pack(anchor="w")

        # ------------------------------------------------------------
        # Storage / cache options
        # ------------------------------------------------------------

        storage_frame = ttk.LabelFrame(main, text="Storage and Cache", padding=10)
        storage_frame.pack(fill="x", pady=(0, 12))

        ttk.Checkbutton(
            storage_frame,
            text="Save to Excel",
            variable=self.save_excel_var,
        ).pack(side="left", padx=(0, 18))

        ttk.Checkbutton(
            storage_frame,
            text="Save to Supabase",
            variable=self.save_supabase_var,
        ).pack(side="left", padx=(0, 18))

        ttk.Checkbutton(
            storage_frame,
            text="Use Supabase cache",
            variable=self.use_supabase_cache_var,
        ).pack(side="left", padx=(0, 18))

        ttk.Checkbutton(
            storage_frame,
            text="Cache any model",
            variable=self.cache_any_model_var,
        ).pack(side="left")

        # ------------------------------------------------------------
        # Automator options
        # ------------------------------------------------------------

        automator_frame = ttk.LabelFrame(main, text="Automator", padding=10)
        automator_frame.pack(fill="x", pady=(0, 12))

        ttk.Checkbutton(
            automator_frame,
            text="Run automator after generation",
            variable=self.run_automator_var,
        ).pack(side="left", padx=(0, 18))

        ttk.Checkbutton(
            automator_frame,
            text="Automator dry run",
            variable=self.automator_dry_run_var,
        ).pack(side="left", padx=(0, 18))

        ttk.Label(automator_frame, text="Instruments:").pack(side="left")

        ttk.Entry(
            automator_frame,
            textvariable=self.instruments_var,
            width=20,
        ).pack(side="left", padx=(6, 0))

        # ------------------------------------------------------------
        # Buttons
        # ------------------------------------------------------------

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(0, 10))

        self.start_button = ttk.Button(
            buttons,
            text="Generate",
            command=self._on_start_clicked,
        )
        self.start_button.pack(side="left")

        self.stop_button = ttk.Button(
            buttons,
            text="Stop",
            command=self._on_stop_clicked,
            state="disabled",
        )
        self.stop_button.pack(side="left", padx=(8, 0))

        ttk.Button(
            buttons,
            text="Clear Log",
            command=self._clear_log,
        ).pack(side="left", padx=(8, 0))

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status_var).pack(anchor="w", pady=(0, 6))

        # ------------------------------------------------------------
        # Log box
        # ------------------------------------------------------------

        log_frame = ttk.LabelFrame(main, text="Process Log", padding=8)
        log_frame.pack(fill="both", expand=True)

        self.log_box = tk.Text(log_frame, wrap="word", height=28)
        self.log_box.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_box.configure(yscrollcommand=scrollbar.set)

    # ============================================================
    # Command construction
    # ============================================================

    def _build_command(self, prompt: str) -> list[str]:
        cmd = [
            sys.executable,
            "-m",
            "src.generate_explorer",
            prompt,
        ]

        # Excel saving
        if not self.save_excel_var.get():
            cmd.append("--no-save")

        # Supabase saving
        if self.save_supabase_var.get():
            cmd.append("--save-supabase")

        # Supabase cache
        if self.use_supabase_cache_var.get():
            cmd.append("--use-supabase-cache")

        if self.cache_any_model_var.get():
            cmd.append("--cache-any-model")

        # Automator
        if self.run_automator_var.get():
            cmd.append("--run-automator")

        if self.automator_dry_run_var.get():
            cmd.append("--automator-dry-run")

        instruments = self.instruments_var.get().strip() or "all"
        cmd.extend(["--instruments", instruments])

        return cmd
    
    def _clean_prompt(self, prompt: str) -> str:
        """
        Remove accidental wrapping quotes from GUI input.

        Examples:
            "Find stocks..."  -> Find stocks...
            'Find stocks...'  -> Find stocks...
            ""Find stocks..."" -> Find stocks...
        """
        text = (prompt or "").strip()

        changed = True
        while changed and len(text) >= 2:
            changed = False

            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1].strip()
                changed = True

            if text.startswith("'") and text.endswith("'"):
                text = text[1:-1].strip()
                changed = True

        return text

    # ============================================================
    # Event handlers
    # ============================================================

    def _on_start_clicked(self) -> None:
        if self.worker and self.worker.is_alive():
            messagebox.showinfo("MetaStock LLM Automator", "A run is already active.")
            return

        prompt = self._clean_prompt(self.prompt_var.get())

        if not prompt:
            messagebox.showerror("Missing prompt", "Please enter a prompt.")
            return

        if self.run_automator_var.get() and not self.save_excel_var.get():
            messagebox.showerror(
                "Invalid option combination",
                (
                    "The current automator bridge still reads from Excel. "
                    "Keep 'Save to Excel' enabled when running automator.\n\n"
                    "Later, after the Supabase API bridge is implemented, this restriction can be removed."
                ),
            )
            return

        cmd = self._build_command(prompt)

        self._append_log("\n=== Starting MetaStock LLM workflow ===\n")
        self._append_log(f"Prompt: {prompt}\n")
        self._append_log(f"Command: {self._format_command(cmd)}\n\n")

        self.status_var.set("Running...")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        self.worker = threading.Thread(
            target=self._run_subprocess,
            args=(cmd,),
            daemon=True,
        )
        self.worker.start()

    def _on_stop_clicked(self) -> None:
        if self.process and self.process.poll() is None:
            self._append_log("\n[GUI] Stopping process...\n")
            self.process.terminate()
            self.status_var.set("Stopping...")

    # ============================================================
    # Subprocess / log streaming
    # ============================================================

    def _run_subprocess(self, cmd: list[str]) -> None:
        try:
            self.process = subprocess.Popen(
                cmd,
                cwd=str(REPO_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            assert self.process.stdout is not None

            for line in self.process.stdout:
                self.output_queue.put(line)

            return_code = self.process.wait()

            if return_code == 0:
                self.output_queue.put("\n=== Workflow completed successfully ===\n")
                self.output_queue.put("__STATUS_READY__")
            else:
                self.output_queue.put(
                    f"\n=== Workflow failed with exit code {return_code} ===\n"
                )
                self.output_queue.put("__STATUS_FAILED__")

        except Exception as e:
            self.output_queue.put(f"\n[GUI ERROR] {e}\n")
            self.output_queue.put("__STATUS_FAILED__")

    def _poll_output_queue(self) -> None:
        try:
            while True:
                text = self.output_queue.get_nowait()

                if text == "__STATUS_READY__":
                    self.status_var.set("Ready")
                    self.start_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    continue

                if text == "__STATUS_FAILED__":
                    self.status_var.set("Failed")
                    self.start_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    continue

                self._append_log(text)

        except queue.Empty:
            pass

        self.root.after(100, self._poll_output_queue)

    def _append_log(self, text: str) -> None:
        self.log_box.insert("end", text)
        self.log_box.see("end")

    def _clear_log(self) -> None:
        self.log_box.delete("1.0", "end")

    @staticmethod
    def _format_command(cmd: list[str]) -> str:
        return " ".join(f'"{part}"' if " " in part else part for part in cmd)


def main() -> None:
    app = MetaStockLLMGui()
    app.run()


if __name__ == "__main__":
    main()