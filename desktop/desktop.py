import tkinter
from tkinter import messagebox
import customtkinter

import requests
import webbrowser
import os
from PIL import Image,ImageTk
import threading
import cv2

from localStoragePy import localStoragePy

localStorage = localStoragePy('AFMS', 'sqlite')


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
search_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "static/search.ico")), size=(26, 20))
logout_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "static/logout.png")), size=(26, 20))

availableQuota = 0

#utility functions
def callback(url):
    webbrowser.open_new(url)

def update_output():
    for i in range(10):
        txtProcessBox.insert("0.0",f"{i}")

def check_status(response,**kwargs):
    if response.status_code != 200:
        txtProcessBox.insert(tkinter.END,"Fetching vechiicle data...\n")
        txtProcessBox.configure(state="disabled")
    else:
        txtProcessBox.configure(state="normal")
        txtProcessBox.insert(tkinter.END,"vechicle data Fetched SuccessFully....\n")
        txtProcessBox.configure(state="disabled")

def login(username,password,window):
    r = requests.post('https://auto-fuel-management-system.herokuapp.com/api/token/', data={
        "username": str(username.get()),
        "password": str(password.get())
    })
    
    try :
        checkRequestSuccess = r.json()["refresh"]
        # f = open("token.txt", "w")
        # f.write(f"refresh: {r.json()['refresh']}\n")
        # f.write(f"access: {r.json()['access']}")
        # f.flush()
        localStorage.setItem("access",r.json()['access'])
        localStorage.setItem("refresh",r.json()['refresh'])
        window.destroy()
        mainWindow()
    except:
        print("login failed")
        print(r.json())
        messagebox.showerror("Login error", r.json()['detail'])

def logout():
    localStorage.setItem("access",None)
    localStorage.setItem("refresh",None)
    admin_window.destroy()
    loginWindow()

def getVechicleDetails():
    if txtVechicleNumberField.get() != "":
        vechicleNumber = txtVechicleNumberField.get().upper()
        r = requests.get(f'https://auto-fuel-management-system.herokuapp.com/api/getVechicle/{vechicleNumber}',hooks=dict(response=check_status))
        print(r.json())
        lblFullnameValue.configure(text=f"{r.json()['first_name']} {r.json()['last_name']}")
        lblMobileNumberValue.configure(text=f"{r.json()['phone_no']}")
        lblVechicleNumberValue.configure(text=f"{r.json()['vechicle_no']}")
        global vechicle_number
        vechicle_number = f"{r.json()['vechicle_no']}"
        lblVechicleTypeValue.configure(text=f"{r.json()['vechicle_type']['name']}")
        lblFuelTypeValue.configure(text=f"{r.json()['fuel_type']}")
        lbltotalQuotaValue.configure(text=f"{r.json()['vechicle_type']['quota_limit']}")
        global availableQuota
        availableQuota = r.json()['vechicle_type']['quota_limit']-r.json()['quota_used']
        lblAvailableQuotaslider.set((r.json()['vechicle_type']['quota_limit']-r.json()['quota_used'])/r.json()['vechicle_type']['quota_limit'])
        lblAvailableQuotaValue.configure(text=f"{r.json()['vechicle_type']['quota_limit']-r.json()['quota_used']}")
        lblLastFilledValue.configure(text=f"{r.json()['last_filled_at']}")
        if (r.json()['vechicle_type']['quota_limit']-r.json()['quota_used']) == 0:
            quotaUpdateSlider.configure(state="disabled")
            btnUpdate.configure(state="disabled")
        else:
            quotaUpdateSlider.configure(state="normal",from_=0, to=r.json()['vechicle_type']['quota_limit']-r.json()['quota_used'])
            btnUpdate.configure(state="normal")
        quotaUpdateSlider.set(0)

def updateSliderEvent(value):
    global updatefuelamount
    updatefuelamount = int(value)
    lblupdateAmount.configure(text=str(int(value)))

def updateFuel():
    r = requests.get(f'https://auto-fuel-management-system.herokuapp.com/api/updateQuota/{vechicle_number}/{updatefuelamount}')
    if r.json()['Message'] == " success":
        global availableQuota
        localavailablequota = availableQuota
        lblAvailableQuotaslider.set(localavailablequota-updatefuelamount)
        lblAvailableQuotaValue.configure(text=f"{localavailablequota-updatefuelamount}")
        print(localavailablequota)
        if localavailablequota == 1:
            quotaUpdateSlider.configure(state="disabled")
        else:
            quotaUpdateSlider.configure(from_=0, to=localavailablequota-updatefuelamount)
            quotaUpdateSlider.set(0)
        lblupdateAmount.configure(text="0")
        availableQuota = localavailablequota-updatefuelamount
        
