import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from enum import Enum
import re
from PIL import Image

import customtkinter
import pandas
import pandastable as pt
from nltk.tree import *
from customtkinter import CTk

from Main import find_token, Tokens, Parse, errors

global ImageCounter
ImageCounter = 0


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("LISP Compiler")
        self.geometry("1600x900")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        svg_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DFAsSVG")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))
        self.titleText = customtkinter.CTkLabel(master=self, text="LISP Compiler")
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.scanner_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "scannerlight.png")),
            dark_image=Image.open(os.path.join(image_path, "scannerdark.png")), size=(20, 20))
        self.DFA_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "transitionLight.png")),
                                                dark_image=Image.open(os.path.join(image_path, "transitionDark.png")),
                                                size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  LISP Compiler",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Compiler",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.scanner_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text=" DFA Visualization ",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.DFA_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_title = customtkinter.CTkLabel(self.home_frame, text="LISP Compiler",
                                                       font=('Rockwell', 45))

        self.home_frame_title.grid(row=0, column=0, padx=20, pady=10)

        self.ScanButton = customtkinter.CTkButton(self.home_frame, text="Scan & Parse", font=('Arial Bold', 15),
                                                  command=self.Scan, width=170, height=60)
        self.ScanButton.grid(row=2, column=0, padx=20, pady=10)

        # self.ScanAndParseButton = customtkinter.CTkButton(self.home_frame, text="Clear All", font=('Arial Bold', 15),
        #                                                   command=self.clear(dTDa1, dTDa2), width=170, height=60)
        # self.ScanAndParseButton.grid(row=3, column=0, padx=20, pady=10)

        self.home_frame_TextBox = customtkinter.CTkTextbox(self.home_frame, width=1000, height=400, font=('', 25))
        self.home_frame_TextBox.grid(row=1, column=0, padx=60, pady=10)

        # create second frame
        self.DFAFrame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.DFAFrame.grid_columnconfigure(0, weight=1)

        # select default frame
        self.select_frame_by_name("home")

        # DFA Visualization
        DFA_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Test-DFAs")

        self.commentsDFA = customtkinter.CTkImage(light_image=Image.open(os.path.join(DFA_path, "commentsDFA.png")),
                                                  dark_image=Image.open(os.path.join(DFA_path, "commentsDFA.png")),
                                                  size=(368, 165))

        self.identifiersDFA = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(DFA_path, "identifiersDFA.png")),
            dark_image=Image.open(os.path.join(DFA_path, "identifiersDFA.png")),
            size=(768, 254))

        self.numbersDFA = customtkinter.CTkImage(light_image=Image.open(os.path.join(DFA_path, "numbersDFA.png")),
                                                 dark_image=Image.open(os.path.join(DFA_path, "numbersDFA.png")),
                                                 size=(618, 413))

        self.relationalOperatorsDFA = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(DFA_path, "relationalOperatorsDFA.png")),
            dark_image=Image.open(os.path.join(DFA_path, "relationalOperatorsDFA.png")),
            size=(768, 475))

        self.semiStandardCharacters = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(DFA_path, "semiStandardCharactersDFA.png")),
            dark_image=Image.open(os.path.join(DFA_path, "semiStandardCharactersDFA.png")),
            size=(768, 250))

        self.stringsDFA = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(DFA_path, "stringsDFA.png")),
            dark_image=Image.open(os.path.join(DFA_path, "stringsDFA.png")),
            size=(595, 367))

        self.arithmeticOperatorsDFA = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(DFA_path, "arithmeticOperatorsDFA.png")),
            dark_image=Image.open(os.path.join(DFA_path, "arithmeticOperatorsDFA.png")),
            size=(595, 367))

        self.charactersDFA = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(DFA_path, "charactersDFA.png")),
            dark_image=Image.open(os.path.join(DFA_path, "charactersDFA.png")),
            size=(768, 314))

        DFA_List = [self.identifiersDFA, self.stringsDFA, self.numbersDFA, self.commentsDFA,
                    self.semiStandardCharacters, self.arithmeticOperatorsDFA, self.relationalOperatorsDFA,self.charactersDFA]

        DFA_List_svg = ["identifiersDFA.svg", "stringsDFA.svg", "numbersDFA.svg", "commentsDFA.svg",
                        "semiStandardCharactersDFA.svg",
                        " arithmeticOperatorsDFA.svg", "relationalOperatorsDFA.svg","charactersDFA.svg"]
        DFA_NamesList = ["DFA For Identifiers", "DFA For Strings", "DFA For Numbers", "DFA For Comments",
                         "DFA For semiStandardCharacters", "DFA For Arithmetic Operators", "DFA Relational Operators","DFA For Characters"]

        self.DFAFrame_imageViewer = customtkinter.CTkLabel(self.DFAFrame, text="", image=self.identifiersDFA, )
        self.DFAFrame_imageViewer.grid(row=0, column=0, padx=150, pady=20)

        # DFA Image Label
        self.DFAFrame_imageLabel = customtkinter.CTkLabel(self.DFAFrame, text=DFA_NamesList[0], font=('Rockwell', 25))
        self.DFAFrame_imageLabel.grid(row=5, column=0, padx=20, pady=20)
        # DFA Image Buttons
        self.DFAFrame_nextButton = customtkinter.CTkButton(self.DFAFrame, text="-->",
                                                           font=('Arial Bold', 15),
                                                           command=lambda: self.on_next(DFA_List, DFA_NamesList),
                                                           width=170, height=60)
        self.DFAFrame_previousButton = customtkinter.CTkButton(self.DFAFrame, text="<--",
                                                               font=('Arial Bold', 15),
                                                               command=lambda: self.on_back(DFA_List, DFA_NamesList),
                                                               width=170, height=60)

        self.DFAFrame_nextButton.grid(row=2, column=0, padx=20, pady=20)
        self.DFAFrame_previousButton.grid(row=3, column=0, padx=20, pady=10)
        # DFA Image Buttons

        self.DFAFrame_openSVGButton = customtkinter.CTkButton(self.DFAFrame, text="Open SVG",
                                                              font=('Arial Bold', 15),
                                                              command=lambda: self.open_svg(DFA_List_svg),
                                                              width=170, height=60)
        self.DFAFrame_openSVGButton.grid(row=4, column=0, padx=20, pady=20)

        self.DFAFrame_openSVGHint = customtkinter.CTkLabel(self.DFAFrame, text="Click on the Open SVG for a higher "
                                                                               "quality and ability to zoom ",
                                                           font=('Times', 20), text_color=("#37529c", "#CF6679"))
        self.DFAFrame_openSVGHint.grid(row=6, column=0, padx=20, pady=1)

    def on_next(self, DFA_List, DFA_NamesList):
        global ImageCounter
        if ImageCounter + 1 < len(DFA_List):
            self.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter + 1])
            self.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter + 1])
            ImageCounter = ImageCounter + 1
        else:
            ImageCounter = 0
            self.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter])
            self.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter])

    def on_back(self, DFA_List, DFA_NamesList):
        global ImageCounter
        if ImageCounter - 1 >= 0:
            self.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter - 1])
            self.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter - 1])
            ImageCounter = ImageCounter - 1
        else:
            ImageCounter = len(DFA_List) - 1
            self.DFAFrame_imageViewer.configure(image=DFA_List[ImageCounter])
            self.DFAFrame_imageLabel.configure(text=DFA_NamesList[ImageCounter])

    def open_svg(self, DFA_List_svg):
        global ImageCounter
        os.system(DFA_List_svg[ImageCounter])

    def Scan(self):  # Scan Button Functionality
        x1 = self.home_frame_TextBox.get('1.0', END)
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

    def clear_table(self,df):
        df.drop(df.index,inplace=True)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.DFAFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.DFAFrame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("table")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()

    app.mainloop()
