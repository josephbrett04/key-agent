logging_active = False

def toggle_logging():

    global logging_active
    logging_active = not logging_active

    if logging_active:
        print("Now logging pc strokes")
    else:
        print("Logging stopped")
