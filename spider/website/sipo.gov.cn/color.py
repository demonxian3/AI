class Color:
    def __init__(self):
        self.f = {};
        self.b = {};

        self.f['black']  = "\033[30m";
        self.f['red']    = "\033[31m";
        self.f['green']  = "\033[32m";
        self.f['yellow'] = "\033[33m";
        self.f['blue']   = "\033[34m";
        self.f['violet'] = "\033[35m";
        self.f['cyan']   = "\033[36m";
        self.f['white']  = "\033[37m";
        self.f['gray']   = "\033[38m";

        self.b['black']  = "\033[40m";
        self.b['red']    = "\033[41m";
        self.b['green']  = "\033[42m";
        self.b['yellow'] = "\033[43m";
        self.b['blue']   = "\033[44m";
        self.b['violet'] = "\033[45m";
        self.b['cyan']   = "\033[46m";
        self.b['white']  = "\033[47m";
        self.b['gray']   = "\033[48m";

        self.cls = "\033[0m";

    def show(self, string, color, isbg=0):
        if isbg == 1:
            print self.b[color] + string + self.cls;
        else:
            print self.f[color] + string + self.cls;
