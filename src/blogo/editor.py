from tkinter import *
from tkinter import font, filedialog
from tkinter import messagebox as mbox
from markdown2 import Markdown
from tkhtmlview import HTMLLabel


class Editor(Frame):

    def __init__(self, master=None, title=None, path=None, directory=None):
        self.title = title
        self.path = path
        self.directory = directory
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        BLOGO_FONT = font.Font(
            family="Helvetica",
            size="14"
        )
        self.master.title(self.title if self.title else "Blogo")
        self.pack(fill=BOTH, expand=1)
        self.input_editor = Text(self, width="1", font=BLOGO_FONT)
        self.input_editor.pack(fill=BOTH, expand=1, side=LEFT)
        self.output_box = HTMLLabel(
            self, width="1", background="white", html=f"<h1>{self.title}</h1>"
        )
        self.output_box.pack(fill=BOTH, expand=1, side=RIGHT)
        self.output_box.fit_height()
        self.input_editor.bind("<<Modified>>", self.on_input_change)
        self.mainmenu = Menu(self)
        self.file_menu = Menu(self.mainmenu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save as", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.mainmenu.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.mainmenu)

    def on_input_change(self, event):
        self.input_editor.edit_modified(0)
        md2html = Markdown()
        markdownText = self.input_editor.get("1.0", END)
        html = md2html.convert(markdownText)
        self.output_box.set_html(html)

    def open_file(self):
        open_file_name = filedialog.askopenfilename(
            filetypes=(
                ("Markdown File", "*.md , *.mdown , *.markdown"),
                ("Text File", "*.txt"),
                ("All Files", "*.*")
            )
        )
        if open_file_name:
            try:
                self.input_editor.delete(1.0, END)
                self.input_editor.insert(END, open(open_file_name).read())
            except:
                mbox.showerror(
                    "Error Opening Selected File" , 
                    f"Oops!, The file you selected : {open_file_name} can not be opened!"
                )

    def save_file(self):
        from pathlib import Path
        filedata = self.input_editor.get("1.0" , END)
        save_file_name = filedialog.asksaveasfilename(
           # parent=self,
            filetypes = (
                ("Markdown File", "*.md"),
                ("Text File", "*.txt")
            ), 
            title="Save Markdown File",
            initialfile=self.path,
            initialdir=self.directory if not self.path else None
        )
        if save_file_name:
            try:
                f = open(save_file_name , "w")
                f.write(filedata)
            except:
                mbox.showerror(
                    "Error Saving File" , 
                    f"Oops!, The File : {save_file_name} can not be saved!"
                )
