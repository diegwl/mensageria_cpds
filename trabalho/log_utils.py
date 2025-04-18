def log_event(filename, event):
    with open(filename, 'a') as f:
        f.write(event + '\n')
