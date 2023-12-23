#! /bin/bash

# Start the first Python script in the first folder in a new window
cd environment/frontend_server/ 
gnome-terminal -- python manage.py runserver

# Open the server verification on browser in Windows default browser
cmd.exe /C start http://localhost:8000/

# Move back to directory where we want to run the script
cd ../../

# Change directory 
cd reverie/backend_server

# Run simulation script in the background
python reverie.py 








