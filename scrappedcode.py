 # this is for code that I scrapped but still want to reference for later ~ thallia


        arg1 = messageargs[1].strip()
        try:
            arg2 = messageargs[2].strip()
        except Exception:
            arg2 = None
        try:
            arg3 = messageargs[3].strip()
        except Exception:
            arg3 = None

        print("before: " + str(arg1))
        print("before: " + str(arg2))
        print("before: " + str(arg3))

        if before_rotate == 0:
            try:
                rotate = int(arg1)
            except:
                pass
            try:
                rotate = int(arg2)
            except:
                pass
            try:
                rotate = int(arg3)
            except:
                pass

        print("rotate(with int args) " + str(rotate))

        try:
            #if type(arg1) is int:
            #   rotate = arg1
            if type(arg1) is str:
                if arg1 in users:
                    messages_from = arg1
                else:
                    title = arg1
            #if type(arg2) is int:
             #   rotate = arg2
            if type(arg2) is str:
                if arg2 in users:
                    messages_from = arg2
                else:
                    title = arg2
            #if type(arg3) is int:
             #   rotate = arg3
            if arg3 != None:
                if type(arg3) is str:
                    if arg3 in users:
                        messages_from = arg3
                    else:
                        title = arg3
        except Exception:
            pass

        #if messages_from != none:
            # needs to register if a username was provided, cycle through and only pick out those user messages

        if title == None:
            title = "messages"
        try:
            int(title)
        except:
            title = "messages"
        if rotate == 0:
             rotate = 1
        i = rotate

        print("argument 1: " + str(arg1))
        print("argument 2: " + str(arg2))
        print("argument 3: " + str(arg3))

        print("rotate: " + str(rotate))
        print("messages_from: " + str(messages_from))
        print("title: " + str(title))
