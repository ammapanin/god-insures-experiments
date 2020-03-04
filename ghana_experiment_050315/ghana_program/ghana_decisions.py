import Tkinter as tk
import tkFont
import random
import csv
import tkMessageBox
import datetime
import os
from collections import namedtuple
import string
import itertools
import pickle
import sys
import time
from note_pile import NotePile

fullpack = {"expand":True,
            "fill": "both"}

class Decisions():
    def __init__(self, master,
                 base_path,
                 treatments, denomination, religion, data_function):

        self.master = master

        self.mainframe = tk.Frame(self.master)
        self.mainframe.pack(side = "bottom", **fullpack)

        self.denomination = denomination
        self.payment_experiment_dics = dict()

        self.BASE = base_path
        self.pie = 11
        self.religion = religion
        self.treatment_dic = treatments
        self.global_write_data = data_function

        self.instructions_dic = self.get_decision_instructions()

        self.experiment_types = ("practice", "real_stakes")
        self.practice_var = tk.StringVar(self.mainframe)
        self.practice_var.set("practice")

        self.choice_idx_var = tk.IntVar(self.mainframe)

        self.unlock_pay_frame = tk.Frame(self.mainframe)
        self.draw_unlock_payment(self.unlock_pay_frame)

        self.name_var = tk.StringVar(self.master)


        self.choice_sets = [self.get_choice_sets(experiment)
                            for experiment in self.experiment_types]
        self.draw_instructions(self.mainframe)


    def get_decision_instructions(self):
        base_names = ("decision_general",
                      "public",
                      "thanksgiving",
                      "street")

        population = self.treatment_dic.get("population")
        
        if population:
            fnames = base_names + (population, population + "_named")
        else:
            pass
            #fnames = base_names + ("church", "church_named")
        fpaths = [os.path.join(self.BASE, "texts", name + ".txt")
                  for name in fnames]

        def read_file(name):
            with open(name, "r") as myfile:
                file_text = myfile.read()
            return file_text

        texts = dict([(name, read_file(os.path.join(self.BASE,
                                                    "texts",
                                                    name + ".txt")))
                      for name in fnames])

        return(texts)


    def draw_instructions(self, master):
        frame = tk.Frame(master)

        choicefont = tkFont.Font(size = 15)
        titlefont = tkFont.Font(size = 15, weight = "bold")
        bigtitlefont = tkFont.Font(size = 18, weight = "bold")

        title = tk.Label(frame,
                         font = bigtitlefont,
                         text = "Instructions for the decision task")

        general = self.instructions_dic["decision_general"].format(self.n_options,
                                                          self.n_options)

        instructions = tk.Label(frame,
                                wraplength = 1000,
                                text = general,
                                justify = "left")
        description_frame = tk.Frame(frame)

        [w.pack(anchor = "w", pady = 5)
          for w in (frame, title, instructions, description_frame)]

        basic_choice_tags  = ("thanksgiving", "street")

        population = self.treatment_dic.get("population")
        if population == "church":
            choice_tags = basic_choice_tags + ("church", "church_named")
        elif population == "market":
            choice_tags = basic_choice_tags + ("market", "market_named")


        titles = {"thanksgiving": "National thanksgiving offering",
                  "street": "Street Children's Empowerment Fund",
                  "church":"Anonymous church offering",
                  "church_named":"Named church offering",
                  "market":"Anonymous market offering",
                  "market_named":"Named market offering"}


        choices = [self.instructions_dic.get(choice) for choice in
                   choice_tags]

        [self.make_option_instruction(frame,
                                      titlefont,
                                      titles[choice],
                                      self.instructions_dic.get(choice))
         for choice in choice_tags]

        bt = tk.Button(frame,
                       text = "Answer first question",
                       command = lambda f = frame:
                       self.show_choice_screen(f))

        bt.pack(side = "bottom")
        return None

    def make_option_instruction(self, master, titlefont, title_in, text_in):

        self.name_var = tk.StringVar(master)


        title = tk.Label(master,
                         wraplength = 1000,
                         text = title_in,
                         font = titlefont,
                         justify = "left")

        description = tk.Label(master,
                               wraplength = 1000,
                               text = text_in,
                               justify = "left")

        title.pack(anchor = "w", side = "top")
        description.pack(anchor = "w",
                         pady = 8,
                         side = "top")

        if title_in[0:5].upper() == "NAMED":
            entryframe = tk.Frame(master)
            entry = tk.Entry(entryframe, textvariable = self.name_var)
            lab = tk.Label(entryframe,
                           text = ("Please enter your name."
                                   " This will only be used if you end up giving"
                                   " money to the church with your name."))

            entryframe.pack(side = "top", anchor = "w")
            [w.pack(side = "left", anchor = "w") for w in (entry, lab)]


        return None

    def show_choice_screen(self, frame_in):
        self.setup_choice_screen(self.mainframe)
        #self.setup_choice_screen(self.mainframe)
        frame_in.pack_forget()
        frame = self.decision_frames["main"]
        frame.pack(expand = True, fill = "both")

    def restart_experiment(self):
        tkMessageBox.showinfo("Real money at stake!",
                              ("That was the practice session."
                               "\nYou will now start a section of the experiment"
                               " where one of your decisions will determine"
                               " your real final payout. Please pay close attention "
                               "to the choices you make."))

        shortinstructions = ("Please choose how you would most"
                             " prefer to allocate 11GHS.")

        realmoney = ("Please note, one of your choices "
                     "will now be played for real money")


        self.space_id = self.master.bind("<space>", self.go_next)

        lab0, lab1, lab2 = [self.text_labels.get(lab)
                            for lab in ("lab0", "lab1", "lab2")]

        lab0.config(text = shortinstructions)
        lab1.config(text = realmoney)
        lab2.pack_forget()

        next_bts = [self.buttons.get(b)
                    for b in ("next", "back")]

        [bt.config(text = t, command = f, state = "active")
         for bt, t, f in zip(next_bts,
                             ("Back", "Next"),
                             (lambda e = "event": self.show_previous(e),
                              lambda e = "event": self.go_next(e)))]

        [bt.pack(side = "left") for bt in next_bts]
        bt_frame = self.buttons.get("frame")

        choice_frame = self.decision_frames.get("choice_frame")

        payment_frame = self.decision_frames.get("payment_frame")
        pay_frame = self.decision_frames.get("payframe")
        show_frame = self.decision_frames.get("show_frame")

        [f.pack_forget()
         for f in (choice_frame, payment_frame, bt_frame)]

        [f.pack(side = "top")
         for f in (lab0, lab1, choice_frame, bt_frame)]

        [f.pack_forget()
         for f in (pay_frame, show_frame)]

        choice_frame.config(bd = 0)

        self.experiment_dic = self.experiment["real_stakes"]
        self.practice_var.set("real_stakes")
        experiment = self.practice_var.get()

        self.choice_idx_var.set(0)

        scales = [choice.get("scale")
                  for choice in self.experiment_dic.values()]

        [scale.config(state = "active")
         for scale in scales]

        self.enum_helpbox.pack(side = "bottom", anchor = "w", pady = 3)

        idx_list = self.experiment[experiment].values()
        choice_frames = [v.get("frame") for v in idx_list]

        [f.pack_forget() for f in choice_frames]
        self.pay_lab.config(text = ("Please wait for an enumerator "
                                    "to authorise your payment information"))
        roundtext = "This is the {} round".format(experiment)
        self.experiment_pay_lab.config(text = roundtext)

        self.pay_entry.config(state = "normal")
        self.pay_entry.pack(side = "top")
        [e.delete(0, "end") for e in (self.random_entry, )]
        self.pay_button.config(state = "disabled")


    def setup_choice_screen(self, master):
        frame = tk.Frame(master)

        textfont = tkFont.Font(size = 15, weight = "bold")
        mainfont = tkFont.Font(size = 18, weight = "bold")


        shortinstructions = ("For each of the following options,"
                             " please choose how you would most"
                             " prefer to allocate 11GHS.")

        practicepay =  ("In this practice round, none of the "
                        "answers will be played out for real money.")

        practicetext = "This is a practice round"


        labels = [(shortinstructions, "black", mainfont),
                  (practicepay, "black", textfont),
                  (practicetext, "orange", textfont)]

        labwidgets = [tk.Label(frame,
                               wraplength = 600,
                               text = t,
                               fg = col,
                               font = f)
                      for t, col, f in labels]

        [l.pack(side = "top", pady = 20)
         for l in labwidgets[:2]]

        choice_frame, \
        buttons_frame, \
        payment_frame = [tk.Frame(frame)
                          for i in range(0,3)]

        paytext_frame, \
        showtext_frame  = [tk.Frame(payment_frame)
                           for i in range(0,2)]

        labnames = ["lab{}".format(i)
                    for i, k in enumerate(labwidgets)]
        labwidgets[2].pack(side = "bottom", pady = 20)

        [f.pack(side = "top",
                padx = 5)
         for f in (choice_frame, payment_frame, buttons_frame)]



        pay, show = self.draw_payment_labels(paytext_frame,
                                             showtext_frame,
                                             textfont)

        button_info = zip(("Back", "Next"),
                          (lambda e = "event": self.show_previous(e),
                           lambda e = "event": self.go_next(e)))

        next_bt, back_bt = [tk.Button(buttons_frame,
                                      text = txt,
                                      command = func)
                            for txt, func in button_info]
        [bt.pack(side = "left")
         for bt in (next_bt, back_bt)]

        self.text_labels = dict(zip(labnames, labwidgets))
        self.text_labels.update(pay)
        self.text_labels.update(show)

        self.buttons = {"next": next_bt,
                        "back": back_bt,
                        "frame": buttons_frame}

        self.decision_frames = {"payment_frame": payment_frame,
                                "choice_frame": choice_frame,
                                "payframe": paytext_frame,
                                "show_frame": showtext_frame,
                                "main": frame}

        self.make_choice_labels(choice_frame)
        self.experiment_dic = self.experiment["practice"]
        return None


    def draw_payment_labels(self, payframe, showframe, textfont):
        payhighlightfont = tkFont.Font(size = 15,
                                       family = "courier",
                                       weight = "bold")

        choicehighlightfont = tkFont.Font(size = 18,
                                          family = "courier",
                                          weight = "bold")

        showtextfont = tkFont.Font(size = 12,
                                   slant = "italic")


        payframes = [tk.Frame(payframe) for i in range(0, 6)]
        [frame.pack(side = "top", anchor = "w") for frame in payframes]

        p1 = [tk.Label(payframes[0], font = textfont) for i in range(0, 4)]
        p2 = [tk.Label(payframes[1], font = textfont) for i in range(0, 6)]
        p3 = [tk.Label(payframes[2], font = textfont) for i in range(0, 3)]
        p4 = [tk.Label(payframes[j], font = textfont)
              for j in range(3, 6) for i in (0, 2)]

        paylabs = p1 + p2 + p3 + p4

        public_i = 3
        pay_dic = {"random_choice": p1,
                   "individual_choice": p2,
                   "public_contribution": p3,
                   "public_pot": p4[0:2],
                   "public_individual": p4[2:4]}

        showlabs = [tk.Label(showframe, font = textfont)
                    for i in range(0, 13)]

        show_amts = showlabs[1:7]
        show_text = showlabs[7:13]


        royal_blue = (pay_dic["individual_choice"][2],
                      pay_dic["individual_choice"][5],
                      pay_dic["random_choice"][1],
                      pay_dic["random_choice"][3])

        blue_four = (pay_dic["individual_choice"][1],
                     pay_dic["individual_choice"][4])

        dark_green =  (pay_dic["public_contribution"][1],
                       pay_dic["public_pot"][1],
                       pay_dic["public_individual"][1])

        [lab.config(fg = "RoyalBlue1",
                    font = payhighlightfont)
         for lab in royal_blue]

        [lab.config(fg = "Blue4",
                     font = choicehighlightfont)
        for lab in blue_four]

        [lab.config(fg = "Dark green",
                    font = payhighlightfont)
         for lab in dark_green]

        [lab.pack(side = "left", pady = 2) for lab in paylabs]
        [l.config(font = showtextfont) for l in show_text]

        showlabs[0].grid(row = 0, column = 0)
        [lab.grid(row = i, column = 1, sticky = "e")
         for i, lab in enumerate(show_amts)]
        [lab.grid(row = i, column = 2, sticky = "w", padx = 20)
         for i, lab in enumerate(show_text)]


        ShowTup = namedtuple("Show", "amount text")
        showlab_pairs = [ShowTup(*i) for i in zip(show_amts, show_text)]

        shownames = ("survey",
                     "additional",
                     "option1",
                     "option2",
                     "public_payout",
                     "total")

        show_dic = dict(zip(shownames, showlab_pairs))
        show_dic.update({"show_text": showlabs[0]})

        return pay_dic, show_dic

    def get_choice_sets(self, experiment):
        if self.religion == "muslim":
            thanksgiving_image = "prayer_muslim{}.gif"
        else:
            thanksgiving_image = "prayer_christian{}.gif"

        ChoiceOption = namedtuple("Choice",
                                  "lab text short past logo_name named")
        all_options_dic = dict()

        options_path = os.path.join(self.BASE, "texts", "options.csv")

        with open(options_path, "rb") as optfile:
            optscsv = [r for r in csv.reader(optfile)]
            names = optscsv[0]
            for row in optscsv:
                choice = {row[0]: ChoiceOption(*row)}
                all_options_dic.update(choice)


        basic_opts = ("thanksgiving", "keep", "street")

        population = self.treatment_dic.get("population")

        if population == "church":
            opts = basic_opts + ("church", "church_named")
        elif population == "market":
            opts = basic_opts + ("market", "market_named")

        options_dic = dict([(i, all_options_dic.get(i)) for i in opts])

        church_market = self.treatment_dic.get("population")

        if experiment == "practice":
            choice_filename = "choice_pairs_practice.csv"
        elif experiment == "real_stakes":
            choice_filename = "choice_pairs.csv"

        choice_path = os.path.join(self.BASE,
                                   "texts",
                                   choice_filename)


        with open(choice_path, "rb") as choicefile:
            choicecsv = csv.reader(choicefile)
            choice_labs = list()
            for row in choicecsv:
                pair_labs = [pair.format(church_market) for pair in row[0:2]]
                choice_labs.append(pair_labs)

            choices = list()

            for pair in choice_labs:
                choice_pair = [options_dic.get(lab) for lab in pair]
                choices.append(choice_pair)

        choice_pairs = enumerate(choices)

        ChoiceTuple = namedtuple("ChoiceLab", "tag colour choice_pair")
        letters = string.ascii_uppercase
        colours = ("dark green",
                   "saddle brown",
                   "yellow",
                   "firebrick",
                   "midnight blue",
                   "violet red",
                   "antique white",
                   "blue violet",
                   "goldenrod",
                   "lawn green")

        choices = [ChoiceTuple(letters[i], colours[i], choice)
                   for i, choice in choice_pairs]

        if experiment == "practice":
            self.n_practice = len(choices)
        elif experiment == "real_stakes":
            self.n_options = len(choices)


        random.shuffle(choices)

        with open("labelled_choices.csv", "wb") as myfile:
            c = csv.writer(myfile)
            for choice in choices:
                info = [choice.tag] +\
                       [cp.lab for cp in choice.choice_pair]
                
                c.writerow(info)

        past_tense_dic = dict([(c.tag, [cp.past for cp in c.choice_pair])
                                     for c in choices])

        public_tags_dic = dict(filter(None,
                                  [self.get_public_tags(cp)
                                   for cp in choices]))
        named_tags_list = filter(None,
                                 [self.get_named_tags(cp)
                                  for cp in choices])

        keep_tags_dic = dict(filter(None,
                                    [self.get_keep_tags(cp)
                                     for cp in choices]))

        tagged_choice_dic = dict([(c.tag,
                                        {"choices": [cp.short
                                                     for cp in c.choice_pair],
                                         "idx": i})
                                       for i, c in enumerate(choices, 1)])


        dics = {experiment: {"past_tense": past_tense_dic,
                             "named_tags": named_tags_list,
                              "public_tags": public_tags_dic,
                              "keep_tags": keep_tags_dic,
                              "tagged_choice_dic": tagged_choice_dic}}
        self.payment_experiment_dics.update(dics)
        return choices

    def make_choice_labels(self, master):
        dics = [dict([(idx,
                       self.draw_individual_choice(idx,
                                                   choice,
                                                   master))
                      for idx, choice in enumerate(choice_set, 1)])
                for choice_set in  self.choice_sets]


        self.experiment = dict(zip(self.experiment_types, dics))
        return None

    def get_named_tags(self, choice_pair):
        choices = [p.text for p in choice_pair.choice_pair]

        tag = [choice_pair.tag
               for i, choice in enumerate(choices) if "name" in choice]
        if tag:
            return tag[0]
        else:
            return None

    def get_public_tags(self, choice_pair):
        choices = [p.text for p in choice_pair.choice_pair]

        tag = [(choice_pair.tag, i)
               for i, choice in enumerate(choices) if "public" in choice]
        if tag:
            return tag[0]
        else:
            return None

    def get_keep_tags(self, choice_pair):
        choices = [p.text for p in choice_pair.choice_pair]

        tag = [(choice_pair.tag, i)
               for i, choice in enumerate(choices) if "Keep" in choice]

        if tag:
            return tag[0]
        else:
            return None

    def draw_individual_choice(self, idx, choice_obj, master):

        colour = choice_obj.colour

        frame = tk.LabelFrame(master, highlightthickness = 3,
                              highlightcolor = colour)
        labelfontsize = 18

        idxfont = tkFont.Font(name = "idxfont",
                              size = 25,
                              weight = "bold")
        amtfont = tkFont.Font(size = labelfontsize,
                              family = "courier",
                              weight = "bold")
        decisionfont = tkFont.Font(name = "decisionfont",
                                   size = labelfontsize)

        choice = choice_obj.choice_pair

        check_var, lvar, rvar = [tk.StringVar(frame)
                                            for i in range(0, 3)]

        scale_var = tk.IntVar(frame)

        if self.treatment_dic["population"] == "market":
            subgroup = "your market line"

        else:
            subgroup = self.treatment_dic.get("subgroup")

        if subgroup == None:
            subgroup = "your church"

        if self.treatment_dic["population"] == "church":
            texts = [c.text.format(money = {},
                                   denomination = subgroup)
                     for c in choice]

        if self.treatment_dic["population"] == "market":
            texts = [c.text.format(money = {},
                                   unit_line = subgroup)
                     for c in choice]



        id_lab = tk.Label(frame,
                          text = "Q{}. ".format(idx),
                          font = idxfont,
                          name = "id_lab")

        choice_frames = [tk.Frame(frame,
                                  name = "pic_frame_{}".format(i))
                         for i in (0, 1)]

        lab_frames = [tk.Frame(cframe, name = "label_frame")
                      for cframe in choice_frames]

        [lab.grid(row  = 0, column = 0)
         for i, lab in zip((1, 3), lab_frames)]


        notes = [NotePile(self.BASE, f, grid_row = 1, grid_col = 0)
                for f in choice_frames]

        env_configs = zip(choice, choice_frames)
        envelopes = [ChoiceEnvelope(f, 2, 0,
                                    self.BASE,
                                    self.name_var,
                                    choice = c.logo_name,
                                    named = c.named)
                     for c, f in env_configs]


        split_texts = [t.split("GHS{}") for t in texts]
        [t.insert(1, "") for t in split_texts]

        left_text, right_text = [[tk.Label(f, text = t,
                                           font = decisionfont,
                                           name = "lab_{}".format(i))
                                  for i, t in enumerate(text)]
                                  for text, f in zip(split_texts,
                                                     lab_frames)]

        text_labs = (left_text, right_text)

        amts = [text[1] for text in text_labs]
        amt_col =  "dark blue"
        [amt.config(fg = amt_col,
                   font = amtfont) for amt in amts]

        [l.pack(side = "left")
         for l in itertools.chain(*text_labs)]


        def buttons_plus(event):
            amt_0 = scale.get()
            if amt_0 < self.pie:
                amt_1 = amt_0 + 1
                scale.set(amt_1)
            else:
                pass

        def buttons_minus(event):
            amt_0 = scale.get()
            if amt_0 > 0:
                amt_1 = amt_0 - 1
                scale.set(amt_1)
            else:
                pass

        choice_dic = {"scale_n": 0}
        scale_n = tk.IntVar(master)
        scale_n.set(-1)

        def scale_move(name, index, mode):
            i = scale_n.get()
            i += 1
            scale_n.set(i)
            choice_dic["scale_n"] = i
            return None

        def scale_to_amounts(event):
            right = scale.get()
            left = self.pie - right

            l = left_text[1]
            r = right_text[1]

            amt = "GHS{}"

            [note.get_positions(nr)
             for note, nr in zip(notes, (left, right))]

            [lab.config(text = amt.format(side))
             for lab, side in zip((l,r), (left, right))]
            scale_move("name", "index", "mode")

        def buttons_to_amounts(name, index, mode):
            scale_to_amounts("event")
            return None

        scale = tk.Scale(frame,
                         from_ = 0,
                         to = self.pie,
                         variable = scale_var,
                         orient = "horizontal",
                         showvalue = False,
                         sliderlength = 30,
                         length = 400,
                         command = scale_to_amounts)

        scale_start = random.choice(range(0, self.pie))
        scale.set(scale_start)
        scale_var.trace("w", buttons_to_amounts)
        scale.focus()

        keys = ("<Left>", "<Right>", "<space>")
        functions = (buttons_minus, buttons_plus, self.go_next)

        ids = [self.master.bind(key, func)
               for key, func in zip(keys, functions)]
        self.space_id = ids[2]

        id_lab.grid(row = 0, column = 0)

        [f.grid(row = 0, column = i, sticky = "w", pady = 10)
         for f, i in zip(choice_frames, (1, 3))]

        scale.grid(row = 0, column = 2)

        [frame.grid_columnconfigure(index = i,
                                    minsize = 350,
                                    weight = 1)
          for i in (1, 3)]

        choice_dic.update({"scale_start": scale_start,
                           "frame": frame,
                           "idx_lab": id_lab,
                           "scale": scale,
                           "pics": envelopes,
                           "tag": choice_obj.tag})

        return choice_dic

    def decision_bindings_off(self):


        keys = ("<Left>", "<Right>", "<space>")
        [self.master.unbind_all(key) for key in keys]

    def make_add_amount_bts(self, master, bfuncs):
        buttonfont = tkFont.Font(size = 14, weight = "bold")
        bts = [tk.Button(master,
                         text = t,
                         font = buttonfont,
                         command = bfunc)
               for t, bfunc in zip(("+", "-"), bfuncs)]

        [bt.pack(side = "left",
                 padx = 2) for bt in bts]

        return None



    def draw_unlock_payment(self, master):
        textfont = tkFont.Font(size = 15, weight = "bold")
        roundfont = tkFont.Font(weight = "bold")
        pay_text = ("Please wait for an enumerator "
                    "to authorise your payment information")

        self.password_frame = tk.Frame(master)

        lab = self.pay_lab = tk.Label(master,
                                      text = pay_text,
                                      font = textfont)

        password_lab = tk.Label(self.password_frame, text = "Password")
        entry = self.pay_entry = tk.Entry(self.password_frame,
                                          show = "*")

        self.random_frame = tk.Frame(master)
        self.random_letter = tk.StringVar()

        roundtext = "This is the {} round".format(self.practice_var.get())
        self.experiment_pay_lab = tk.Label(master,
                                           text = roundtext,
                                           font = roundfont)
        random_lab = tk.Label(self.random_frame,
                              text = "Random letter")
        random_entry = tk.Entry(self.random_frame,
                                textvariable = self.random_letter)
        self.random_entry = random_entry

        [w.pack(side = "left") for w in random_lab, random_entry,
         password_lab, entry]


        button = self.pay_button = tk.Button(master,
                                             text = "Show payment information",
                                             command =  self.start_payment,
                                             state = "disabled")

        entry.bind("<Return>",
                   (lambda event, e = entry, b = button, l = lab, e2 = random_entry:
                    self.unlock_payment_screen(event, e, b, l, e2)))

        enum_text = "Did an enumerator help to answer these questions?"
        self.enum_helpvar = tk.IntVar(master)
        self.enum_helpbox = tk.Checkbutton(master,
                                           text = enum_text,
                                           variable = self.enum_helpvar)

        widgets = (lab,
                   self.experiment_pay_lab,
                   self.random_frame,
                   self.password_frame)

        [w.pack(side = "top", anchor = "w", pady = 3) for w in widgets]
        button.pack(side = "bottom", anchor = "w")


    def go_next(self, event):

        idx = min(self.n_options, self.choice_idx_var.get())

        choice_check = self.experiment_dic.get(idx)

        sure_text = ("You have not moved the slider."
                     " Are you sure of this decision?")

        if choice_check:
            answer = choice_check.get('scale_n')

            if answer == 0:
                choice_check['scale_n'] += 1
            elif answer != "":
                #go_next when an answer has been given
                frame = choice_check.get("frame")
                frame.grid_forget()

                self.show_next(idx)
        else:
            #go_next with no answer
            self.show_next(idx)

    def show_previous(self, event):
        idx0 = max(2, self.choice_idx_var.get())
        idx1 = idx0 - 1

        frame0, frame1 = [self.experiment_dic.get(idx).get("frame")
                          for idx in (idx0, idx1)]

        frame0.grid_forget()
        frame1.grid()

        self.choice_idx_var.set(idx1)
        return None

    def show_next(self, idx):
        idx1 = idx + 1

        experiment = self.practice_var.get()

        n_dic = {"real_stakes": self.n_options,
                 "practice": self.n_practice}

        n_max = n_dic.get(experiment)

        if idx1 < n_max + 1:
            self.choice_idx_var.set(idx1)
            choice_objs = self.experiment_dic.get(idx1)
            try:
                frame = choice_objs.get("frame")
                frame.grid()

                scale = choice_objs.get("scale")
                scale.focus_set()
            except:
                pass
        else:
            self.end_choices()
        return None


    def end_choices(self):
        experiment = self.practice_var.get()
        d = self.payment_experiment_dics.get(experiment)

        self.past_tense_dic, \
            self.named_tags_list,\
            self.public_tags_dic,\
            self.keep_tags_dic,\
            self.tagged_choice_dic = [d.get(i)  for i in ("past_tense",
                                                          "named_tags",
                                                          "public_tags",
                                                          "keep_tags",
                                                          "tagged_choice_dic")]


        self.decision_bindings_off()
        self.master.unbind("<space>", self.space_id)

        next_bt, back_bt = [self.buttons.get(b) for b in ("next", "back")]
        back_bt.pack_forget()

        self.enumerator_unlock_payment()

        #tkMessageBox.showinfo("Confirmation", confirm_text)


        # frames = [choice.get("frame")
        #           for choice in self.experiment_dic.values()]

        # id_labs = [f.children.get("id_lab") for f in frames]
        # [l.grid(row = 0, column = 0) for l in id_labs]

        # envelopes = [f.children.get(frame).children.get("envelope")
        #              for frame in ("pic_frame_0", "pic_frame_1")
        #              for f in frames]

        # notes = [f.children.get(frame).children.get("note_stack")
        #          for frame in ("pic_frame_0", "pic_frame_1")
        #          for f in frames]

        # endfont = tkFont.Font(size = 12)

        # label_frames = [f.children.get(frame).children.get("label_frame")
        #                for frame in ("pic_frame_0", "pic_frame_1")
        #                for f in frames]

        # label_dics = [label_frame.children
        #               for label_frame in label_frames]
        # keys = [key for key in label_dics[0].keys() if key[0:3] == "lab"]

        # labels = [d.get(k) for k in keys for d in label_dics]
        # [l.config(font = endfont) for l in labels + id_labs]


        # [widget.grid_forget() for widget in envelopes + notes]

        # [frame.pack(pady = 1, padx = 5) for frame in frames]
        # [frame.config(bd = 0, highlightcolour = None) for frame in frames]


        # next_bt.config(text = "Confirm choices",
        #                command = self.enumerator_unlock_payment)



    def enumerator_unlock_payment(self):
        self.decision_frames.get("main").pack_forget()
        self.unlock_pay_frame.pack(pady = 20)

        self.master.bind_all("<Shift-Left>", 
                             self.back_to_decisions)


    def back_to_decisions(self, event):
        self.decision_frames.get("main").pack()
        self.unlock_pay_frame.pack_forget()

        self.space_id = self.master.bind("<space>", self.go_next) 

        next_bt, back_bt = [self.buttons.get(b) for b in ("next", "back")]
        [bt.pack(side = "left") 
         for bt in next_bt, back_bt]

        
    def unlock_payment_screen(self, event, entry, button, label, entry2):
        p = entry.get()
        tag  = self.random_letter.get().strip().upper()

        [e.delete(0, "end") for e in (entry, )]

        if self.practice_var.get() == "real_stakes":
            password = "nudistcolony"
        else:
            password = "jollofrice"



        if tag in [i for i in string.ascii_uppercase[0:self.n_options]]:
            go = True
        else:
            go = False
            label.config(text = ("Please enter a valid letter:",
                                 "A, B, C, D, E, F, G, H, I , J"))
        if p == "":
            label.config(text = "Please enter password")
        elif p != "":
            if go == True:
                if p == password:
                    label.config(text = "Getting payment information...")
                    entry.pack_forget()
                    button.config(state = "active")

                else:
                    label.config(text = "Please enter password again")
            elif go == False:
                pass

        return None

    def write_public_payment(self, tag):
        idx = self.tagged_choice_dic.get(tag).get("idx")
        desk = self.treatment_dic["desk"]

        i = self.public_tags_dic.get(tag)

        scale_amt = self.experiment_dic.get(idx).get("scale").get()

        if i == 0:
            choice_amt = self.pie - scale_amt
        elif i == 1:
            choice_amt = scale_amt

        public_choice = (desk,
                         choice_amt)

        public_path = os.path.join(self.BASE,
                                   "public",
                                   "choices_{}".format(tag))

        if os.path.exists(public_path) == False:
            os.makedirs(public_path)

        fpath = os.path.join(public_path,
                             "desk_{}.csv".format(desk))

        with open(fpath, "wb") as myfile:
            p = csv.writer(myfile)
            p.writerow(public_choice)

        return None

    def get_random_answer(self):
        tag = self.random_letter.get().strip().upper()



        choices = self.tagged_choice_dic.get(tag)

        idx = int(choices.get("idx"))
        choice = choices.get("choices")


        return tag, idx, choice

    def get_public_payout(self, tag):

        public_path = os.path.join(self.BASE,
                                   "public",
                                   "choices_{}".format(tag))


        public_choices = [os.path.join(public_path, fname)
                          for fname in os.listdir(public_path)
                          if fname[-3:] == "csv"]
        self.n_players = len(public_choices)

        public_dict = dict([self.read_public_file(f)
                            for f in public_choices])

        pot = [int(i) for i in public_dict.values() if int(i) > 0]

        public_amt = sum(pot)
        return public_amt

    def read_public_file(self, fname):
        bool_dic = {"True": True,
                    "False": False}

        with open(fname, "rb") as myfile:
            public = list(csv.reader(myfile))[0]

        return tuple(public)

    def start_payment(self):
        self.write_data()


        #self.pay_button.config(state = "disabled")

        self.unlock_pay_frame.pack_forget()
        self.decision_frames.get("main").pack()

        #CAUTION!!!
        cdic = self.experiment_dic

        lab0, lab1, lab2 = [self.text_labels.get(lab)
                            for lab in ("lab0", "lab1", "lab2")]

        lab0.config(text = "You made the following choices")

        cframe = self.decision_frames.get("choice_frame")
        cframe.config(bd = 1, relief = "solid")
        cframe.pack_forget()


        [lab.pack_forget() for lab in (lab1,)]


        payment_frame = self.decision_frames.get("payment_frame")
        button_frame = self.buttons.get("frame")
        #button_frame.pack(side = "bottom")


        [f.pack_forget()
         for f in (button_frame,)]

        [f.pack(side = "top")
         for f in (payment_frame, button_frame)]

        paynames = ("payframe", )
        payframes = [self.decision_frames.get(f)
                     for f in paynames]

        [f.pack(side = "top", pady = 10, fill = "y")
         for f in payframes]


        self.show_payment()


    def show_payment(self):
        cdic = self.experiment_dic

        tag, idx, choices = self.get_random_answer()
        past_choices = self.past_tense_dic.get(tag)

        public_question = tag in self.public_tags_dic.keys()
        keep_question = tag in self.keep_tags_dic.keys()

        amt = cdic.get(idx)["scale"].get()
        amts  = (self.pie - amt, amt)
        print_amts = [0, 0]

        randomfile = os.path.join(self.BASE,
                                  "payment",
                                  "random_selections.csv")

        if self.practice_var.get() == "real_stakes":
            with open(randomfile, "ab") as myfile:
                pay_data = (self.treatment_dic.get("desk"),
                            self.treatment_dic.get("session")) +\
                    (tag,) + tuple(choices) + tuple(amts)
                if tag in self.named_tags_list:
                    pay_data = pay_data + (self.name_var.get(),)

                payment = csv.writer(myfile)
                payment.writerow(pay_data)

        # dic_opts = dict([(value, key)
        #                  for key, value in self.opts_dic.items()])

        if public_question == True:
            public_pot = self.get_public_payout(tag)
            public_value = public_pot * 1.5
            public_amt = round(float(public_value) / self.n_players, 2)
            public_tuple = (public_pot, public_value, public_amt)
        elif public_question == False:
            public_amt = 0
            public_tuple = None

        if keep_question == True:
            keep_n = self.keep_tags_dic[tag]
            kept_amt = amts[keep_n]
            print_amts[keep_n] = "+" + str(amts[keep_n])
            print_amts[abs(keep_n-1)] = "- " + str(amts[abs(keep_n - 1)])
        elif keep_question == False:
            kept_amt =  0
            print_amts = tuple(["- " + str(a) + "GHS" for a in amts])

        choice_texts = zip(print_amts, past_choices)
        total = 20 + kept_amt + public_amt


        scales = [choice.get("scale")
                  for choice in self.experiment_dic.values()]

        [scale.config(state = "disabled")
         for scale in scales]


        frame = cdic.get(idx)["frame"]
        frame.config(highlightthickness = 3,
                     highlightbackground = "blue")

        self.payment_narrative(choices, amts, public_tuple)

        button = self.buttons.get("next")
        button.config(text = "OK",
                      command = (lambda x = idx:
                                 self.show_payment_details(x, "event",
                                                           choice_texts,
                                                           public_question,
                                                           public_amt,
                                                           total)))
        self.master.bind("<space>",
                         lambda x = idx: self.show_payment_details("event", x,
                                                                   choice_texts,
                                                                   public_question,
                                                                   public_amt,
                                                                   total))



        return None

    def show_payment_details(self, event, random_idx,
                             choice_texts, public_question, public_amt, total):

        disappear_frames = [choice.get("frame")
                            for idx, choice in self.experiment_dic.items()
                            if idx != random_idx]

        [f.pack_forget() for f in disappear_frames]

        self.payment_details(choice_texts,
                             public_question,
                             public_amt,
                             total)
        self.complete_experiment_buttons()


    def complete_experiment_buttons(self):
        button = self.buttons.get("next")
        if self.practice_var.get() == "practice":
            button.config(text = "Proceed to main experiment",
                          command = self.restart_experiment)

        if self.practice_var.get() == "real_stakes":
            button.config(text = "End experiment",
                          command = self.complete_experiment)

    def config_payment_narratives_labs(self, lab_name, texts):
        labs = self.text_labels[lab_name]
        [lab.config(text = t)
         for lab, t in zip(labs, texts)]
        return None


    def details_lab(self, lab_name, texts):
        lab = self.text_labels[lab_name]

        lab.amount.config(text = texts[0])
        lab.text.config(text = texts[1])
        return None

    def payment_details(self,
                        choice_texts, public_played, public_payout, total):

        show_frame = self.decision_frames.get("show_frame")
        show_frame.pack(side = "bottom")

        labs = self.text_labels

        labs["show_text"].config(text = ("Your final payment information "
                                         "is as follows:"))

        survey_texts = ("+ 20 GHS", "for completing the survey")
        additional_texts = ("+ 11 GHS", "additional payment")
        total_texts = ("{}GHS".format(total), "TOTAL")


        lab_names = ("survey", "additional", "total")
        lab_texts = (survey_texts,
                     additional_texts,
                     total_texts)

        [self.details_lab(lab_name, lab_text)
         for lab_name, lab_text in zip(lab_names, lab_texts)]

        [self.details_lab(opt_lab, text) for
         opt_lab, text in zip(("option1", "option2"), choice_texts)]

        self.write_payment(total)
        return None

    def write_payment(self, total):
        desk = self.treatment_dic["desk"]

        payments_path = os.path.join(self.BASE,
                                     "payment",
                                     "payment_csv")

        if os.path.exists(payments_path) == False:
            os.makedirs(payments_path)

        fpath = os.path.join(payments_path,
                             "pay_{}.csv".format(desk))

        with open(fpath, "wb") as payfile:
            pay = csv.writer(payfile)
            pay.writerow([desk, total])

    def payment_narrative(self, choices, amts, public):

        random =  ("The choice to be played is between",
                   "{}".format(choices[0]),
                   "and",
                   "{}".format(choices[1]))

        individual = ("You chose to give",
                      "{} GHS".format(amts[0]),
                      " to {}".format(choices[0]),
                      "and",
                      "{} GHS".format(amts[1]),
                      " to {}".format(choices[1]))

        self.config_payment_narratives_labs("random_choice", random)
        self.config_payment_narratives_labs("individual_choice", individual)

        if public:
            public_pot, public_value, public_amt = public

            public_texts = (("In total, ",
                             "{} GHS".format(public_pot),
                             "were contributed to the public pot"),
                            ("This means the total value of the pot is ",
                             "{}GHS".format(public_value)),
                            ("Each person will receive ",
                             "{}GHS".format(public_amt)))

            names = ["public_{}".format(i)
                     for i in ("contribution", "pot", "individual")]

            [self.config_payment_narratives_labs(lab_name, texts)
             for lab_name, texts in zip(names, public_texts)]

        return None

    def get_choices(self):
        choice_dics = self.experiment_dic.values()

        decisions = [("choice_{}".format(v["tag"]),
                      v["scale"].get()) for v in choice_dics]

        starts = [("start_{}".format(v["tag"]),
                   v.get("scale_start")) for v in choice_dics]

        nmoves = [("nmove_{}".format(v["tag"]),
                   v.get("scale_n")) for v in choice_dics]

        enum_help = [("enum_help", self.enum_helpvar.get())]
        return decisions + starts + nmoves + enum_help


    def write_data(self):
        decisions = self.get_choices()
        filename = self.global_write_data("ab", decisions)
        print "Choice data appended to {}".format(filename)


    def complete_experiment(self):
        self.mainframe.forget()

        thanks = tk.Label(self.master,
                          font = tkFont.Font(size = 15, weight = "bold"),
                          text = ("Thank you for your time.\n"
                                  "Now please take your number "
                                  "and wait quietly at your desk until you are "
                                  "called for payment."),
                          justify = "left")

        thanks.pack(pady = 20)

        print "Monkeys and elephants"



