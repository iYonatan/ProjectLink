from tkinter import *
import tkinter.messagebox as tm


class LoginFrame(Frame):
    def __init__(self, method_name, master, **kw):
        Frame.__init__(self, master, **kw)

        self.master.title("Project Link")
        self.master.minsize(350, 150)
        self.master.resizable(0, 0)
        self.master.iconbitmap(
            default='C:\Users\Yonatan\PycharmProjects\ProjectLink\Documents\Other\projectlink_sm_icon.ico')

        self.method_name = method_name

        self.username_input = Entry(self)
        self.pwd_input = Entry(self, show="*")

        self.label_1 = Label(self, text="Username: ")
        self.label_2 = Label(self, text="Password: ")

        self.label_1.grid(row=50)
        self.label_2.grid(row=51)

        self.username_input.grid(row=50, column=1)
        self.pwd_input.grid(row=51, column=1)

        self.logbtn = Button(self, text="Login", command=lambda: self.method_name(self))
        self.logbtn.grid(columnspan=2)

        self.pack()

    def failed_login(self):
        tm.showerror("Login error", "Incorrect username or password")

    def success_login(self):
        tm.showinfo("Login info", "Welcome to Project Link!")

    def _login_btn_clickked(self):
        # print("Clicked")
        username = self.username_input.get()
        password = self.pwd_input.get()

        # print(username, password)

        if username == "john" and password == "password":
            tm.showinfo("Login info", "Welcome John")
        else:
            tm.showerror("Login error", "Incorrect username")


class GUI:
    def __init__(self, ):
        self.method_name = None
        self.lf = None

    def run(self, method_name):
        self.method_name = method_name
        root = Tk()
        self.lf = LoginFrame(self.method_name, root)
        root.mainloop()

# def test(gui):
#     print gui.username_input.get()
#     print gui.pwd_input.get()
#
#     gui.destroy()
#     gui.quit()
#     print "DEAD"
#     return
#
#
# g = GUI()
# g.run(test)
