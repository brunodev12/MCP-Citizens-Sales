from sre_parse import State
from tkinter import *
from tkinter import ttk
import pandas as pd

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h*2}+{x}+{y}")

class ShowData(Toplevel, CenterWidgetMixin):
    def __init__(self, parent, dirname):
        super().__init__(parent)
        self.dirname = dirname
        self.title(f"Show data {self.dirname} side")
        self.build()
        self.center()
        self.grab_set()
    
    def build(self):
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=1)

        self.treeview = ttk.Treeview(frame)
        self.treeview['columns'] = ('DateTime', 'Txhash', 'Token_ID', 'Sale_price', 'Rank',
                                'Gender', 'Generation', 'Strength', 'Endurance',
                                'Charisma', 'Intelligence', 'Agility', 'Luck')

        self.treeview.column("#0", width=0, stretch=NO)
        self.treeview.column("DateTime", width=150, anchor=CENTER)
        self.treeview.column("Txhash", width=600, anchor=CENTER)
        self.treeview.column("Token_ID", width=80, anchor=CENTER)
        self.treeview.column("Sale_price", width=100, anchor=CENTER)
        self.treeview.column("Rank", width=150, anchor=CENTER)
        self.treeview.column("Gender", width=80, anchor=CENTER)
        self.treeview.column("Generation", width=100, anchor=CENTER)
        self.treeview.column("Strength", width=80, anchor=CENTER)
        self.treeview.column("Endurance", width=90, anchor=CENTER)
        self.treeview.column("Charisma", width=80, anchor=CENTER)
        self.treeview.column("Intelligence", width=120, anchor=CENTER)
        self.treeview.column("Agility", width=70, anchor=CENTER)
        self.treeview.column("Luck", width=60, anchor=CENTER)

        self.treeview.heading("DateTime", text="Datetime", anchor=CENTER, command=lambda: self.sort_columns("DateTime"))
        self.treeview.heading("Txhash", text="Txhash", anchor=CENTER, command=lambda: self.sort_columns("Txhash"))
        self.treeview.heading("Token_ID", text="Token ID", anchor=CENTER, command=lambda: self.sort_columns("Token_ID", int))
        self.treeview.heading("Sale_price", text="Sale price", anchor=CENTER, command=lambda: self.sort_columns("Sale_price", float))
        self.treeview.heading("Rank", text="Rank", anchor=CENTER, command=lambda: self.sort_columns("Rank"))
        self.treeview.heading("Gender", text="Gender", anchor=CENTER, command=lambda: self.sort_columns("Gender"))
        self.treeview.heading("Generation", text="Generation", anchor=CENTER, command=lambda: self.sort_columns("Generation"))
        self.treeview.heading("Strength", text="Strength", anchor=CENTER, command=lambda: self.sort_columns("Strength", int))
        self.treeview.heading("Endurance", text="Endurance", anchor=CENTER, command=lambda: self.sort_columns("Endurance", int))
        self.treeview.heading("Charisma", text="Charisma", anchor=CENTER, command=lambda: self.sort_columns("Charisma", int))
        self.treeview.heading("Intelligence", text="Intelligence", anchor=CENTER, command=lambda: self.sort_columns("Intelligence", int))
        self.treeview.heading("Agility", text="Agility", anchor=CENTER, command=lambda: self.sort_columns("Agility", int))
        self.treeview.heading("Luck", text="Luck", anchor=CENTER, command=lambda: self.sort_columns("Luck", int))

        self.treeview.tag_configure('gray', background='lightgray')
        self.treeview.tag_configure('normal', background='white')
        

        yscrollbar = Scrollbar(frame, command=self.treeview.yview)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(frame, command=self.treeview.xview, orient='horizontal')
        xscrollbar.pack(side=BOTTOM, fill='x')

        self.treeview['yscrollcommand'] = yscrollbar.set
        self.treeview['xscrollcommand'] = xscrollbar.set

        self.df=pd.read_csv(f"{self.dirname}/Citizens_sales.csv")
        self.df.fillna(0, inplace=True)

        my_tag = 'normal'
        for index, row in self.df.iterrows():
            my_tag = 'gray' if my_tag=='normal' else 'normal'
            self.treeview.insert(
                parent='', index='end', iid=row['Txhash'],
                values=(row['DateTime'],
                row['Txhash'],
                row['Token_ID'],
                row['Sale_price'],
                row['Rank'],
                row['Gender'],
                row['Generation'],
                row['Strength'],
                row['Endurance'],
                row['Charisma'],
                row['Intelligence'],
                row['Agility'],
                row['Luck']),
                tags=my_tag
            )

        self.treeview.pack(fill=BOTH, expand=1)
    
        self.treeview.bind('<ButtonRelease-3>', self.click_handler)

    def click_handler(self, event):
        cur_item = self.treeview.item(self.treeview.focus())
        col = self.treeview.identify_column(event.x)
        try:
            if col == '#2':
                Tk.clipboard_clear(self)
                Tk.clipboard_append(self, cur_item['values'][1])
                print(cur_item['values'][1], "copied to clipboard")
            if col == '#3':
                Tk.clipboard_clear(self)
                Tk.clipboard_append(self, cur_item['values'][2])
                print(cur_item['values'][2], "copied to clipboard")
        except IndexError:
            pass

    def sort_columns(self, namecolumn="", type=str):
        self.treeview.delete(*self.treeview.get_children())
        self.df[namecolumn] = self.df[namecolumn].astype(type)
        self.df.sort_values([namecolumn], inplace=True, ascending=True if self.df[namecolumn].is_monotonic_increasing==False else False)
        my_tag = 'normal'
        for index, row in self.df.iterrows():
            my_tag = 'gray' if my_tag=='normal' else 'normal'
            self.treeview.insert(
                parent='', index='end', iid=row['Txhash'],
                values=(row['DateTime'],
                row['Txhash'],
                row['Token_ID'],
                row['Sale_price'],
                row['Rank'],
                row['Gender'],
                row['Generation'],
                row['Strength'],
                row['Endurance'],
                row['Charisma'],
                row['Intelligence'],
                row['Agility'],
                row['Luck']),
                tags=my_tag
            )
