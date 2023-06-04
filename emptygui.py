import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

import svglib.svglib as svglib

from enum import Enum
import re
from PIL import Image, ImageDraw

import customtkinter
import pandas
import pandastable as pt
from nltk.tree import *
from customtkinter import CTk
from PIL import ImageTk, Image

from Main import find_token, Tokens, errors, Parse

global ImageCounter
ImageCounter = 0


def select_frame_by_name(name):
    # set button color for selected button
    root.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    root.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

    # show selected frame
    if name == "home":
        root.home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        root.home_frame.grid_forget()
    if name == "frame_2":
        root.DFAFrame.grid(row=0, column=1, sticky="nsew")
    else:
        root.DFAFrame.grid_forget()
def home_button_event():
    select_frame_by_name("home")


def frame_2_button_event():
    select_frame_by_name("frame_2")


def frame_3_button_event():
    select_frame_by_name("table")


def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)

def Scan(self):  # Scan Button Functionality
    x1 = root.home_frame_TextBox.get('1.0', END)
    x1 = x1.lower()

    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()


root = customtkinter.CTk()

root.title("LISP Compiler")
root.geometry("1600x900")

# set grid layout 1x2
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
svg_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DFAsSVG")
root.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                         size=(26, 26))
root.titleText = customtkinter.CTkLabel(master=root, text="LISP Compiler")
root.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                               size=(20, 20))
root.scanner_image = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(image_path, "scannerlight.png")),
    dark_image=Image.open(os.path.join(image_path, "scannerdark.png")), size=(20, 20))
root.DFA_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "transitionLight.png")),
                                        dark_image=Image.open(os.path.join(image_path, "transitionDark.png")),
                                        size=(20, 20))

# create navigation frame
root.navigation_frame = customtkinter.CTkFrame(master=root, corner_radius=0)
root.navigation_frame.grid(row=0, column=0, sticky="nsew")
root.navigation_frame.grid_rowconfigure(4, weight=1)

root.navigation_frame_label = customtkinter.CTkLabel(root.navigation_frame, text="  LISP Compiler",
                                                     image=root.logo_image,
                                                     compound="left",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
root.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

root.home_button = customtkinter.CTkButton(root.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                           text="Compiler",
                                           fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"),
                                           image=root.scanner_image, anchor="w", command=lambda:home_button_event())
root.home_button.grid(row=1, column=0, sticky="ew")

root.frame_2_button = customtkinter.CTkButton(root.navigation_frame, corner_radius=0, height=40,
                                              border_spacing=10, text=" DFA Visualization ",
                                              fg_color="transparent", text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"),
                                              image=root.DFA_image, anchor="w",
                                              command=lambda:frame_2_button_event())
root.frame_2_button.grid(row=2, column=0, sticky="ew")

root.appearance_mode_menu = customtkinter.CTkOptionMenu(root.navigation_frame,
                                                        values=["Light", "Dark", "System"],
                                                        command=lambda:change_appearance_mode_event())
root.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

# create home frame
root.home_frame = customtkinter.CTkFrame(master=root,corner_radius=0, fg_color="transparent")
root.home_frame.grid_columnconfigure(0, weight=1)

root.home_frame_title = customtkinter.CTkLabel(root.home_frame, text="LISP Compiler",
                                               font=('Rockwell', 45))

root.home_frame_title.grid(row=0, column=0, padx=20, pady=10)

root.ScanButton = customtkinter.CTkButton(root.home_frame, text="Scan Only", font=('Arial Bold', 15),
                                          command=Scan, width=170, height=60)
root.ScanButton.grid(row=2, column=0, padx=20, pady=10)

root.ScanAndParseButton = customtkinter.CTkButton(root.home_frame, text="Scan & Parse", font=('Arial Bold', 15),
                                                  command=Scan, width=170, height=60)
root.ScanAndParseButton.grid(row=3, column=0, padx=20, pady=10)

root.home_frame_TextBox = customtkinter.CTkTextbox(root.home_frame, width=1000, height=400, font=('', 25))
root.home_frame_TextBox.grid(row=1, column=0, padx=60, pady=10)

# create second frame
root.DFAFrame = customtkinter.CTkFrame(master=root,corner_radius=0, fg_color="transparent")
root.DFAFrame.grid_columnconfigure(0, weight=1)

# select default frame
select_frame_by_name("home")

# DFA Visualization
DFA_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Test-DFAs")

root.commentsDFA = customtkinter.CTkImage(light_image=Image.open(os.path.join(DFA_path, "commentsDFA.png")),
                                          dark_image=Image.open(os.path.join(DFA_path, "commentsDFA.png")),
                                          size=(368, 165))

root.identifiersDFA = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(DFA_path, "identifiersDFA.png")),
    dark_image=Image.open(os.path.join(DFA_path, "identifiersDFA.png")),
    size=(768, 254))

