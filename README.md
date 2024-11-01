# SimRaceTelemetry

## Games supported:

**F12020**

**Checkout the HTML files, the screenshots attached below are from the same files, plus these graphs are interactive, play with it as much as you want**

Welcome to the ultimate pit stop for data-driven F1 enthusiasts! This project dives deep into the telemetry data of Formula 1 races, capturing and visualizing essential metrics to enhance our understanding of the track dynamics. It’s like having your own telemetry engineer, minus the tire changes(for now)! In short, be your own Race Engineer

>**<h2>FUTURE UPDATES SCOPE</h2>**

> - *Track movements GPS*

> - *Live ERS harvesting and deployment*

> - *Real-Time comparison with your rival*

> - *More Games F1, GT, iRacing, Automobilista etc..(I don't have those right now)*

> - *Tyre usage and strategy*

> - *And many more...*

<h2>⚙️ Project Overview</h2>

Using Python and socket programming, this script listens to real-time UDP packets emitted by the F1 2020 game, allowing you to collect telemetry data from multiple drivers. Think of it as your digital pit crew, gathering vital stats like speed, gear, engine RPM, tire temperatures, and more, all while you focus on mastering those apex corners.

<h2>📊 Key Features:</h2>

 - Real-Time Data Capture: Harnessing the power of UDP to capture live telemetry data directly from the game, giving you immediate insights into driver performance.
 - Dynamic Visualization: Leveraging Plotly to create interactive graphs and dashboards, visualizing critical metrics such as:
 - Speed (km/h)
 - Gear Selection
 - Engine RPM
 - Brake and Tire Temperatures
 - Tire Pressures
 - Comprehensive Data Structure: Organizing telemetry data into easy-to-access dictionaries for quick analysis and plotting, making it a breeze to track driver performance throughout the session.

<h2>🔧 Technical Highlights:</h2>

 - Data Handling: Implemented functions to unpack UDP packets and categorize telemetry data, ensuring efficient processing of incoming data streams.
 - Driver Management: Created a robust driver management system that dynamically updates stats based on current session data, allowing for seamless integration of telemetry for multiple participants.
 - Session Tracking: Captured vital session details, such as air temperature and safety car status, providing context for the telemetry data.

<h2>🚀 Getting Started:</h2>

1. Clone the repository
> https://github.com/gaurav16-byte/SimRaceTelemetry.git
2. Install the required libraries
> pip install plotly, pandas, f1_2020_telemetry
3. Set the folder variable to your prefered location (default is D drive, data folder)
> folder = "D:\\data\\"
4. Run the script and hop into your simrig, FOCUS!, you'll enjoy the data if it's good.

<h2>🎮 Acknowledgments:</h2>
This project was inspired by the competitive spirit of Formula 1 racing and the passion for data analytics. Whether you're racing against friends or just looking to refine your skills, this tool is designed to help you understand the nuances of F1 telemetry.
Join the race, analyze the data, and push your limits!

<h2>🖼️ Screenshots</h2>

In this case I am Bottas, track is Abu Dhabi

![{04122005-3729-4465-8ACA-B663F1D19F22}](https://github.com/user-attachments/assets/5619ee23-c49b-42ca-a53c-32cd508bce3a)

Lap times throughout race, there is some issue in here which is being fixed!

![{C3EB5493-B5FE-41B3-A627-948C2DCA9202}](https://github.com/user-attachments/assets/15dbb2d0-7a2b-4f4a-8778-f8e756fa15a2)

Telemetry Data

![{BB180C9C-9D90-4E70-B41A-06C96AC1F0EE}](https://github.com/user-attachments/assets/bda954c4-9a1f-40f3-8279-a4031e555971)

Brake Temparatures

![{0BD3814C-F86E-45F5-BFCA-1C3175C0136B}](https://github.com/user-attachments/assets/958981d4-5f51-4d90-95c4-6491992cac9f)

Inner Tyre Temps

![{55715C0E-439F-40C8-BB7E-1B822C48AB8E}](https://github.com/user-attachments/assets/9e30f50c-e24f-42a8-b41d-bf99e50a4223)

Outer Tyre Temps (Carcass)

![{2174C528-B580-47B8-BBBA-00E591757ACD}](https://github.com/user-attachments/assets/168c6261-ad5b-49b1-ba3f-9d5a7bb1165b)

Tyre pressures throughout the race

![{6670FAAB-9440-4598-8CFC-88D43C67491E}](https://github.com/user-attachments/assets/504397e7-71ec-4ce0-836d-81391ed49cc9)

Position Changes (Yes, Yas Marina is dull!)

![{0D999918-3432-4237-B71E-C2DE9027C071}](https://github.com/user-attachments/assets/36e7dfc9-a97d-448e-a031-b584cef26439)

Temparatures and Safety Car Status