def update_frame():
    # Read the next frame from the webcam
    _, frame = video_capture.read()

    # Convert the frame to a PhotoImage object
    frame = Image.fromarray(frame)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = ImageTk.PhotoImage(image=frame)

    # Update the label with the new image
    imagelabel.configure(image=image)
    imagelabel.image = image
    # imagelabel2.configure(image=image)
    # imagelabel2.image = image

    # Schedule the next frame update
    admin_window.after(15, update_frame())

root = customtkinter.CTk()

#windows
def mainWindow():
    # global video_capture
    # video_capture = cv2.VideoCapture(0)
    root.withdraw()
    global admin_window
    admin_window = customtkinter.CTkToplevel(root)
    admin_window.geometry("1100x700")
    admin_window.title("Automatic Fuel Management System")
    admin_window.resizable(0,0)

    frmLeftBar = customtkinter.CTkFrame(master=admin_window, width=400, height=700)
    frmLeftBar.grid(row=0, column=0, rowspan=4, sticky="nsew")
    frmLeftBar.grid_rowconfigure(4, weight=1)
    frmLeftBar.propagate(0)

    global txtVechicleNumberField
    txtVechicleNumberField = customtkinter.CTkEntry(master=frmLeftBar, placeholder_text="Enter Vechicle Number", height=40, width=300,)
    txtVechicleNumberField.place(x=20,y=20)

    btnSearch = customtkinter.CTkButton(master=frmLeftBar, text="", width=50, height=40, image=search_logo, command=getVechicleDetails)
    btnSearch.place(x=330, y=20)

    lblFullname = customtkinter.CTkLabel(master=frmLeftBar, text="Full Name: ", font=("Roboto", 15))
    lblFullname.place(y=100, x=20)
    global lblFullnameValue
    lblFullnameValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblFullnameValue.place(y=100, x=170)

    lblMobileNumber = customtkinter.CTkLabel(master=frmLeftBar, text="Mobile Number: ", font=("Roboto", 15))
    lblMobileNumber.place(y=130, x=20)
    global lblMobileNumberValue
    lblMobileNumberValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblMobileNumberValue.place(y=130, x=170)

    lblVechicleNumber = customtkinter.CTkLabel(master=frmLeftBar, text="Vechicle Number: ", font=("Roboto", 15))
    lblVechicleNumber.place(y=160, x=20)
    global lblVechicleNumberValue
    lblVechicleNumberValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblVechicleNumberValue.place(y=160, x=170)

    lblVechicleType = customtkinter.CTkLabel(master=frmLeftBar, text="Vechicle Type: ", font=("Roboto", 15))
    lblVechicleType.place(y=190, x=20)
    global lblVechicleTypeValue
    lblVechicleTypeValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblVechicleTypeValue.place(y=190, x=170)

    lblFuelType = customtkinter.CTkLabel(master=frmLeftBar, text="Fuel Type: ", font=("Roboto", 15))
    lblFuelType.place(y=220, x=20)
    global lblFuelTypeValue
    lblFuelTypeValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblFuelTypeValue.place(y=220, x=170)

    lbltotalQuota = customtkinter.CTkLabel(master=frmLeftBar, text="Quota Limit: ", font=("Roboto", 15))
    lbltotalQuota.place(y=250, x=20)
    global lbltotalQuotaValue
    lbltotalQuotaValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lbltotalQuotaValue.place(y=250, x=170)

    lblAvailableQuota = customtkinter.CTkLabel(master=frmLeftBar, text="Available Quota: ", font=("Roboto", 15))
    lblAvailableQuota.place(y=280, x=20)
    global lblAvailableQuotaslider
    lblAvailableQuotaslider = customtkinter.CTkProgressBar(master=frmLeftBar, width=180)
    lblAvailableQuotaslider.set(0)
    lblAvailableQuotaslider.place(y=290, x=170)
    global lblAvailableQuotaValue
    lblAvailableQuotaValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblAvailableQuotaValue.place(y=280, x=360)

    lblLastFilled = customtkinter.CTkLabel(master=frmLeftBar, text="Last Filled at: ", font=("Roboto", 15))
    lblLastFilled.place(y=310, x=20)
    global lblLastFilledValue
    lblLastFilledValue = customtkinter.CTkLabel(master=frmLeftBar, text="", font=("Roboto", 15))
    lblLastFilledValue.place(y=310, x=170)

    lblUpdate = customtkinter.CTkLabel(master=frmLeftBar, text="Update Quota", font=("Roboto", 18))
    lblUpdate.place(y=400, x=20)

    global quotaUpdateSlider
    quotaUpdateSlider = customtkinter.CTkSlider(master=frmLeftBar, width=350, state="disabled", command=updateSliderEvent)
    quotaUpdateSlider.place(y=450, x=20)

    global lblupdateAmount
    lblupdateAmount = customtkinter.CTkLabel(master=frmLeftBar, text="0", font=("Roboto",20))
    lblupdateAmount.pack(pady=(480,0))

    global btnUpdate
    btnUpdate = customtkinter.CTkButton(master=frmLeftBar, width=350, height=40, text="Update Quota",state="disabled", command=updateFuel)
    btnUpdate.place(y=530, x=25)

    btnLogout = customtkinter.CTkButton(master=frmLeftBar, text="Logout", width=100, height=40, image=logout_logo, command=logout)
    btnLogout.place(x=20, y=640)

    frmCam1 = customtkinter.CTkFrame(master=admin_window, width=280, height=280)
    frmCam1.propagate(0)
    frmCam1.place(x=450, y=100)

    global imagelabel
    imagelabel = customtkinter.CTkLabel(master=frmCam1)
    imagelabel.pack()

    frmCam2 = customtkinter.CTkFrame(master=admin_window, width=280, height=280)
    frmCam2.propagate(0)
    frmCam2.place(x=770, y=100)

    global imagelabel2
    imagelabel2 = customtkinter.CTkLabel(master=frmCam2)
    imagelabel2.pack()

    # video_thread = threading.Thread(target=update_frame)

    # video_thread.start()


    global txtProcessBox
    txtProcessBox = customtkinter.CTkTextbox(master=admin_window, width=600, height=100)
    txtProcessBox.place(x=450,y= 550)

    admin_window.deiconify()