root.numbersDFA = customtkinter.CTkImage(light_image=Image.open(os.path.join(DFA_path, "numbersDFA.png")),
                                         dark_image=Image.open(os.path.join(DFA_path, "numbersDFA.png")),
                                         size=(618, 413))

root.relationalOperatorsDFA = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(DFA_path, "relationalOperatorsDFA.png")),
    dark_image=Image.open(os.path.join(DFA_path, "relationalOperatorsDFA.png")),
    size=(768, 475))

root.semiStandardCharacters = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(DFA_path, "semiStandardCharactersDFA.png")),
    dark_image=Image.open(os.path.join(DFA_path, "semiStandardCharactersDFA.png")),
    size=(768, 250))

root.stringsDFA = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(DFA_path, "stringsDFA.png")),
    dark_image=Image.open(os.path.join(DFA_path, "stringsDFA.png")),
    size=(595, 367))

root.arithmeticOperatorsDFA = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(DFA_path, "arithmeticOperatorsDFA.png")),
    dark_image=Image.open(os.path.join(DFA_path, "arithmeticOperatorsDFA.png")),
    size=(595, 367))

DFA_List = [root.identifiersDFA, root.stringsDFA, root.numbersDFA, root.commentsDFA,
            root.semiStandardCharacters, root.arithmeticOperatorsDFA, root.relationalOperatorsDFA]

DFA_List_svg = ["identifiersDFA.svg", "stringsDFA.svg", "numbersDFA.svg", "commentsDFA.svg",
                "semiStandardCharactersDFA.svg",
                " arithmeticOperatorsDFA.svg", "relationalOperatorsDFA.svg"]
DFA_NamesList = ["DFA For Identifiers", "DFA For Strings", "DFA For Numbers", "DFA For Comments",
                 "DFA For semiStandardCharacters", "DFA For Arithmetic Operators", "DFA Relational Operators"]

root.DFAFrame_imageViewer = customtkinter.CTkLabel(root.DFAFrame, text="", image=root.identifiersDFA, )
root.DFAFrame_imageViewer.grid(row=0, column=0, padx=150, pady=20)

# DFA Image Label
root.DFAFrame_imageLabel = customtkinter.CTkLabel(root.DFAFrame, text=DFA_NamesList[0], font=('Rockwell', 25))
root.DFAFrame_imageLabel.grid(row=5, column=0, padx=20, pady=20)
# DFA Image Buttons
root.DFAFrame_nextButton = customtkinter.CTkButton(root.DFAFrame, text="-->",
                                                   font=('Arial Bold', 15),
                                                   command=lambda: on_next(DFA_List, DFA_NamesList),
                                                   width=170, height=60)
root.DFAFrame_previousButton = customtkinter.CTkButton(root.DFAFrame, text="<--",
                                                       font=('Arial Bold', 15),
                                                       command=lambda: on_back(DFA_List, DFA_NamesList),
                                                       width=170, height=60)

root.DFAFrame_nextButton.grid(row=2, column=0, padx=20, pady=20)
root.DFAFrame_previousButton.grid(row=3, column=0, padx=20, pady=10)
# DFA Image Buttons

root.DFAFrame_openSVGButton = customtkinter.CTkButton(root.DFAFrame, text="Open SVG",
                                                      font=('Arial Bold', 15),
                                                      command=lambda: open_svg(DFA_List_svg),
                                                      width=170, height=60)
root.DFAFrame_openSVGButton.grid(row=4, column=0, padx=20, pady=20)

root.DFAFrame_openSVGHint = customtkinter.CTkLabel(root.DFAFrame, text="Click on the Open SVG for a higher "
                                                                       "quality and ability to zoom ",
                                                   font=('Times', 20), text_color=("#37529c", "#CF6679"))
root.DFAFrame_openSVGHint.grid(row=6, column=0, padx=20, pady=1)


def on_next(DFA_List, DFA_NamesList):
    global ImageCounter
    if ImageCounter + 1 < len(DFA_List):
        root.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter + 1])
        root.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter + 1])
        ImageCounter = ImageCounter + 1
    else:
        ImageCounter = 0
        root.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter])
        root.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter])


def on_back(DFA_List, DFA_NamesList):
    global ImageCounter
    if ImageCounter - 1 >= 0:
        root.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter - 1])
        root.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter - 1])
        ImageCounter = ImageCounter - 1
    else:
        ImageCounter = len(DFA_List) - 1
        root.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter])
        root.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter])


def open_svg(DFA_List_svg):
    global ImageCounter
    os.system(DFA_List_svg[ImageCounter])



root.mainloop()






