import tkinter as tk
from tkinter import ttk, messagebox
from WordPressSite import WordPressSite as wp


class application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.option_add('*Font', ('JetBrains Mono', 10))
        self.title("Formularz Wordpress")
        self.geometry("800x400")
        self.resizable(False, False)
        self.WordPress = wp()

        self.canvas = tk.Canvas(self,  highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, highlightthickness=0)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        # self.canvas.grid_propagate(False)
        self.canvas.config(width=800, height=400)
        self.scrollbar.grid(row=0, column=0, sticky='nse')

        self.create_widgets()

    def on_mousewheel(self, event):
        if (self.canvas.yview()[0] <= 0 and event.delta > 0) or (self.canvas.yview()[1] >= 1.0 and event.delta < 0):
            pass  # Nie przewijaj, jeśli jesteśmy na górze i próbujemy przewinąć do góry, lub na dole i próbujemy przewinąć w dół
        else:
            self.canvas.yview_scroll(-1*(event.delta//120), "units")

    def on_text_mousewheel(self, event):
        self.canvas.unbind("<MouseWheel>")
        self.entry2.yview_scroll(-1*(event.delta//120), "units")
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        return "break"

    def create_widgets(self):
        tk.Label(self.scrollable_frame, text="Tytuł").grid(row=0)
        tk.Label(self.scrollable_frame, text="Zawartość:").grid(row=1)
        tk.Label(self.scrollable_frame, text="Adres url:").grid(row=2)
        tk.Label(self.scrollable_frame, text="Kategoria:").grid(row=3, sticky='n')
        tk.Label(self.scrollable_frame, text="Tagi:").grid(row=4, sticky='n')

        self.entry1 = tk.Entry(self.scrollable_frame, width=25)
        self.entry2 = tk.Text(self.scrollable_frame, width=25, height=5)
        self.entry3 = tk.Entry(self.scrollable_frame, width=25)

        self.entry1.grid(row=0, column=1, ipadx=5, ipady=5, pady=5)
        self.entry2.grid(row=1, column=1, ipadx=5, ipady=5, pady=5)
        self.entry3.grid(row=2, column=1, ipadx=5, ipady=5, pady=5)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.scrollable_frame)
        scrollbar.grid(row=1, column=2, sticky='nsw')
        self.entry2.bind("<MouseWheel>", self.on_text_mousewheel)

        # Attach the scrollbar to the Text widget
        self.entry2.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.entry2.yview)

        self.categories = self.WordPress.get_categories()

        # Create a list for the categories
        self.category_vars = [tk.IntVar() for _ in self.categories]
        self.category_frame = ttk.Frame(self.scrollable_frame)
        self.category_frame.grid(row=3, column=1, sticky="w")

        for i, category in enumerate(self.categories):
            checkbutton = tk.Checkbutton(self.category_frame, text=category, variable=self.category_vars[i])
            checkbutton.grid(row=i, column=1, sticky="w")

        self.new_category_entry = tk.Entry(self.scrollable_frame)
        self.new_category_entry.grid(row=3, column=3, sticky=tk.NW, ipadx=5, ipady=5)
        self.new_category_entry.bind("<Return>", lambda event: self.add_category())

        tk.Button(self.scrollable_frame, text='Dodaj kategorię', command=self.add_category).grid(row=3, column=2, sticky=tk.NE)

        self.tags = self.WordPress.get_tags()

        # Create a list for the tags
        self.tag_vars = [tk.IntVar() for _ in self.tags]
        self.tag_frame = ttk.Frame(self.scrollable_frame)
        self.tag_frame.grid(row=4, column=1, sticky="w")

        for i, tag in enumerate(self.tags):
            checkbutton = tk.Checkbutton(self.tag_frame, text=tag, variable=self.tag_vars[i])
            checkbutton.grid(row=i, column=1, sticky="w")

        self.new_tag_entry = tk.Entry(self.scrollable_frame)
        self.new_tag_entry.grid(row=4, column=3, sticky=tk.NW, ipadx=5, ipady=5)
        self.new_tag_entry.bind("<Return>", lambda event: self.add_tag())

        tk.Button(self.scrollable_frame, text='Dodaj tag', command=self.add_tag).grid(row=4, column=2, sticky=tk.NE)

        tk.Button(self.scrollable_frame, text='Wyślij', command=self.submit_form).grid(row=5, column=1, sticky=tk.W, pady=4)

    def reset_form(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete("1.0", "end")
        self.entry3.delete(0, tk.END)

        self.categories = self.WordPress.get_categories()
        self.tags = self.WordPress.get_tags()

        self.category_vars = [tk.IntVar() for _ in self.categories]
        self.tag_vars = [tk.IntVar() for _ in self.tags]

        for widget in self.category_frame.winfo_children():
            widget.destroy()

        for i, category in enumerate(self.categories):
            checkbutton = tk.Checkbutton(self.category_frame, text=category, variable=self.category_vars[i])
            checkbutton.grid(row=i, column=1, sticky="w")

        for widget in self.tag_frame.winfo_children():
            widget.destroy()

        for i, tag in enumerate(self.tags):
            checkbutton = tk.Checkbutton(self.tag_frame, text=tag, variable=self.tag_vars[i])
            checkbutton.grid(row=i, column=1, sticky="w")

    def submit_form(self):
        title = self.entry1.get().strip()
        content = self.entry2.get("1.0", "end").strip()
        selected_categories = [self.categories[i] for i, var in enumerate(self.category_vars) if var.get()]
        selected_tags = [self.tags[i] for i, var in enumerate(self.tag_vars) if var.get()]
        post_url = self.entry3.get().strip()

        if (title == "" or content == ""):
            messagebox.showerror("Błąd", "Wypełnij wszystkie pola!")
            return
        print(selected_categories)
        print(selected_tags)
        self.WordPress.create_post(title, content, categories=selected_categories, tags=selected_tags, post_url=post_url)
        # messagebox.showinfo("Formularz", "Formularz został wysłany!")
        self.reset_form()

    def add_category(self):
        new_category = self.new_category_entry.get().strip()
        if new_category:
            self.category_vars.append(tk.IntVar())
            checkbutton = tk.Checkbutton(self.category_frame, text=new_category, variable=self.category_vars[-1])
            checkbutton.grid(row=len(self.categories), column=1, sticky="w")
            self.categories.append(new_category)
            self.new_category_entry.delete(0, tk.END)

    def add_tag(self):
        new_tag = self.new_tag_entry.get().strip()
        if new_tag:
            self.tag_vars.append(tk.IntVar())
            checkbutton = tk.Checkbutton(self.tag_frame, text=new_tag, variable=self.tag_vars[-1])
            checkbutton.grid(row=len(self.tags), column=1, sticky="w")
            self.tags.append(new_tag)
            self.new_tag_entry.delete(0, tk.END)

    def on_selected_categories(self, event):
        self.on_selected_categories = [self.categories_listbox.get(i) for i in self.categories_listbox.curselection()]

    def on_selected_tags(self, event):
        self.on_selected_tags = [self.tags_listbox.get(i) for i in self.tags_listbox.curselection()]


if __name__ == "__main__":
    app = application()
    app.mainloop()
