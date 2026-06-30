# MISSION OVERVIEW
You must break out of the harness parsing loops and use a fallback strategy to install the client and write the script. Execute these steps sequentially.

## STEP 1: Install
Run this command:
`python3 -m pip install --user gradio_client`

## STEP 2: Write Script Safely
Execute this exact Python command to write the file using base64 (this bypasses all quote/parentheses shell errors):
`python3 -c "import base64; code = base64.b64decode('aW1wb3J0IHN5cwpmcm9tIGdyYWRpb19jbGllbnQgaW1wb3J0IENsaWVudAoKZGVmIHJ1bl9waXBlbGluZShmaWxlX3BhdGgpOgogICAgdHJ5OgogICAgICAgIHdpdGggb3BlbihmaWxlX3BhdGgsICJyIikgYXMgZjoKICAgICAgICAgICAgdHJhbnNjcmlwdCA9IGYucmVhZCgpCiAgICAgICAgcHJpbnQoIkNvbm5lY3RpbmcgdG8gTmV4aUNsYXcuLi4iKQogICAgICAgIGNsaWVudCA9IENsaWVudCgiTWFsaWs0MzQvTmV4aUNsYXciKQogICAgICAgIHJlc3VsdCA9IGNsaWVudC5wcmVkaWN0KHRyYW5zY3JpcHRfdGV4dD10cmFuc2NyaXB0LCBnbG9iYWxfY29udGV4dD0iQXV0b25vbW91cyBPbWVnYUNsYXcgUGFzcyIsIGFwaV9uYW1lPSIvcHJlZGljdCIpCiAgICAgICAgdGFyZ2V0ID0gIi90bXAvYXRvbXNwYWNlLm1ldHRhIgogICAgICAgIHdpdGggb3Blbih0YXJnZXQsICJhIikgYXMgZl9vdXQ6CiAgICAgICAgICAgIGZfb3V0LndyaXRlKCJcblxuOyAtLS0gQXV0b25vbW91cyBOZXhpQ2xhdyBJbmdlc3Rpb24gLS0tXG4iICsgcmVzdWx0WzFdICsgIlxuIikKICAgICAgICBwcmludCgiU3VjY2VzcyEiKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHByaW50KCJFcnJvcjogIiArIHN0cihlKSkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICAgcnVuX3BpcGVsaW5lKHN5cy5hcmd2WzFdKQ==').decode('utf-8'); f = open('/tmp/nexiclaw_client.py', 'w'); f.write(code); f.close()"`

## STEP 3: Execute
Run the script against the transcript:
`python3 /tmp/nexiclaw_client.py interview.text`

Report back the exact console output of Step 2 and Step 3.