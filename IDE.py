from tkinter import *

from Lexer import Lexer
from Token import *
from Interpreter import Interpreter
import multiprocessing as mp

import json
import re

with open("keywords.json", "r") as f:
    KWS = json.load(f)

with open("vars.json", "r") as f:
    VARS = json.load(f)

BG = "#333333"
FG = "#c0c0c0"


class Q(object):

    def __init__(self):
        self.queue = mp.Queue()

    def write(self, string):
        self.queue.put(string)

    def get(self):
        res = ""
        while not self.queue.empty():
            res += self.queue.get()
        return res


class IDE(object):

    def __init__(self, master):

        self.thread = None
        self.queue = Q()
        self.master = master

        self.code = Text(self.master, bg=BG, fg=FG, insertbackground=FG)
        self.code.grid(row=0, column=1, rowspan=3, sticky=NSEW)
        self.code.bind("<KeyRelease>", self.highlight)

        self.code.tag_config("keyword", foreground="#ff4500")
        self.code.tag_config("var", foreground="#c71585")
        self.code.tag_config("prev", foreground="#89cff0")
        self.old_code = [""]

        self.tokens = Text(self.master, state=DISABLED, bg=BG, fg=FG)
        self.tokens.grid(row=0, column=2, columnspan=3, sticky=NSEW)

        Label(self.master, text="Terminal", anchor=W).grid(row=1, column=2, sticky=W)
        Button(self.master, text="Compile", command=self.compile).grid(row=1, column=3, sticky=EW)
        self.run_button = Button(self.master, text="Run", command=self.run)
        self.run_button.grid(row=1, column=4, sticky=EW)

        self.terminal = Text(self.master, state=DISABLED, bg=BG, fg=FG)
        self.terminal.grid(row=2, column=2, columnspan=3, sticky=NSEW)

        self.master.columnconfigure(1, weight=3)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(2, weight=1)

    def highlight(self, *args):
        code = self.code.get("0.0", END).split("\n")
        for i in range(len(code)):
            if i < len(self.old_code) and code[i] == self.old_code[i]:
                continue

            self.code.tag_remove("keyword", f"{i + 1}.0", f"{i + 1}.{len(code[i])}")
            self.code.tag_remove("var", f"{i + 1}.0", f"{i + 1}.{len(code[i])}")
            self.code.tag_remove("prev", f"{i + 1}.0", f"{i + 1}.{len(code[i])}")

            for KW in sorted(set(KWS) | {VAR for VARTYP in VARS for VAR in VARS[VARTYP]}, reverse=True):
                if re.sub(r"\W", "", KW):
                    m = re.match("(?:.*)(?:\W|\A)(" + KW.replace(" ", r"\s+") + ")(?=(\W|\Z))", code[i].upper())
                    if m is not None:
                        if KW in KWS:
                            self.code.tag_add("keyword", f"{i + 1}.{m.start(1)}", f"{i + 1}.{m.end(1)}")
                        else:
                            for VARTYP in VARS:
                                if KW in VARS[VARTYP]:
                                    self.code.tag_add("prev" if VARTYP == "PREV" else "var",
                                                      f"{i + 1}.{m.start(1)}", f"{i + 1}.{m.end(1)}")
                                    break

        self.old_code = code

    def compile(self):
        try:
            self.tokens["state"] = NORMAL
            tokens = Lexer(self.code.get("0.0", END)).tokenize()
            self.tokens.delete("0.0", END)

            translated = ""
            scope = 0
            for token in tokens:
                if token.typ in ["WHILE", "GOES", "FUNC ASSIGN", "IF", "ELSE"]:
                    scope += 1
                elif token.typ == "LOCAL END":
                    scope -= 1

                if token.typ in FACTORS + ["ID"]:
                    translated += " [" + str("PREV" if token.val is None else token.val) + "]"
                elif token.typ in ENDING:
                    translated += "\n" + "    " * scope
                else:
                    translated += " " + token.typ

                # print(token.typ, scope)

            translated = re.sub("\n\s+\n", "\n", translated.replace("\n ", "\n")).strip()
            self.tokens.insert(END, translated)
            self.tokens["state"] = DISABLED
        except Exception as e:
            self.tokens["state"] = NORMAL
            self.tokens.delete("0.0", END)
            self.tokens.insert(END, str(e))
            self.tokens["state"] = DISABLED
            pass

    def run(self):

        if self.thread is None:
            self.compile()
            self.thread = mp.Process(target=Interpreter(self.code.get("0.0", END), self.queue).run, daemon=True)
            self.thread.start()
            self.master.after(1, self.check)
            self.run_button["text"] = "Stop"

            self.terminal["state"] = NORMAL
            self.terminal.delete("0.0", END)
            self.terminal["state"] = DISABLED
        else:
            self.thread.terminate()

    def check(self):
        self.write()
        if not self.thread.is_alive():
            self.thread.join()
            self.thread = None
            self.run_button["text"] = "Run"
        else:
            self.master.after(1, self.check)

    def write(self):
        self.terminal["state"] = NORMAL
        self.terminal.insert(END, self.queue.get())
        self.terminal.see(END)
        self.terminal["state"] = DISABLED



if __name__ == '__main__':
    root = Tk()
    ide = IDE(root)

    root.mainloop()
