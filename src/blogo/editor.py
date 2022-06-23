# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from tkinter import BOTH
from tkinter import END
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import Frame
from tkinter import Menu
from tkinter import Text
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox as mbox

from markdown2 import Markdown
from tkhtmlview import HTMLLabel


class Editor(Frame):
    """Creates a blogo post editor using tkinter."""

    def __init__(self, master=None, title=None, path=None, directory=None):
        """Creates an instance of a markdown file editor for blogo posts.

        Args:
            master (Tk, optional): A Tk object to create a window frame for. Defaults to None.
            title (str, optional): The title of the blog to edit. Defaults to None.
            path (str, optional): The path to the blog file to edit. Defaults to None.
            directory (str, optional): The path to a the directory containing blogs. Defaults to None.
        """
        self.title = title
        self.path = path
        self.directory = directory
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        """Creates the initial editor window frame."""
        blogo_font = font.Font(family="Helvetica", size="14")
        self.master.title(self.title if self.title else "Blogo")
        self.pack(fill=BOTH, expand=1)
        self.input_editor = Text(self, width="1", font=blogo_font)
        self.input_editor.pack(fill=BOTH, expand=1, side=LEFT)
        self.output_box = HTMLLabel(self, width="1", background="white", html=f"<h1>{self.title}</h1>")
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
        """Callback used when input changes in the editor."""
        self.input_editor.edit_modified(0)
        md2html = Markdown()
        markdown_text = self.input_editor.get("1.0", END)
        html = md2html.convert(markdown_text)
        self.output_box.set_html(html)

    def open_file(self):
        """Creates an open file dialog option."""
        open_file_name = filedialog.askopenfilename(
            filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"), ("Text File", "*.txt"), ("All Files", "*.*"))
        )
        if open_file_name:
            try:
                self.input_editor.delete(1.0, END)
                self.input_editor.insert(END, open(open_file_name).read())
            except Exception as e:
                mbox.showerror(
                    "Error Opening Selected File", f"Oops!, The file you selected : {open_file_name} can not be opened!"
                )

    def save_file(self):
        """Creates a save file dialog option."""
        filedata = self.input_editor.get("1.0", END)
        save_file_name = filedialog.asksaveasfilename(
            filetypes=(("Markdown File", "*.md"), ("Text File", "*.txt")),
            title="Save Markdown File",
            initialfile=self.path,
            initialdir=self.directory if not self.path else None,
        )
        if save_file_name:
            try:
                f = open(save_file_name, "w")
                f.write(filedata)
            except Exception as e:
                mbox.showerror("Error Saving File", f"Oops!, The File : {save_file_name} can not be saved!")
