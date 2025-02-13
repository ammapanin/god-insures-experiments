import Tkinter as tk
import tkFont
import csv
import tkMessageBox
import itertools
import os
import datetime
from collections import namedtuple

#BASE = '/Users/aserwaahWZB/Desktop/ghana_experiment_210215/ghana_program'

class Questionnaire():

    def __init__(self, master, BASE, treatments, data_function):
        self.master = master
        self.treatment_dic = treatments
        self.BASE = BASE
        self.global_write_data = data_function

        population = (treatments.get("population"),)
        self.questions = self.setup_questionnaire(BASE, population)
        self.qformats_dic = self.setup_formats()

        self.top_frame = tk.Frame(master)
        self.top_frame.pack(side = "top")

        titlefont = tkFont.Font(size = 28, weight = 'bold')
        self.title = tk.Label(self.top_frame,
                              text = "Questionnaire",
                              font = titlefont)
        self.title.grid(columnspan = 2, sticky = 'w')
        self.title.pack(side = "left")

        self.progress = tk.Canvas(self.top_frame, width = 800, height = 50)
        self.progress.pack(side = "left")
        self.bar_increment = 8

        x0 = 20
        y0 = 20
        x1 = 20 + self.bar_increment * len(self.questions)
        y1 = 30
        xn = x0
        self.progress_coords = (x0, y0, x1, y1, xn)
        self.progress.create_rectangle(x0, y0 , x1, y1, fill = "green")
        self.progress.create_rectangle(x0, y0 , xn, y1, fill = "blue")

        self.canvas = tk.Canvas(master,
                                highlightthickness = 0)
        self.frame = tk.Frame(self.canvas)

        self.vsb = tk.Scrollbar(master,
                                command = self.canvas.yview)

        self.canvas.configure(yscrollcommand = self.vsb.set)

        self.vsb.pack(side = "right", fill = "y")

        self.canvas.pack(side = "left", fill = "both", expand = True)

        self.canvas.create_window((4,4),
                                  window = self.frame,
                                  anchor = "nw",
                                  tags = "self.frame")

        self.frame.bind("<Configure>",
                        self.OnFrameConfigure)



        self.answered_questions = [1]
        self.latest_frame_var = tk.IntVar(master)
        self.latest_frame_var.set(1)

        self.active_frame_var = tk.IntVar(master)
        self.active_frame_var.set(1)

        self.n_skip = tk.IntVar(master)

        self.setup_dictionaries_and_controls()

        self.question_idx = tk.IntVar(master)
        self.question_idx.set(1)

        self.religion_var = tk.StringVar(master)
        self.complete_var = tk.BooleanVar()
        self.complete_var.set(False)

        self.next_disabled = False

        self.enter_bind = self.canvas.bind_all("<Return>", self.go_next)

        self.highlight_next_question(1, 1)


    def check_population(self, population, desired_populations):
        if population == "all":
            return True
        elif population in desired_populations:
            return True
        else:
            return False

    def get_questions(self, line, desired):
        population = line[6]
        yes_pop = self.check_population(population, desired)

        if yes_pop:
            qlab, qdic = self.process_options(line)
        else:
            qlab, qdic = None, None
        return qlab, qdic


    def process_options(self, line):
        rows = ("question",
                "format",
                "options",
                "label",
                "other",
                "extra_options",
                "population")

        qrows = dict([(r, i)
                      for i, r in enumerate(rows)])

        qformat = line[qrows.get("format")]
        raw_options = line[qrows.get("options")]
        extra_options = line[qrows.get("extra_options")]
        qlab = line[qrows.get("label")]

        if qformat == "text":
            options = ""

        elif qformat != "text":
            options = raw_options.split(",x")
            try:
                options = [int(i) for i in options]
            except ValueError:
                pass

            if qformat == "list":
                try:
                    list_options = range(*options)
                except TypeError:
                    list_options = options

                if extra_options:
                    extra_list = extra_options.split(",x")
                    list_options = options + extra_list
                else:
                    pass

                options = list_options

        if qformat == "list_options":
            check_options = line[qrows.get("extra_options")].split(",x")
        else:
            check_options = None

        if qformat == "multiple_list":
            all_extras = line[qrows.get("extra_options")].split(",XX")
            extra_lists = [l.split(",x") for l in all_extras]
        else:
            extra_lists = None

        qdic = {"question": line[0],
                "format":   line[1],
                "options":  options,
                "label":    line[3],
                "other":    line[4],
                "answer_dic": dict(),
                "check_options":check_options,
                "extra_lists": extra_lists}
        return qlab, qdic


    def define_other(self, lab):
        qdic = {"question": "If 'Other', please specify.",
                "format": "text",
                "options": "",
                "label": lab + "_other",
                "other": False }
        return qdic


    def setup_answers(self, question):
        qf = question["format"]
        simple = ("choice", "check", "list", "multiple_list")

        if qf in simple:
            choice_list = question["options"]
        if qf == "list_options":
            choice_list = question["check_options"]

        zero_indexed = ("care", "care_live")

        if qf != "text":
            if question["label"] in zero_indexed:
                idx = enumerate(choice_list, 0)
            else:
                idx = enumerate(choice_list, 1)
            answer_dic = dict([(str(text), i)
                               for i, text in idx])
        elif qf == "text":
            answer_dic = dict()

        defaults = {"99": "99",
                    "unanswered": "unanswered",
                    "na": "na"}

        answer_dic.update(defaults)

        question["answer_dic"] = answer_dic
        return None


    def get_question_order(self, ordering_in):
        qorderpath = os.path.join(self.BASE,
                                  "texts",
                                  "questionnaire_order.csv")

        with open(qorderpath, "rU") as orders:
            lab_lines = [l for l in csv.reader(orders)]
            labels = lab_lines[0]

            order_dic = dict([(label, list())
                              for label in labels])

            for line in lab_lines[1:]:
                for i, lab in enumerate(line):
                    ordering = labels[i]
                    order_dic[ordering].append(lab)

        return order_dic.get(ordering_in)


    def setup_questionnaire(self, BASE, population):

        qpath = os.path.join(BASE, "ghana_questionnaire.csv")
        with open(qpath, "rU") as gqs:
            q_lines = [line for line in csv.reader(gqs)]

        if "market" in  population:
            ordering = "market"
        else:
            ordering = "general"

        qorder = self.get_question_order(ordering)

        all_questions = dict([self.get_questions(line, population)
                              for line in q_lines])

        questions = [all_questions.get(q) for q in qorder]
        questions = [q for q in questions if q != None]


        idx0 = list() # list of tuples: (original_index, other_question)

        for i in range(len(questions)):
            q = questions[i]
            if q["other"] == "1":
                q["options"].append("Other")
                lab = q["label"]
                other = self.define_other(lab)
                idx0.append((i, other))

        idx1 = [(1 + i + j[0], j[1])
                for i, j in enumerate(idx0)]

        [questions.insert(idx_lab[0], idx_lab[1])
         for idx_lab in idx1]

        [self.setup_answers(q) for q in questions]

        questions_dic = dict(enumerate(questions, 1))

        return questions_dic


    def setup_dictionaries_and_controls(self):
        self.entry_vars_dic = dict()
        self.frames_dic = dict()
        self.question_objects = dict()
        self.nlab_dic = dict()
        self.labn_dic = dict()

        self.qs = [self.place_question(self.frame, i, dic)
                   for i, dic in self.questions.items()]

        [self.question_objects.update(dic["question_objects"])
         for dic in self.qs]

        [self.nlab_dic.update(dic["labs"])
         for dic in self.qs]

        [self.labn_dic.update(dic["lab_to_n"])
         for dic in self.qs]

        self.control_questions()
        return None


    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

        [dic.update({"yview":dic["frame"].winfo_rooty()})
         for dic in self.question_objects.values()]

    def hide_questionnaire(self):
        self.master.pack_forget()

    def setup_formats(self):
        qf = namedtuple("QF", "grid place_function extra_kwargs non_answer")

        formats = ("text",
                   "list",
                   "choice",
                   "check",
                   "list_options",
                   "multiple_list")

        functions = {"multiple_list": self.draw_list,
                     "list": self.draw_list ,
                     "text": self.draw_text,
                     "choice": self.draw_choice,
                     "check": self.draw_check,
                     "list_options": self.draw_options_list}

        extra_kwargs = {"text" : None,
                      "list": None,
                      "choice": None,
                      "check": None,
                      "list_options": "check_options",
                      "multiple_list": "extra_lists"}


        nonanswer = {"text" : True,
                     "list": True,
                     "choice": True,
                     "check": True,
                     "list_options": False,
                     "multiple_list": True}

        grid10 = (1, 0)
        grid03 = (0, 3)

        nonanswer_grids = {'text':  grid10,
                           "list":  grid10,
                           'choice': grid03,
                           'check': grid03,
                           'list_options': grid03,
                           "multiple_list": grid10}

        qf_options = dict([(f, qf(nonanswer_grids.get(f),
                                  functions.get(f),
                                  extra_kwargs.get(f),
                                  nonanswer.get(f))) for f in formats])
        return qf_options

    def setup_question_basics(self, master, n,
                              qlab, qformat, qtext, qadic, other_idx):


        bframe = tk.Frame(master)
        question_frame = tk.Frame(bframe)
        bframe.pack(side = "top",
                    anchor = "w",
                    expand = "True",
                    fill = "x")

        question_frame.pack(side = "top",
                            anchor = "w",
                            expand = "True",
                            fill = "x",
                            padx = 4,
                            pady = 4)

        question_frame.bind("<Button-1>",
                            self.highlight_from_frame_press)

        question_frame.bind_all("<Up>",
                                lambda event, up_var = True: \
                                self.highlight_from_key_press(event,
                                                              up = up_var))
        question_frame.bind_all("<Down>",
                                lambda event, up_var = False: \
                                self.highlight_from_key_press(event,
                                                              up = up_var))

        bframe.bind_all("<Tab>", self.cycle_select_question)

        label_frame = tk.Frame(question_frame)
        label_frame.grid(row = 1, column = 1, sticky = 'w')

        answer_frame = tk.Frame(question_frame)
        answer_frame.grid(row = 2, column = 1, pady = 3)

        questionfont = tkFont.Font(question_frame, size = 18)
        question_number = tk.Label(question_frame,
                                   text = "Q{}.".format(n),
                                   font = questionfont)
        question_number.grid(row = 1, column = 0, sticky = 'nw')

        question_text_lab = tk.Label(label_frame,
                                     text = qtext,
                                     justify = 'left',
                                     font = questionfont,
                                     wraplength = 1000)
        question_text_lab.grid(row = 0, column = 0)

        [self.frames_dic.update({widget:n})
         for widget in (question_frame, bframe)]

        question_objects = {'text_lab': question_text_lab,
                            'numlab': question_number,
                            "frame": bframe,
                            'text': qtext,
                            'qlab': qlab,
                            'yview': 0,
                            'other': other_idx,
                            "format": qformat,
                            "answer_dic": qadic}

        return answer_frame, question_objects


    def draw_question_answer(self, master, n,
                             qlab, qformat, qoptions, qdic, qf_options,
                             qobject_dic):
        answer_var = tk.StringVar(master)
        answer_var.set("99")

        extra_kwarglist = qf_options.extra_kwargs
        no_kwargs = {"": None}

        if extra_kwarglist:
            extra_kwargs = {extra_kwarglist: qdic.get(extra_kwarglist)}

        else:
            extra_kwargs = no_kwargs

        def variable_traces(answer_var, show_var):
            def display_answer(name, index, mode):
                a = answer_var.get()
                try:
                    if int(a) < 100:
                        show_var.set(a)
                    elif int(a) > 100:
                        show_var.set("---")
                except ValueError:
                    show_var.set(a)
                return None

            def set_shown_answer(name, index, mode):
                answer = show_var.get()
                if answer != "---":
                    answer_var.set(show_var.get())
                elif answer == "---":
                    pass
            return display_answer, set_shown_answer


        answer_args = (master, qlab, qformat,
                       answer_var, qoptions, variable_traces, qobject_dic)

        answer_function =  qf_options.place_function
        answer_kwargs = extra_kwargs

        qwidgets, answer_var, qobject_dic = answer_function(*answer_args,
                                                           **answer_kwargs)

        buttons = self.draw_nonanswers(master, answer_var, qf_options)

        widgets = qwidgets + buttons
        [self.frames_dic.update({widget:n}) for widget in widgets]

        [w.bind("<Button-1>", self.highlight_from_frame_press)
         for w in widgets]

        qobject_dic.update({"widgets": widgets})
        return qwidgets, answer_var, qobject_dic


    def draw_nonanswers(self, master, answer_var, qf_options):
        pref_configs = [('prefer not to answer', "765"),
                        ('do not know', "865"),
                        ("not applicable", "965")]

        buttons = [tk.Radiobutton(master,
                                  text = msg,
                                  font = tkFont.Font(size = 10),
                                  variable = answer_var,
                                  value = val)
                   for msg, val in pref_configs]

        n1, n2, n3 = buttons
        g_row, g_col = qf_options.grid

        if qf_options.non_answer == True:
            [nbutt.grid(row = brow,
                        column = g_col,
                        sticky = 'w',
                        padx = 8)
             for nbutt, brow in [(n1, g_row),
                                 (n2, g_row + 1),
                                 (n3, g_row + 2)]]
        elif qf_options.non_answer == False:
            pass

        return buttons


    def place_question(self, master, n, qdic):
        qtext = qdic.get("question")
        qformat = qdic.get("format")
        qlab = qdic.get("label")
        qoptions = qdic.get("options")
        check_options = qdic.get("check_options")
        extra_lists = qdic.get("extra_lists")
        qadic = qdic.get("answer_dic")

        if int(qdic["other"]) == True:
            other_idx = len(qoptions) - 1
        else:
            other_idx = 0

        all_apply = " Please check all that apply"
        if qformat == "check":
            qtext = qtext + all_apply

        qf_options = self.qformats_dic.get(qformat)

        if qlab == "weekly_monthly":
            qf_options = qf_options._replace(non_answer = False)

        question_basics = (master, n, qlab, qformat, qtext, qadic, other_idx)
        answer_frame, \
            question_objects  = self.setup_question_basics(*question_basics)

        answer_basics = (answer_frame, n,
                         qlab, qformat, qoptions, qdic, qf_options,
                         question_objects)

        qwidgets, \
            answer_var, \
            question_objects = self.draw_question_answer(*answer_basics)




        question_objects_dic = {n: question_objects}
        nlab_dic = {n:qlab}
        labn_dic = {qlab:n}

        self.toggle_enable_question(question_objects, False)


        return {"question_objects": question_objects_dic,
                "labs": nlab_dic,
                "lab_to_n": labn_dic}


    def draw_check(self, master, lab, qformat,
                   answer_var, options, show_functions, qdic,
                   **kwargs):
        answer_var.set("anything but the phospene")
        check_vars = [tk.IntVar(master)
                      for i in range(len(options))]
        [v.set(0) for v in check_vars]
        bts = [tk.Checkbutton(master,
                              variable = var,
                              justify = 'left',
                              text = option)
               for option, var in zip(options, check_vars)]

        [bt.grid(row = i, column = 1, sticky = 'w')
         for i, bt in enumerate(bts)]

        def clear_checked(name, index, mode):
            if answer_var.get() in ("765", "865", "965"):
                [var.set(False) for var in check_vars]
                print "changed here"
                return None

        def clear_answer(name, index, mode):
            answer_var.set(0)
            return None

        [var.trace("w", clear_answer) for var in check_vars]
        answer_var.trace("w", clear_checked)
        qwidget = bts
        answer = answer_var
        qdic.update({"answer": answer_var,
                     "check_vars": check_vars})
        return qwidget, answer_var, qdic


    def draw_choice(self, master, lab, qformat,
                  answer_var, options, show_functions, qdic,
                  **kwargs):

        bts = [tk.Radiobutton(master,
                              variable = answer_var,
                              justify = 'left',
                              value = i,
                              text = option)
            for i, option in enumerate(options)]

        [bt.grid(row = i, column = 1, sticky = 'w')
         for i, bt in enumerate(bts)]

        qwidget = bts
        answer = answer_var

        qdic.update({"answer": answer_var})
        return qwidget, answer_var, qdic


    def draw_text(self, master, lab, qformat,
                  answer_var, options, show_functions, qdic,
                  **kwargs):

        show_var = tk.StringVar(master)

        entry_widget = tk.Entry(master,
                                textvariable = show_var)
        entry_widget.grid(row = 0, column = 0)

        entry_var_dic = {"answer_var": answer_var,
                         "widget": entry_widget}

        display_answer, \
            set_shown_answer = \
                               show_functions(answer_var, show_var)

        answer_var.trace("w", display_answer)
        show_var.trace("w", set_shown_answer)

        self.entry_vars_dic.update({answer_var.__str__():entry_var_dic})
        entry_events = ("<FocusIn>", "<Button-1>")

        [entry_widget.bind(event, self.empty_entry_box)
         for event in entry_events]

        qwidget = [entry_widget]
        answer = answer_var
        qdic.update({"answer": answer_var})

        return qwidget, answer_var, qdic


    def draw_list(self, master, lab, qformat,
                  answer_var, options, show_functions, qdic,
                  **kwargs):

        extra_lists = kwargs.get("extra_lists")
        show_var = tk.StringVar(master)

        display_answer, \
            set_shown_answer = \
                               show_functions(answer_var, show_var)

        answer_var.trace("w", display_answer)
        show_var.trace("w", set_shown_answer)

        listoptions = tuple(options)
        listbox = apply(tk.OptionMenu,
                        (master, show_var) + listoptions)

        if qformat == "multiple_list":

            def make_extra_list(options):
                weeklylist = tuple(options)
                weeklylistbox = apply(tk.OptionMenu,
                                      (master, show_var) + weeklylist)
                return weeklylistbox, options

            lists = [make_extra_list(l)
                             for l in extra_lists]

            listboxes = [l[0] for l in lists]
            options = [l[1] for l in lists]

            qwidget = listboxes

            if lab == "income_individual":
                multiple_lists = {"weekly": qwidget[0],
                                  "monthly": qwidget[1]}
                answer_options = {"weekly": options[0],
                                  "monthly": options[1]}
            else:
                pass
            qdic.update({"multiple_lists": multiple_lists,
                         "answer_options": answer_options})

        elif qformat != "multiple_list":
            listbox.grid(row = 0, column = 0)
            qwidget = [listbox]

        answer = answer_var
        qdic.update({"answer": answer_var})
        return qwidget, answer_var, qdic


    def draw_options_list(self, master, lab, qformat,
                          answer_var, options, show_functions, qdic,
                          **kwargs):
        check_options = kwargs.get("check_options")

        label = lab
        frames = [tk.Frame(master) for i in options]
        labs = [tk.Label(frame, text = option)
                for frame, option in zip(frames, options)]

        check_vars = [tk.StringVar(master) for i in options]
        [v.set("na") for v in check_vars]

        list_boxes = [apply(tk.OptionMenu,
                            (frame, var) + tuple(check_options))
                      for frame, var in zip(frames, check_vars)]

        for i, lab in enumerate(labs):
            lab.grid(row = i, column = 0, sticky  = "w")

        for i, listbox in enumerate(list_boxes):
            listbox.grid(row = i, column = 1, sticky  = "e")

        if label == "care" or label == "care_live":
            [v.set(0) for v in check_vars]
            [frame.grid(row = i, sticky = "w")
             for i, frame in enumerate(frames)]

        qwidget = frames
        answer = answer_var
        qdic.update({"answer": answer_var,
                     "check_vars": check_vars})
        return qwidget, answer_var, qdic


    def empty_entry_box(self, event):
        entry_box = event.widget
        entry_box.delete(0, "end")

    def show_active(self, frame_id, on):
        qdic = self.question_objects[frame_id]

        frame = qdic["frame"]
        widgets = qdic["widgets"]

        if on == True:
            check_other = (qdic["format"] == "check"
                           and qdic["other"] > 0)

            if check_other:
                self.next_disabled = True
                self.n_skip.set(2)

            frame.config(bg = "green")
            self.toggle_enable_question(qdic, on)
            [w.config(takefocus = 1) for w in widgets]
            frame.focus_set()
            self.current_widget = frame

            coord = self.get_coordinates(frame_id)
            self.canvas.yview("moveto", coord)

        else:
            #Change to be system specific!!
            frame.config(bg = "white")
            [w.config(takefocus = 0) for w in widgets]

        return None



    def get_coordinates(self, idx):
        keys = self.question_objects.keys()

        i1 = keys[0]
        iN = keys[-1]

        begin, end, nidx = [self.question_objects[max(n-2, 1)]["yview"]
                            for n in (i1, iN, idx)]

        num = nidx - begin - 100
        denom = end - begin

        try:
             c = float(num)/denom
        except ZeroDivisionError:
            c = 0

        return c

    def check_answer(self, idx):
        if self.question_objects[idx]["format"] != "list_options":
            response = self.question_objects[idx]["answer"].get()

            null_answer = ["", 99, "99"]

            if response in null_answer:
                go_next = False
            else:
                go_next = True

        else:
            responses = [v.get()
                         for v in self.question_objects[idx]["check_vars"]]
            if "unanswered" in responses:
                go_next = False
            else:
                go_next = True

        return go_next


    def go_next(self, event):
        idx_x = self.active_frame_var.get()
        idx0 = self.latest_frame_var.get()


        if idx_x < idx0:
            self.highlight_next_question(idx_x, idx0)

        elif idx_x == idx0:

            if self.check_answer(idx0):
                base = self.question_idx.get()

                i = 1 if self.next_disabled == False else self.n_skip.get()
                self.next_disabled = False
                idx1 = base + i
                if idx1 > max(self.question_objects.keys()):
                    self.complete_var.set(True)
                    pass
                elif idx1 <= max(self.question_objects.keys()):

                    self.question_idx.set(idx1)
                    self.highlight_next_question(idx0, idx1)

                    if idx1 not in self.answered_questions:
                        self.answered_questions.append(idx1)
                    else:
                        pass

                    if idx1 >= max(self.answered_questions):
                        self.update_progress_bar(idx1)
                    else:
                        pass

            else:
                tkMessageBox.showinfo("No answer given",
                                      "Please answer Question {}".format(idx0))

        return None

    def update_progress_bar(self, idx):
        xn = 20 + idx * self.bar_increment
        self.progress.coords(2, (20, 20, xn, 30))

    def cycle_select_question(self, event):
        next_widget = self.current_widget.tk_focusNext()
        next_widget.focus_set()

        if next_widget.winfo_class() == "Radiobutton":
            next_widget.select()
        elif next_widget.winfo_class() == "Radiobutton":
            next_widget.toggle()
        elif next_widget.winfo_class() == "Entry":
            pass

        self.current_widget = next_widget
        return None


    def highlight_next_question(self, idx0, idx1):

        idx_x = self.active_frame_var.get()

        ids = (idx0, idx_x, idx1)
        on = (False, False, True)

        [self.show_active(frame, status)
         for frame, status in zip(ids, on)]
        self.latest_frame_var.set(idx1)
        self.active_frame_var.set(idx1)
        return None

    def highlight_from_frame_press(self, event):
        frame = event.widget
        lab_on = self.frames_dic[frame]

        # print "sort of almost there"
        # if lab_on not in self.answered_questions:
        #     print "do nothing"
        #     activate = False
        #     pass
        # elif lab_on in self.answered_questions:
        #     print "do something"
        #     activate = True


