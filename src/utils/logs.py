from datetime import datetime


def logs(req, status, message=None):

    now = datetime.now()
    formatted_date_time = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("./static/logs.txt", mode="a") as logs_file:

        if message is not None:
            content = f"{formatted_date_time} - {req} '{message}' {status}\n"
        else:
            content = f"{formatted_date_time} - {req} {status}\n"

        logs_file.write(content)
