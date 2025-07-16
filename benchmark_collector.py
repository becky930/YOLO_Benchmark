#This file is intended to merge all GPU benchmark csv files into one 

import pandas as pd
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def merge_csv_files(file_paths):
    merged_list = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            filename = os.path.basename(file_path)
            gpu_model = filename.split('_')[0]  # Ex: RTX4090
            df['GPU_Model'] = gpu_model
            merged_list.append(df)
        except Exception as e:
            print(f"❌ {file_path} 처리 중 오류: {e}")
    if merged_list:
        merged_df = pd.concat(merged_list, ignore_index=True)
        return merged_df
    else:
        return None

def save_to_excel(df, output_path):
    try:
        df.to_excel(output_path, index=False)
        return True
    except Exception as e:
        print(f"❌ 저장 중 오류: {e}")
        return False

class DragDropCSVApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV 병합기 - Drag & Drop 지원")
        self.geometry("700x400")
        self.configure(bg="#f7f7f7")

        self.selected_files = []

        self.label = ttk.Label(self, text="① 아래 박스에 CSV 파일들을 드래그하거나 버튼을 눌러 추가하세요", font=("Arial", 11))
        self.label.pack(pady=10)

        self.drop_area = tk.Listbox(self, width=90, height=12, bg="white")
        self.drop_area.pack(pady=10)

        # Enable dropping
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.drop_files)

        self.add_button = ttk.Button(self, text="파일 수동 선택", command=self.select_files)
        self.add_button.pack(pady=5)

        self.save_button = ttk.Button(self, text="② 병합 후 Excel로 저장", command=self.merge_and_save)
        self.save_button.pack(pady=10)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        self.add_files(file_paths)

    def drop_files(self, event):
        raw_files = self.tk.splitlist(event.data)
        csv_files = [f for f in raw_files if f.endswith('.csv')]
        self.add_files(csv_files)

    def add_files(self, file_paths):
        for f in file_paths:
            if f not in self.selected_files:
                self.selected_files.append(f)
                self.drop_area.insert(tk.END, f)

    def merge_and_save(self):
        if not self.selected_files:
            messagebox.showwarning("⚠️ 파일 없음", "CSV 파일을 먼저 추가하세요.")
            return
        merged_df = merge_csv_files(self.selected_files)
        if merged_df is None:
            messagebox.showerror("오류", "파일 병합 중 오류가 발생했습니다.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            success = save_to_excel(merged_df, save_path)
            if success:
                messagebox.showinfo("✅ 완료", f"병합 완료!\n저장 위치:\n{save_path}")
            else:
                messagebox.showerror("오류", "Excel 저장 실패")

if __name__ == "__main__":
    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
        class DragDropCSVApp(DragDropCSVApp, TkinterDnD.Tk):
            pass
    except ImportError:
        print("⚠️ tkinterDnD2가 설치되어 있지 않습니다. Drag & Drop 없이 실행됩니다.")

    app = DragDropCSVApp()
    app.mainloop()
