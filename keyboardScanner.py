import keyboard
# this is a simple program seperate from the rest of the files, this returns the scancodes of the keys pressed down while it's running


try:
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            print(f"Scan code: {event.scan_code}, Name: {event.name}")
except KeyboardInterrupt:
    pass