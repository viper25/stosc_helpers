import customtkinter
from widget_classes.GenerateMemberList import GenerateMembersFrame
from widget_classes.UpdateGBList import UpdateGBList


class MyTabView(customtkinter.CTkTabview):

    # def resource_path(relative_path):
    #     """ Get absolute path to resource, works for dev and for PyInstaller
    #     https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    #     """
    #     try:
    #         # PyInstaller creates a temp folder and stores path in _MEIPASS
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #         return os.path.join(base_path, relative_path)

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Generate Members")
        self.add("Update GB Members")
        self.add("Create Harvest Invoices  ")
        self.add("Compare Xero and CRM  ")

        self.generate_members_frame = GenerateMembersFrame(master=self.tab("Generate Members"), title="Options")
        self.generate_members_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.generate_members_frame = UpdateGBList(master=self.tab("Update GB Members"), title="Update GB Members")
        self.generate_members_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("STOSC")
        self.eval('tk::PlaceWindow . center')

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.mainloop()
