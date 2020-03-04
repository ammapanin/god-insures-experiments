#-*-encoding:utf-8-*-

import Tkinter as tk
import ghana_questionnaire as gq
import ghana_decisions as gd
import os
import tkFont
import tkMessageBox
import datetime
import csv
import codecs

reload(gq)
reload(gd)

#BASE = '/Users/aserwaahWZB/Desktop/ghana_experiment_121114/ghana_program'
BASE = os.path.join((os.path.dirname(__file__)))

def read_file(name):
    with open(name, "r") as myfile:
        file_text = myfile.read()
        return file_text

        texts = dict([(name, read_file(os.path.join(self.BASE,
                                                    "texts",
                                                    name + ".txt")))
                      for name in fnames])

def get_instructions():

    text_list = ("experiment_general",
                 "acknowledge_payment")

    fnames = [os.path.join(BASE, "texts", name + ".txt")
              for name in text_list]

    texts = dict([(name, read_file(os.path.join(BASE,
                                                "texts",
                                                name + ".txt")))
                  for name in text_list])

    return texts

class GhanaReligion():

    def __init__(self, master, instructions, treatments):

        self.master = master
        self.treatment_dic = treatments
        self.msg_dic = instructions


        self.debug = treatments["debug"]
        self.BASE = BASE
        self.start_screen = self.draw_start_screen(self.master)

    def draw_start_screen(self, master):

        headerfont = tkFont.Font(size = 25, weight = "bold")
        textfont = tkFont.Font(size = 20)
        buttonfont = tkFont.Font(size = 15)
        labelfont = tkFont.Font(size = 15, weight = "bold")

        mframe = tk.Frame(master)
        mframe.pack(fill = "both",
                    expand = True,
                    anchor = "center", padx = 10, pady = 10)

        okframe = tk.Frame(mframe)

        txt0 = tk.Label(mframe,
                        text = "Welcome to the study.",
                        font = headerfont)

        enumeratorpath = os.path.join(self.BASE,
                                      "texts",
                                      "enumerators.csv")

        with open(enumeratorpath, "rb") as myfile:
            enumcsv = csv.reader(myfile)
            enum_list = tuple(["-".join(row) for row in enumcsv])


        desk_list = tuple(["0" * (2 - len(str(i))) + str(i)
                           for i in range(1, 13)]) + ("AMMA", "TEST", "OTHER")
        session_list = ("015", "016", "017", "018", "019",
                        "020", "021", "022", "023", "024",
                        "025", "026", "027", "028", "029",
                        "030", "031", "032", "033", "034",
                        "035", "036", "037", "038", "039",
                        "040", "041", "042", "043", "044",
                        "045", "046", "047", "048", "049",
                        "050", "051", "052", "053", "054")

        treatment_list = ("Insurance",
                          "No insurance",
                          "Insurance information")
        population_list = ("Church", "Market")
        subgroup_list = ("AoG Exhibition",
                         "AoG Abundant Life",
                         "AoG House of Hope",
                         "AoG Redemption")

        enum_var = tk.StringVar(mframe)
        desk_var = tk.StringVar(mframe)
        session_var = tk.StringVar(mframe)
        treatment_var = tk.StringVar(mframe)
        population_var = tk.StringVar(mframe)
        subgroup_var = tk.StringVar(mframe)

        var_container = tk.Frame(mframe)

        varframes = [tk.Frame(var_container) for i in  (0,1)]
        [f.grid(row = 0, column = i)
         for i, f in enumerate(varframes)]

        texts = ("Enumerator",
                 "Desk",
                 "Session",
                 "Treatment",
                 "Population",
                 "Subgroup")

        var_labs = [tk.Label(varframes[0], text = txt, font = labelfont)
                    for txt in  texts]

        var_list = (enum_var,
                    desk_var,
                    session_var,
                    treatment_var,
                    population_var,
                    subgroup_var)

        text_lists = (enum_list,
                      desk_list,
                      session_list,
                      treatment_list,
                      population_list,
                      subgroup_list)


        entries = zip(var_list, text_lists)


        var_lists = [apply(tk.OptionMenu,
                           (varframes[1], var) + l)
                     for var, l in entries]

        [l.grid(row = i, column = 0, pady = 3, sticky = "w")
         for labs in (var_lists, var_labs)
         for i, l in enumerate(labs)]


        txt = tk.Label(mframe,
                       text = ("Please enter the following information "
                               "then press ENTER to continue"),
                       font = textfont,
                       justify = "left")

        next_bt = self.ok = tk.Button(mframe,
                                      text = "Begin study",
                                      command = self.start_to_instructions,
                                      font = buttonfont)

        def validate_entries(event):
            enum = enum_var.get() == ""
            desk = desk_var.get() == ""
            treatment = treatment_var.get() == ""
            session = session_var.get() == ""
            population = population_var.get() == ""
            subgroup = subgroup_var.get() == ""

            all_entries = enum + desk + treatment + session + population + subgroup == 0
            if all_entries == True or self.debug == True:
                next_bt.pack(side = "top",
                             anchor = "w",
                             pady = 15)

                self.treatment_dic.update({"desk": desk_var.get(),
                                           "enumerator": enum_var.get(),
                                           "session": session_var.get(),
                                           "treatment": treatment_var.get(),
                                           "population": population_var.get().lower(),
                                           "subgroup": subgroup_var.get()})
            elif enum == 1:
                tkMessageBox.showinfo("Missing information",
                                      "Please select an enumerator number")
            elif desk == 1:
                tkMessageBox.showinfo("Missing information",
                                      "Please select a desk number")

            elif session == 1:
                tkMessageBox.showinfo("Missing information",
                                      "Please select a session number")

            elif treatment == 1:
                tkMessageBox.showinfo("Missing information",
                                      "Please select a treatment")
            elif population == 1:
                tkMessageBox.showinfo("Missing information",
                                      "Please select a population")
            return None

        mframe.bind_all("<Return>",
                        validate_entries)

        txt0.pack(side = "top", anchor = "w", pady = 5, padx = 10)
        txt.pack(side = "top", anchor = "w", pady = 10, padx = 10)
        var_container.pack(side = "top", anchor = "w", padx = 10, pady = 10)

        return {"main_frame": mframe,
                "var_frame": var_container,
                "txt": txt,
                "header": txt0,
                "next_bt": next_bt}


    def start_to_instructions(self):
        #self.treatment_dic.update({"enumerator": },
        #)
        disappear_widgets = [self.start_screen.get(w)
                             for w in ("var_frame",)]
        [w.destroy() for w in disappear_widgets]

        frame = self.start_screen.get("main_frame")
        headingfont = tkFont.Font(size = 25, weight = "bold")
        generalfont = tkFont.Font(size = 18)

        full_instructions = self.msg_dic["experiment_general"]

        heading = self.start_screen.get("header")
        heading.config(text = "General instructions",
                       fg = "black")

        tlab = self.start_screen.get("txt")
        tlab.config(wraplength = 1000,
                    text = full_instructions,
                    font = generalfont)

        bt = self.start_screen.get("next_bt")
        bt.config(text = "Begin survey",
                  command = self.instructions_to_survey)


    def draw_survey_screen(self, master):
        self.survey_frame = tk.Frame(master)
        self.survey_frame.pack(fill = "both", expand = True)

        q_frame = tk.Frame(self.survey_frame)
        population = self.treatment_dic.get("population")

        #raw_questions = gq.setup_questionnaire(self.BASE, population)

        self.questionnaire = gq.Questionnaire(q_frame,
                                              self.BASE,
                                              self.treatment_dic,
                                              self.write_data)

        txt1font = tkFont.Font(size = 15, weight = "bold")

        txt1 = tk.Label(self.survey_frame,
                        text = ("All contents of this "
                        "survey are strictly confidential"),
                        font = txt1font)

        ok_bt = tk.Button(self.survey_frame,
                          text = "Complete survey")


        complete_frame = tk.Frame(self.survey_frame)
        complete_frame.pack(side = "bottom")


        def quick_complete(event):
            lab = tk.Label(complete_frame, text = "Quick complete password")
            entry = tk.Entry(complete_frame, show = "*")

            def go_quick_complete():
                passwd = entry.get()
                if passwd == "nudist colony":
                    ok_bt.pack(side = "bottom")
                else:
                    lab.config(text = "Please try again")
            bt = tk.Button(complete_frame, text = "OK", command = go_quick_complete)
            [w.pack(side = "left") for w in (lab, entry, bt)]



        self.survey_frame.bind_all("<Shift-Down>", quick_complete)

        ok_bt.bind("<Button-1>", (lambda event, cf = complete_frame,
                                  bt = ok_bt:self.draw_survey_payment(event, bt, cf)))

        if self.debug == True:
            ok_bt.pack(side = "bottom")
        elif self.debug == False:
            pass

        def complete_survey(name, index, mode):
            ok_bt.pack(side = "bottom")
            return None

        self.questionnaire.complete_var.trace("w", complete_survey)

        txt1.pack(side = "top")
        q_frame.pack(side = "top", expand = True, fill = "both" )



    def instructions_to_survey(self):
        self.start_screen["main_frame"].destroy()
        self.draw_survey_screen(self.master)


    def draw_survey_payment(self, event, bt, cf = None):
        bt.destroy()
        if cf:
            cf.destroy()

        frame = tk.Frame(self.master)
        frame.pack(pady = 80)

        sigframe = tk.Frame(frame)
        boldfont = tkFont.Font(size = 15, weight = "bold")
        lab = tk.Label(frame,
                       text = self.msg_dic["acknowledge_payment"],
                       font = boldfont,
                       justify = "left",
                       wraplength = 600,
                       bg = "grey")

        lab.pack()
        sigframe.pack()

        date_var = tk.StringVar()
        date = tk.Entry(sigframe, textvariable = date_var, state = "disabled")
        date.grid(row = 0, column = 1)

        date = tk.Button(sigframe,
                       command = lambda f = frame, b = date, v = date_var:\
                       self.get_paymentdate(f, date, date_var),
                       text = "Get date and time")
        date.grid(row = 0, column = 2)

    def get_paymentdate(self, frame, button, entry_var):
        button.configure(text = "Begin decision task",
                         command = lambda f = frame: self.draw_decisions(f))
        m = datetime.datetime.now()
        mstring = m.strftime("%d-%b-%Y %H:%M")
        entry_var.set(mstring)
        self.questionnaire.write_data()

    def draw_decisions(self, frame):
        frame.pack_forget()

        self.questionnaire.canvas.unbind("<Return>",
                                         self.questionnaire.enter_bind)
        denomination = self.treatment_dic.get("subgroup")

        self.survey_frame.pack_forget()
        self.decisions = gd.Decisions(self.master,
                                      BASE,
                                      self.treatment_dic,
                                      denomination,
                                      self.questionnaire.religion_var.get(),
                                      self.write_data)

    def write_data(self, mode, data):

        data_path = os.path.join(self.BASE,
                                 "data")

        #!!!!
        serverpath = os.path.join("INFO-02-2014-PC",
                                  "Users",
                                  "Public",
                                  "ghana_experiment_260215",
                                  "ghana_program")

        if os.path.exists(data_path) == False:
            os.makedirs(data_path)

        session = self.treatment_dic["session"]
        desk = self.treatment_dic["desk"]

        now = datetime.datetime.now().strftime("%d%m%H%M")

        filename = os.path.join(data_path,
                                "religion_{}_{}.csv".format(session, desk))

        if os.path.exists(filename) == True:
            filename = filename[:-4] + "_" + now + ".csv"

        def write_rows(fpath):
            with open(fpath, mode) as csvfile:
                datawriter = csv.writer(csvfile)
                [datawriter.writerow(d)
                 for d in data]
                datawriter.writerow(("time", now))
            return filename

        local = write_rows(filename)

        if os.path.exists(serverpath) == True:
            server = write_rows(serverpath)
        else:
            pass

def run_program(subgroup, debug):
    root = tk.Tk()

    instructions = get_instructions()
    root.tk_setPalette(background = "white")
    root.title("CUC/IAST/TSE Study. Accra, February 2015")
    root.attributes("-fullscreen", True)
    umlaut = GhanaReligion(root,
                           instructions,
                           {"subgroup": subgroup,
                            "debug": debug})

    print "cool running..."
    root.mainloop()
    return umlaut
