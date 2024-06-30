from sample_library.ImportMod1 import ImportMod11, ImportMod12

def ModuleMoveFunction1(a, b, c, d=None):

    mod1 = ImportMod11()

    mod1.mod112()


def ModuleMoveFunction2(d, e, r, a):
    mod1 = ImportMod11()
    mod2 = ImportMod12()

    mod2.mod121(mod1.mod112)
