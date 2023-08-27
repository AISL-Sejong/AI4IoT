def msgParsing(AIModelName, msg):

    if AIModelName == "humanDetection": 
        print(msg)
        count = msg.split(",")[1].replace(" ","").replace("heads","")
        if int(count) == 0:
            return (count+" person")

        elif int(count) > 0:
            return (count+" people")

    elif AIModelName == "visualLocalization": 
        print(msg)
        location = msg.split("**")[1].split(".")[0]
        return (location)
    
    elif AIModelName == "potholeDetection": 
        print(msg)
        count = msg.rstrip('\n')
        return (count + " pothole")

        
    elif AIModelName == "speedbumpDetection": 
        print(msg)
        count = msg.rstrip('\n')
        return (count + " speedbump")