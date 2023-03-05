# ********************************************* VARIABLE SECTION ******************************************************

# ---------------------------------------- gen 1 cipdie symbols ------------------------------------------------------

gauge = [" ", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "1", "2", "3", "4", "5",
         "6", "7", "8", "9", "0", "@", ":", "&", "%", ";", 'A', 'B', 'C', 'D', 'E', 'F',
         'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z', "<", ">", ",", ".", "$", "-", "+", "/", "*", "!", "?", "#",  # 80CO
         " ", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "1", "2", "3", "4", "5",
         "6", "7", "8", "9", "0", "@", ":", "&", "%", ";", 'A', 'B', 'C', 'D', 'E', 'F',
         'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z', "<", ">", ",", ".", "$", "-", "+", "/", "*", "!", "?", "#"]

nfound = "^"

# ----------------------------------------VARIABLES FOR GUI AND LOGIC ENGINE------------------------------------------

diekey = 0  # for save the encode key by default is 0

keycheck = False  # for conformation key is checked or not by default False
textout = str()

orecode = ""  # for get the ore serial from the text
buffermem = int()  # filter the text and serial

encoding = False  # to find decoding is done or not
decoding = False  # to find decoding is done or not


# ********************************************** LOGIC ENGINE SECTION *************************************************

# for message to title bar or status bar
def throwmessage(itstype, message, solution=" "):
    match itstype:
        case "warning":
            print("> ", message, " --->", solution)
        case "message":
            print("> ", message, " --->", solution)
        case "notify":
            print("> ", message, " --->", solution)
        case "LES":
            print("> ", message, " --->", solution)
        case _:
            print("message  not defined")
    print(" ")


# function to check the encode key
def checkkey(inpkey):
    global diekey, keycheck

    try:
        diekey = int(inpkey)
    except ValueError:
        throwmessage("warning", "encode key TYPE is invalid",
                     "please enter numerical values")
    else:
        if not (999 < diekey < 10000):
            throwmessage("message", "key is invalid",
                         " keep key in 1000 to 9999")
        else:
            throwmessage("notify", "continue next process",
                         f" '{diekey}' key is valid")
            keycheck = True  # now key is tested


# ENGINE FOR GEN1 ENCODE AND DECODE
def operation(mode, inpkey, textdata):
    global keycheck, textout, gauge, orecode, buffermem, decoding, encoding, diekey

    textout = textdata
    match mode:

        case "encode":

            encoding = False
            keycheck = False
            checkkey(inpkey)

            if keycheck is True:
                buffermem = 0

                for shiftvalue in str(inpkey):  # MAIN ENCODER LOOP ***************
                    # print(" ")

                    elements = textout
                    textout = ""
                    buffermem = shiftvalue
                    for char1 in elements:
                        if char1 in gauge:
                            pos = gauge.index(char1)
                            n_pos = pos + int(shiftvalue)
                            textout += gauge[int(n_pos)]
                            # print("encode n_pos ", n_pos)
                        else:
                            textout += nfound

                serial = str(len(textout) + diekey) + str(buffermem)
                serial = "".join(reversed(serial))

                textout = f"SSETG1_{serial}___" + textout

                throwmessage("notify", "Encode done",
                             f"Encode key is {inpkey}")
                encoding = True
            else:
                textout = "ENCODE IS NOT DONE"

        case "decode":

            decoding = False
            keycheck = False
            checkkey(inpkey)

            if keycheck is True:

                buffermem = 0
                orecode = ""
                textout = ""

                for ex in str(textdata):  # SERIAL SEPARATOR LOOP <-------------------

                    if ex == "_":
                        buffermem = buffermem + 1

                    if buffermem == 1:
                        orecode += str(ex)

                    if buffermem == 4:
                        textout += ex

                if orecode == "":
                    throwmessage(
                        "LES", "ERROR : decode-serial-notfound", " TEXT IS NOT 'SSETG1' ")
                else:

                    orecode = orecode[1:]
                    orecode = "".join(reversed(orecode[1:]))

                    textout = textout[1:]

                    try:
                        serial = int(orecode) - len(textout)
                    except TypeError:
                        throwmessage(
                            "LES", "ERROR : Opration-Decode-serial-False", " EDITED SERIAL FOUND ")
                    else:

                        if serial == int(inpkey):

                            shiftvar = "".join(reversed(str(inpkey)))
                            # MAIN DECODING LOOP *****************
                            for shiftvalue in str(shiftvar):
                                # print(" ")

                                elements = textout
                                textout = ""

                                for char1 in elements:
                                    if char1 in gauge:
                                        pos = gauge.index(char1)
                                        n_pos = pos - int(shiftvalue)
                                        textout += gauge[int(n_pos)]
                                        # print("decode n_pos ", n_pos)
                                    else:
                                        textout += nfound

                            throwmessage("notify", "Decode done",
                                         f"{inpkey} key is used")
                            decoding = True
                        else:
                            throwmessage(
                                "warning", "KEY WAS NOT MATCH", f"{inpkey} key is false")
                            textout = f"{inpkey} is a false key for entered text"
            else:
                textout = "DECODE IS NOT DONE"

        case _:
            throwmessage("LES", "ERROR : LES-operation-case-_",
                         " OPERATION MODE NOT MATCH ")


def selection(a):
    match a:
        case 1:
            text1 = input("enter the text for ENCODE : ")
            keys = input("enter the key ")
            operation("encode", keys, text1)
            print("encoded text is :- ", textout[7:])
        case 2:
            text1 = input("enter the text for DECODE : ")
            if text1[0:7] != "SSETG1_":
                text1 = "SSETG1_" + text1
            keys = input("enter the key ")
            operation("decode", keys, text1)
            print("decoded text is :- ", textout)
        case _:
            print(f" {a} option not match ")


print("SSETG1 ENCODE DECODE :-")

for i in range(3):

    option = int(input(
        "---------------------------\n1 ENCODE \n2 DECODE \n3 EXIT \n enter option :: "))
    if option == 3:
        break
    selection(option)
