import os
import sys

from tkinter import messagebox
from tkinter import ttk
import tkinter as tk


class TextSort:
    def main(self):
        self._create_GUI()

    def _create_GUI(self):
        self.root = tk.Tk()
        self.root.title("Text sort")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        iconfile = "icon.ico"
        # PyInstallerでビルドされた場合、展開先を取得
        if getattr(sys, "frozen", False):
            # PyInstallerの一時ディレクトリ
            iconfile = os.path.join(sys._MEIPASS, iconfile)
        self.root.iconbitmap(default=iconfile)

        self.before_text = PlaceholderText(
            self.root, "ソートしたい文字列を入力してください。", height=10
        )
        self.before_text.pack(padx=10, pady=10)
        self.before_text.configure(padx=5, pady=5)

        frame1 = ttk.Frame(self.root)
        frame1.pack()
        tk.Button(frame1, text=("昇順↑"), command=lambda: self._sort_text(False)).grid(
            row=1, column=0, padx=10, pady=5
        )
        tk.Button(frame1, text=("降順↓"), command=lambda: self._sort_text(True)).grid(
            row=1, column=1, padx=10, pady=5
        )

        self.after_text = tk.Text(self.root, bd=1, height=10)
        self.after_text.pack(padx=10, pady=10)
        self.before_text.configure(padx=5, pady=5)

        tk.Button(self.root, text="Copy", command=lambda: self._copy_clipboard()).pack()

        self.root.mainloop()

    def _sort_text(self, bool):
        if not self.before_text.has_placeholder:
            before_text_list = [
                line
                for line in self.before_text.get(0.0, tk.END).split("\n")
                if line.strip()
            ]
            after_text_list = sorted(before_text_list, reverse=bool)

            self.after_text.delete(0.0, tk.END)
            self.after_text.insert(tk.END, "\n".join(after_text_list))

    def _copy_clipboard(self):
        text = self.after_text.get(0.0, tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("メッセージ", "copied!")


class PlaceholderText(tk.Text):
    def __init__(self, master=None, placeholder="Enter text here...", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.has_placeholder = False
        self.insert_placeholder()

        # フォーカスイベントをバインド
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def insert_placeholder(self):
        """プレースホルダーを挿入"""
        self.insert(0.0, self.placeholder)
        self.config(fg="gray")
        self.has_placeholder = True

    def _clear_placeholder(self, event=None):
        """フォーカス時にプレースホルダーを削除"""
        if self.has_placeholder:
            self.delete(0.0, tk.END)
            self.config(fg="black")
            self.has_placeholder = False

    def _add_placeholder(self, event=None):
        """フォーカスアウト時にプレースホルダーを追加"""
        if not self.get(0.0, tk.END).strip():
            self.insert_placeholder()


if __name__ == "__main__":
    ts = TextSort()
    ts.main()
