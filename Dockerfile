FROM selenium/standalone-chrome 

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium

WORKDIR /app

RUN pip install linkedin-jobs-scraper

CMD LI_AT_COOKIE=AQEDAU2IgMABa75YAAABjs_7l7QAAAGO9AgbtFYAZUw9PVIXGWSmn4tBhdq4yFVZk7QZNUUOUVVECKr3cImlqFH6JhxEoeTIRvFcWPwOmDk6vmsry6afAUD8vl4O8lpWU8fbCcPW6T7WNHRnrMx7KdAn python3 main.py