#        if activate == True and lab_on <= self.latest_frame_var.get():
        if lab_on in self.answered_questions:
            lab_off = self.active_frame_var.get()

            if lab_on == lab_off:
                pass
            elif lab_on != lab_off:
                [self.show_active(lab, on)
                 for lab, on in zip((lab_on, lab_off), (True, False))]
                self.active_frame_var.set(lab_on)
        return None

    def highlight_from_key_press(self, event, up):
        frame = event.widget

        lab_current = self.frames_dic[frame]
        i = self.answered_questions.index(lab_current)

        if up == True:
            diff = -1
        elif up == False:
            diff = 1

        try:
            lab_on = self.answered_questions[i + diff]

            if lab_on <= self.latest_frame_var.get():
                lab_off = self.active_frame_var.get()

                if lab_on == lab_off:
                    pass
                elif lab_on != lab_off:
                    [self.show_active(lab, on)
                     for lab, on in zip((lab_on, lab_off), (True, False))]
                    self.active_frame_var.set(lab_on)
        except:
            pass

        return None


    def toggle_enable_question(self, qdic, on):
        widget_list = qdic['widgets']
        qlab = qdic['text_lab']
        numlab = qdic['numlab']

        if on == True:
            toggle_state = "normal"
            toggle_colour = "black"
        else:
            toggle_state = "disabled"
            toggle_colour = "gray"

        [lab.config(fg = toggle_colour) for lab in (qlab, numlab)]

        if qdic["format"] != "list_options":
            [w.config(state = toggle_state) for w in widget_list]

        elif qdic["format"] == "list_options":
            widgets = list()
            [widgets.extend(w.winfo_children()) for w in widget_list]
            [w.config(state = toggle_state) for w in widgets]


    def control_other(self, on, n_list, q_list):
        if on == True:
            self.question_idx.set(n_list[0])
            self.latest_frame_var.set(n_list[0])

            if n_list[1] in self.answered_questions:
                pass
            else:
                [self.answered_questions.insert(n1, n1)
                 for n1 in n_list[1:]]

            self.next_disabled = False

        elif on == False:
            if n_list[1] in self.answered_questions:
                pop_idx = [self.answered_questions.index(n1)
                           for n1 in n_list[1:]]

                [self.answered_questions.pop(pop_idx[0])
                 for idx in pop_idx]

                last_q = max(self.answered_questions)
                self.question_idx.set(last_q)
                self.latest_frame_var.set(last_q)

                if last_q > n_list[0]:
                    self.next_disabled = False
                elif last_q == n_list[0]:
                    self.next_disabled = True

            else:
                self.next_disabled = True

        [self.toggle_enable_question(q1, on)
         for q1 in q_list[1:]]

        return None

    def control_dependent(self, on, n0, q1, num):

        if on == True:
            q1["widgets"][num].grid(row = num, sticky = "w")
            q1["check_vars"][num].set("unanswered")
            self.question_idx.set(n0)
            self.latest_frame_var.set(n0)

        elif on == False:
            q1["widgets"][num].grid_forget()
            q1["check_vars"][num].set(0)

            last_q = max(self.answered_questions)
            self.question_idx.set(last_q)
            self.latest_frame_var.set(last_q)


    def get_routing_functions(self, labels, control_var, num):

        def control(name, index, mode):
            n_list = [self.labn_dic.get(lab) for lab in (labels)]

            q_list = [self.question_objects.get(n)
                      for n in n_list]

            self.n_skip.set(len(n_list))


            control_bool_true = lambda x, y: x == y
            control_bool_false = lambda x, y: x != y

            control_answer = q_list[0]["answer"].get()
            other_idx = q_list[0]["other"]

            if control_var == "other":
                controls = (control_answer, str(other_idx))

            elif control_var == "check_other":
                other_var = q_list[0]["check_vars"][other_idx].get()
                controls = (other_var, True)

            elif control_var == "check":
                check_var = q_list[0]["check_vars"][num].get()
                controls = (check_var, True)

            else:
                controls = (control_answer, str(control_var))

            if control_bool_true(*controls):
                if control_var != "check":
                    self.control_other(True, n_list, q_list)
                elif control_var == "check":
                    self.control_dependent(True, n_list[0], q_list[1], num)

            if control_bool_false(*controls):
                if control_var != "check":
                    self.control_other(False , n_list, q_list)
                elif control_var == "check":
                    self.control_dependent(False, n_list[0], q_list[1], num)


        def control_2(name, index, mode):
            last_q = max(self.answered_questions)
            self.question_idx.set(last_q)
            self.latest_frame_var.set(last_q)


        n_control = len(labels) - 1

        trace = {"other": ("answer", "answer"),
                 "check_other": ("check_other", "answer"),
                 "check": ("check",)}

        t = trace.get(control_var, trace["other"])

        if control_var != "check":
            control_functions = (control,) + (control_2,) * n_control
            trace_types = (t[0],) + (t[1],) * n_control
        elif control_var == "check":
            control_functions = (control,)
            trace_types = t


        nums = (num,) * (n_control + 1)
        return zip(labels, control_functions, trace_types, nums)


    def control_weekly_monthly(self, name, index, mode):
        n_timing =  self.labn_dic.get("weekly_monthly")
        n_timing_dic = self.question_objects[n_timing]
        timing = n_timing_dic.get("answer").get()


        timing_dic = {"0" :"month", "1": "week"}

        n = self.labn_dic.get("income_individual")
        ndic = self.question_objects[n]
        lab = ndic.get("text_lab")
        listboxes = ndic.get("multiple_lists")
        answer_options = ndic.get("answer_options")
        [l.grid_forget() for l in listboxes.values()]

        listbox = None

        if timing not in ("765", "865", "965"):
            if timing == "0":
                str_idx = "monthly"
            if timing == "1":
                str_idx = "weekly"

            listbox = listboxes.get(str_idx)
            options = answer_options.get(str_idx)
        elif timing in ("765", "865", "965"):
            self.next_disabled = True


        if listbox:
            listbox.grid(row = 0, column = 0)
            time_text = ndic.get("text").format(timing_dic.get(timing))
            lab.config(text = time_text)
            ndic["answer_dic"] = dict([(str(opt), i)
                                           for i, opt in enumerate(options)])

    def control_denomination(self, name, index, mode):
        n, nother = [self.labn_dic.get(d)
                     for d in ("denomination", "denomination_other")]

        ndic = self.question_objects[n]
        notherdic = self.question_objects[nother]


        denom_code = ndic.get("answer").get()

        if denom_code == "0":
            denomination = "AoG Shammah Temple"
        elif denom_code == "1":
            denomination = "AoG Ebenezer"
        elif denom_code == "2":
            denomination = "AoG Abundant Life"
        elif denom_code == "3":
            denomination = "AoG Dansoman"
        elif denom_code == "4":
            denomination = "AoG House of Hope"
        elif denom_code == "5":
            denomination = "AoG Redemption"
        elif denom_code in ("765", "865", "965"):
            denomination = "your church"
        else:
            denomination = notherdic.get("answer").get()

        denomination = denomination.upper()


        denomination_text = ["different_church",
                             "church_reasons",
                             "church_assistance",
                             "church_move",
                             "church_giving",
                             "church_attendance",
                             "church_length",
                             "church_distance",
                             "church_ministry",
                             "church_convince"]

        n_list = [self.labn_dic.get(key)
                  for key in denomination_text]

        text_labs = [self.question_objects[key]["text_lab"]
                     for key in n_list]

        texts = [self.question_objects[key]["text"]
                 for key in n_list]

        [lab.config(text = qtext.format(denomination))
         for lab, qtext in zip(text_labs, texts)]



    def control_church_mosque(self, name, index, mode):
        mosque_text = ["charity",
                       "closefriends",
                       "coworkers",
                       "business_partners"]

        n_list = [self.labn_dic.get(key)
                  for key in mosque_text]

        n = self.labn_dic["religion"]

        if self.question_objects[n]['answer'].get() == "4":
            self.religion_var.set("muslim")
            religious_house = "mosque"
        elif self.question_objects[n]['answer'].get() == "5":
            self.religion_var.set("other")
            religious_house = "institution"
        else:
            self.religion_var.set("church")
            religious_house = "church"


        text_labs = [self.question_objects[key]["text_lab"]
                     for key in n_list]

        texts = [self.question_objects[key]["text"]
                 for key in n_list]

        [lab.config(text = qtext.format(religious_house))
         for lab, qtext in zip(text_labs, texts)]



    def get_dependent_vars(self, labels):
        n = self.labn_dic.get(labels[0])
        q = self.question_objects.get(n)


        check_vars = enumerate(q["check_vars"])

        functions_list = [self.get_routing_functions(labels,
                                                     "check",
                                                     num)
                          for num, var in check_vars]

        functions = list(itertools.chain.from_iterable(functions_list))
        return functions


    def get_other_functions(self):

        check_info = [(q["qlab"], q["check_vars"][q["other"]])
                      for q in self.question_objects.values()
                      if q["other"] > 0 and q["format"] == "check"]

        check_labs = [tup[0] for tup in check_info]
        check_vars = [tup[1] for tup in check_info]

        choice_labs = [q["qlab"]
                       for q in self.question_objects.values()
                       if q["other"] > 0 and q["format"] == "choice"]

        labs = check_labs + choice_labs

        ncheck, nchoice = [len(clist) for clist in (check_labs, choice_labs)]

        labs_other = [l + "_other" for l in labs]
        var_types = ("check_other",) * ncheck + ("other",) * nchoice

        other_labs = zip(labs, labs_other)
        other_labs_types = zip(other_labs, var_types)

        functions_list = [self.get_routing_functions(labs, types, "")
                          for labs, types in other_labs_types]

        functions = list(itertools.chain.from_iterable(functions_list))
        return functions, check_vars


    def trace_routing(self, label, function, trace_type, n_var):
        n_idx = self.labn_dic[label]
        qdic = self.question_objects[n_idx]

        if trace_type == "answer":
            trace_var = qdic['answer']

        elif trace_type == "check_other":
            other_idx =  qdic['other']
            trace_var = qdic['check_vars'][other_idx]

        elif trace_type == "check":
            trace_var = qdic['check_vars'][n_var]

        trace_var.trace("w", function)



    def control_questions(self):

        ministry_labs = ("church_ministry",
                         "church_ministry_hours")
        ministry_check = self.get_dependent_vars(ministry_labs)

        monthly_labs = ("monthly_expenses",
                        "monthly_expenses_amount")
        monthly_check = self.get_dependent_vars(monthly_labs)

        left_ghana_labs = ("left_ghana",
                           "left_ghana_location")

        own_business_labs = ("business_ownership",
                             "business_length",
                             "business_employees")

        market_association_labs = ("kaneshie_association",
                                   "kaneshie_years",
                                   "kaneshie_dues")

        nih_labs = ("nih",
                    "nih_reason")

        insurance_labs = ("other_insurance",
                          "other_insurance_specify")

        continue_labs = (left_ghana_labs,
                         own_business_labs,
                         nih_labs,
                         insurance_labs)

        if self.treatment_dic.get("population") == "market":
            continue_labs = continue_labs + (market_association_labs,)

        continue_lists = [self.get_routing_functions(labs, 0, " ")
                           for labs in continue_labs]
        continue_routes = list(itertools.chain(*continue_lists))


        other_info = self.get_other_functions()
        other_questions = other_info[0]
        other_vars = other_info[1]

        routing = other_questions +\
                  ministry_check +\
                  monthly_check +\
                  continue_routes

        self.trace_routing("religion",
                           self.control_church_mosque,
                           "answer",
                           "")
        [self.trace_routing(d, self.control_denomination,
                            "answer", "") for d in
         ("denomination", "denomination_other")]

        self.trace_routing("weekly_monthly",
                           self.control_weekly_monthly,
                           "answer",
                           "")
        [self.trace_routing(*varlist) for varlist in routing]

    def get_response(self, question):
        qformat = question["format"]
        qlab = question["qlab"]
        a_var = question["answer"]
        a_dic = question["answer_dic"]

        if qformat == "check" or qformat == "list_options":
            check_vars = question["check_vars"]
            labs = [qlab + "_{}".format(i)
                    for i, k in enumerate(check_vars)]

            if qformat == "list_options":
                pre_answers = [v.get() for v in check_vars]
                answers = [a_dic.get(v.get()) for v in check_vars]

            elif qformat == "check":
                answers = [str(v.get()) for v in check_vars]

        else:
            labs = [qlab]
            if qformat == "text":
                answers = [a_var.get()]
            if qformat in ("list", "multiple_list"):
                answers = [a_dic.get(a_var.get())]
            elif qformat == "choice":
                answers = [a_var.get()]
        try:
            answer_tuples = zip(labs, answers)
        except:
            print qlab

        return answer_tuples


    def get_all_responses(self):
        questions = self.question_objects.values()
        a_raw = [self.get_response(q) for q in questions]

        a_unchained = list(itertools.chain(*a_raw))

        return a_unchained


    def write_data(self):
        idx = [(key, str(value))
               for key, value in self.treatment_dic.items()]
        survey = self.get_all_responses()
        filename = self.global_write_data("wb", idx + survey)
        print "Survey data written to {}".format(filename)


def run_questionnaire():
    BASE = os.path.join((os.path.dirname(__file__)))

    treatment_dic = {"session": 0,
                     "desk": 155,
                     "population": "market",
                     "public": True,
                     "insurance": "credit"}

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

    root = tk.Tk()
    root.attributes("-fullscreen",True)
    bob = Questionnaire(root, BASE, treatment_dic, write_data)
    #root.mainloop()
    print "bobalicious"
    return bob


#aaron = run_questionnaire()
