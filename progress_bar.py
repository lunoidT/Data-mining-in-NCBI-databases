def progress_bar(current, max_len,bar_len=30):
    """ Progress bar for combinations function """
    bar_prog = int((current/max_len)*bar_len)
    progress_text = "█" * bar_prog
    rest_text = "-" * (bar_len - bar_prog)
    print(f"\rProgress: [{progress_text}{rest_text}]",end="")
