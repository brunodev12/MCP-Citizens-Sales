from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter import filedialog as FileDialog
from settings import set_apis
import raw_data
from get_price import get_sales
import auxclass

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")

class UpWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h*3)
        self.geometry(f"{w}x{h}+{x}+{y}")

class help(Toplevel, CenterWidgetMixin):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.text = text
        self.title("Help")
        self.build(self.text)
        self.center()
    
    def build(self, text):
        frame = Frame(self)
        frame.pack()
        t = Text(frame, height=3, width=130, bg='lightgrey', relief='flat')
        t.insert(END, f"{text}")
        t.config(state=DISABLED)
        t.pack()

class addData(Toplevel, CenterWidgetMixin):
    def __init__(self, parent, title, side, func):
        super().__init__(parent)
        self.title(f"{title}")
        self.side = side
        self.func = func
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
    
    def build(self):
        frame = Frame(self)
        frame.pack()
        Label(frame, text="Enter the path of the .csv file").grid(row=0, column=0)
        self.data_entry = Entry(frame, width=80)
        self.data_entry.grid(row=0, column=1)
        Button(frame, text="Search", command=self.search_csvfile).grid(row=0, column=2)
        frame2 = Frame(self)
        frame2.pack()
        Button(frame2, text="Help", command=self.help_add_data).grid(row=0, column=0)
        Button(frame2, text="Ok", command=self.ok_adddata).grid(row=0, column=1)
        Button(frame2, text="Cancel", command=self.close).grid(row=0, column=2)
    
    def search_csvfile(self):
        path = FileDialog.askopenfilename(title="Open a file", filetypes=(("Csv files",".csv"),("All files","*.*")))
        self.data_entry.delete(0, END)
        self.data_entry.insert(0, path)

    def help_add_data(self):
        text1 = "You can get the .csv file at:"
        if self.side == 0:
            text_eth = "https://polygonscan.com/exportData?type=tokentxns-nft&contract=0x726e1b4841968c0c3eebeef880e60875b745b3c0&a=&decimal=0"
            text2_eth = "You will get all the transactions made about citizens on the eth side, in the selected time range."
            help(self, text=f"{text1}\n{text_eth}\n{text2_eth}")
        if self.side == 1:
            text_trx = "https://polygonscan.com/exportData?type=tokentxns-nft&contract=0x19ed22f59ac603f9f63339eff27cf6b199db269e&a=&decimal=0"
            text2_trx = "You will get all the transactions made about citizens on the trx side, in the selected time range."
            help(self, text=f"{text1}\n{text_trx}\n{text2_trx}")

    def ok_adddata(self):
        path = self.data_entry.get()
        try:
            raw_data.new_file(self.side, path) if self.func == "new" else raw_data.add_data(self.side, path)
            MessageBox.showinfo("Status", "Data added successfully")
            self.close()
        except FileNotFoundError:
            MessageBox.showerror("Status", "The file does not exist, check the name of the .csv file")
        except KeyError:
            MessageBox.showerror("Status", "Unexpected error, make sure the file is .csv")
        except NotADirectoryError:
            MessageBox.showerror("Status", "Wrong directory")

    def close(self):
        self.destroy()
        self.update()

class Next(Toplevel, CenterWidgetMixin):
    def __init__(self, parent, side):
        super().__init__(parent)
        self.name = "eth" if side==0 else "trx"
        self.title(f"Data {self.name} side")
        self.side = side
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
    
    def build(self):
        frame=Frame(self)
        frame.pack()
        Button(frame, text="Get Data", command=self.get_data).pack(padx=60,pady=20)
        Button(frame, text="Show Data", command=self.show_data).pack(padx=60, pady=20)
        self.message = StringVar()
        self.message.set("Status: ready")
        self.statusbar = Label(frame, textvar=self.message, justify='left')
        self.statusbar.pack(side="left")

    def get_data(self):
        self.message.set("Status: working...")
        confirm = MessageBox.askokcancel(f"Data {self.name} side","The information will be processed, this may take several minutes")
        if confirm:
            try:
                get_sales(self.side)
                MessageBox.showinfo("Status", "Data was processed correctly")
                self.message.set("Status: ready")
            except IndexError:
                MessageBox.showerror("Status", f"Unexpected error, are you sure the raw data is from the {self.name} side?")
                self.message.set("Status: ready")
            except FileNotFoundError:
                MessageBox.showerror("Status", "File not found, you must get the raw data first.")
                self.message.set("Status: ready")
            except ValueError:
                MessageBox.showerror("Status", "No API Key entered or API key incorrect.")
                self.message.set("Status: ready")
            except:
                MessageBox.showerror("Status", "Unexpected error. Have you entered the API KEY?")
                self.message.set("Status: ready")
        else:
            self.message.set("Status: ready")
    
    def show_data(self):
        try:
            auxclass.ShowData(self, dirname = self.name)
        except FileNotFoundError:
            MessageBox.showerror("Status", "File not found. You must get the data first.")
            auxclass.ShowData.close(self)

class secondWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent, title, side):
        super().__init__(parent)
        self.title(f"{title}")
        self.side = side
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
    
    def build(self):
        frame = Frame(self)
        frame.pack()
        frame2 = Frame(self)
        frame2.pack()
        Button(frame, text="New raw data", command=self.new_data).grid(row=0, column=0, pady=20, padx=20)
        Button(frame, text="Add more raw data", command=self.add_data).grid(row=0, column=2, pady=20, padx=20)
        Button(frame2, text="Help", command=self.help_raw_data).grid(row=0, column=0)
        Button(frame2, text="Next", command=self.next).grid(row=0, column=1)
        Button(frame2, text="Cancel", command=self.close).grid(row=0, column=2)
    
    def help_raw_data(self):
        text1= "New raw data: Create a new file, if any exist they will be deleted"
        text2= "Add more raw data: Add more data to an existing file"
        text3= "Next: Continue to the next step where the raw data will be processed or you can display the processed data if you already have it"
        help(self, text=f"{text1}\n{text2}\n{text3}")
    
    def new_data(self):
        addData(self, title="New raw data", side=self.side, func="new")
    
    def add_data(self):
        addData(self, title="Add more raw data", side=self.side, func="add")
    
    def next(self):
        Next(self, side=self.side)

    def close(self):
        self.destroy()
        self.update()

class API_Key_Window(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("API Key Settings")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
    
    def build(self):
        frame = Frame(self)
        frame.pack()
        Label(frame, text="Enter your polygonscan apikey").grid(row=0, column=0)
        self.polygon_api = Entry(frame, width=40)
        self.polygon_api.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        self.polygon_api.grid(row=0, column=1)
        Button(frame, text="Help", command=self.help_polygonapi).grid(row=0, column=2)
        Label(frame, text="Enter your moralis apikey").grid(row=1, column=0)
        self.moralis_api = Entry(frame, width=40)
        self.moralis_api.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        self.moralis_api.grid(row=1, column=1)
        Button(frame, text="Help", command=self.help_moralisapi).grid(row=1, column=2)

        frame2 = Frame(self)
        frame2.pack()
        savebutton = Button(frame2, text="Save", command=self.save)
        savebutton.config(state=DISABLED)
        savebutton.grid(row=0, column=0, pady=20, padx=20)
        Button(frame2, text="Cancel", command=self.close).grid(row=0, column=1, pady=20, padx=20)

        self.validations = [0, 0]
        self.savebutton = savebutton
    
    def help_polygonapi(self):
        help(self, text="You can get your polygonscan api key at:\nhttps://docs.polygonscan.com/getting-started/viewing-api-usage-statistics")
    
    def help_moralisapi(self):
        text1="You can get your moralis api key at:"
        text2="https://docs.moralis.io/reference/getting-the-api-key"
        text3="Also, you can leave this field blank and the test api will be used (Not guaranteed to work correctly)"
        help(self, text=f"{text1}\n{text2}\n{text3}")
    
    def save(self):
        polygonapi = self.polygon_api.get()
        moralisapi = self.moralis_api.get()
        if len(moralisapi) == 0:
            moralisapi = "test"
        try:
            set_apis(polygonapi, moralisapi)
            MessageBox.showinfo("Status", "API KEY added successfully")
        except:
            MessageBox.showerror("Status", "An unexpected error occurred")
        self.close()

    def validate(self, event, index):
        value = event.widget.get()
        valid = [1 if (len(value) == 34 and index == 0) or ((value=="test" or len(value)==64 or len(value) == 0) and index==1) else 0]
        event.widget.configure({"bg":"Green" if valid[0] == 1 else "Red"})

        self.validations[index] = valid[0]
        self.savebutton.config(state=NORMAL if self.validations == [1, 1] else DISABLED)

    def close(self):
        self.destroy()
        self.update()


class MainWindow(Tk, UpWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Citizens Sales")
        self.build()
        self.center()
    
    def build(self):
        
        frame = Frame(self)
        frame.pack()
        Label(frame, text="Which side do you want to get the information from?").grid(row=0, column=1)
        Button(frame, text="ETH", command=self.ethside).grid(row=1, column=0)
        Button(frame, text="TRX", command=self.trxside).grid(row=1, column=2)
        frame2 = Frame(self)
        frame2.pack()
        Label(frame2, text="In order to obtain the sales information you need to configure the API KEY (only once)").grid(row=2, column=1)
        Button(frame2, text="SET API KEY", command=self.apikey).grid(row=3, column=1, pady=10)
    
    def ethside(self):
        secondWindow(self, title="Citizens Sales Eth Side", side=0)
    
    def trxside(self):
        secondWindow(self, title="Citizens Sales Trx Side", side=1)
    
    def apikey(self):
        API_Key_Window(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