class ChoiceEnvelope:

    def __init__(self, master, grid_row, grid_col, BASE, name_var, choice, named):
        self.pic = tk.Canvas(master,
                             height = 250,
                             width = 270,
                             name = "envelope")
        self.pic.grid(row = grid_row, column = grid_col, sticky = "n")

        self.BASE = BASE
        multiplier = 2.5

        self.start_x = 5
        self.start_y = 100

        self.x = 100 * multiplier
        self.y = 50 * multiplier

        self.mx = float(self.x) / 2
        self.my = float(self.y) / 2


        self.pic.create_line(self.mx, 0,
                             self.mx, self.start_y - 2,
                             arrow = "last",
                             width = 2)
        self.draw_envelope()
        self.draw_logo(self.pic, choice)

        if int(named) == True:
            self.create_name(name_var.get())

    def draw_envelope(self):

        n1 = (self.start_x, self.start_y)
        n2 = (self.start_x + self.x, self.start_y)
        n3 = (self.start_x, self.start_y + self.y)
        n4 = (self.start_x + self.x,  self.start_y + self.y)
        n5 = (self.start_x + self.mx, self.start_y + self.my)

        flap = (n1 + n5, n5 + n2)

        corners = (n1 + n2, n1 + n3, n2 + n4, n3 + n4)

        [self.pic.create_line(c) for c in corners + flap]

        return None

    def draw_logo(self, master, name_in):

        if name_in != "":

            logo_path = os.path.join(self.BASE, "images", name_in + ".gif")
            logo = tk.PhotoImage(file = logo_path)

            logo_label = tk.Label(master, image = logo)
            logo_label.pack(side = "left")
            logo_label.image = logo

            logo_frame = self.pic.create_window(self.start_x + 10,
                                                self.start_y + 35,
                                                window = logo_label,
                                                anchor = "nw")
        else:
            pass

        return

    def create_name(self, name):
        namefont = tkFont.Font(size = 14, underline = 1)
        name_x = self.mx + 20
        name_y = self.start_y + self.my + 25
        self.pic.create_text(name_x, name_y,
                             text = name,
                             font = namefont)
        return None





def test_decisions():
    try:
        root.destroy()
    except:
        pass

    def write_data(mode, data):

        data_path = os.path.join(BASE,
                                 "data")

        if os.path.exists(data_path) == False:
            os.makedirs(data_path)

        session = "TEST"
        desk = "TEST"

        filename = os.path.join(data_path,
                                "religion_{}_{}.csv".format(session, desk))

        with open(filename, mode) as csvfile:
            datawriter = csv.writer(csvfile)

            [datawriter.writerow(d)
             for d in data]

        return filename

    BASE = '/Users/aserwaahWZB/Desktop/ghana_experiment_210215/ghana_program'
    #BASE = os.path.join((os.path.dirname(__file__)))

    treatment_dic = {"session": 0,
                     "desk": 155,
                     "population": "church",
                     "public": True,
                     "insurance": "credit"}

    #instructions = get_instructions()

    root = tk.Tk()


    textfont = tkFont.Font(size = 15, weight = "bold")
    nghi = Decisions(root, BASE, treatment_dic, "Nudist", "muslim", write_data)
    root.attributes("-fullscreen", True)
    #root.mainloop()
    return nghi


# keep versus give to church provately
#emil = test_decisions()
