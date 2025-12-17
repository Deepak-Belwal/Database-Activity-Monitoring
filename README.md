# Database-Activity-Monitoring
A simple database activity monitoring system that lets you check over the monitor-logins and the operations performed over the users table in a database (dam_db)

# Prerequisites
Before using the code, make sure that you have mysql and python installed in your system. 

# Steps to execute
1. Open the project folder in terminal and run the command --> python app.py [This is to run the backend]
2. Open the Link provided in the terminal ( http://127.0.0.1:5000/ ) and follow the login.
3. Monitor the system and check the system after any changes are made.
<h3>-Copy & Paste the following code for testing:</h3><br>
         INSERT INTO users VALUES (2,"Ram","ramesh@gmail.com");<br>
         UPDATE users SET username = "Ramesh" WHERE user_id = 2;<br>
         DELETE FROM users WHERE user_id = 2;<br>
         SELECT * FROM activity_log;

# Screenshots

<h1>A SIMPLE LOGIN PAGE:</h1>
<img width="1865" height="902" alt="image" src="https://github.com/user-attachments/assets/4c9163ef-2b47-400e-89b5-ba9cf84b7b36" />


<h1>A SIMPLE MONITOR WINDOW:</h1>
<img width="1862" height="904" alt="image" src="https://github.com/user-attachments/assets/af2deb83-ae51-49f3-9f0b-1e938393839d" />


# THANK YOU FOR THE VISIT :)