def loginWindow():
    root.withdraw()
    login_window = customtkinter.CTkToplevel(root)
    login_window.geometry("1100x700")
    login_window.title("Automatic Fuel Management System")

    frmLogin = customtkinter.CTkFrame(master=login_window, width=400, height=400)
    frmLogin.propagate(0)
    frmLogin.pack(pady=150)

    lblSignin = customtkinter.CTkLabel(master=frmLogin, text="Login System", font=("Roboto", 24))
    lblSignin.pack(pady=(35,12))

    txtUsername = customtkinter.CTkEntry(master=frmLogin, placeholder_text="Username", width=300, height=40)
    txtUsername.pack(pady=(50,12))

    txtPassword = customtkinter.CTkEntry(master=frmLogin, placeholder_text="Password", show="*", width=300, height=40)
    txtPassword.pack(pady=12)

    btnSignin = customtkinter.CTkButton(master=frmLogin, text="Login", width=300, height=40)
    btnSignin.pack(pady=12)
    btnSignin.bind('<Button-1>', lambda e:login(txtUsername,txtPassword,login_window))

    lblSignup = customtkinter.CTkLabel(master=frmLogin, text="Don't have an account? Signup.")
    lblSignup.pack(pady=12)
    lblSignup.bind("<Button-1>",lambda e:callback("https://auto-fuel-management-system.herokuapp.com/fuelStationSignup/"))


    login_window.deiconify()
    

def main():

    if localStorage.getItem("access") != "None":
        r = requests.post('https://auto-fuel-management-system.herokuapp.com/api/token/refresh/', data={
                "refresh": localStorage.getItem("refresh"),
            })

        try:
            checkRequestSuccess = r.json()["refresh"]
            localStorage.setItem("access",r.json()['access'])
            localStorage.setItem("refresh",r.json()['refresh'])
            mainWindow()
        except:
            localStorage.setItem("access",None)
            localStorage.setItem("refresh",None)
            loginWindow()
    else:
        loginWindow()


main()

root.mainloop()
