import keyboard

try:
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            print(f"Scan code: {event.scan_code}, Name: {event.name}")
except KeyboardInterrupt:
    pass