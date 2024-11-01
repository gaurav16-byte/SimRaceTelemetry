from f1_2020_telemetry.packets import unpack_udp_packet
import socket
import plotly.graph_objects as go
from plotly.subplots import make_subplots

folder = "D:\\data\\"
timestamps = []
airtemp, tracktemp, sc, drivers = [], [], [], []
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind(("", 20777))

def car_telemetry(packet, drives):  #ADD DRIVER VALUES TO DICTIONARIES, CHANGE LATER
    drivers = list(drives.keys())
    values = list(drives.values())
    for i in range(len(drivers)):
        values[i][0].append(packet.carTelemetryData[i].speed)
        values[i][1].append(packet.carTelemetryData[i].gear)
        values[i][2].append(packet.carTelemetryData[i].engineRPM)
        values[i][3].append(packet.carTelemetryData[i].engineTemperature)
        values[i][4][0].append(packet.carTelemetryData[i].brakesTemperature[0])
        values[i][4][1].append(packet.carTelemetryData[i].brakesTemperature[1])
        values[i][4][2].append(packet.carTelemetryData[i].brakesTemperature[2])
        values[i][4][3].append(packet.carTelemetryData[i].brakesTemperature[3])
        values[i][5][0].append(packet.carTelemetryData[i].tyresSurfaceTemperature[0])
        values[i][5][1].append(packet.carTelemetryData[i].tyresSurfaceTemperature[1])
        values[i][5][2].append(packet.carTelemetryData[i].tyresSurfaceTemperature[2])
        values[i][5][3].append(packet.carTelemetryData[i].tyresSurfaceTemperature[3])
        values[i][6][0].append(packet.carTelemetryData[i].tyresInnerTemperature[0])
        values[i][6][1].append(packet.carTelemetryData[i].tyresInnerTemperature[1])
        values[i][6][2].append(packet.carTelemetryData[i].tyresInnerTemperature[2])
        values[i][6][3].append(packet.carTelemetryData[i].tyresInnerTemperature[3])
        values[i][7][0].append(packet.carTelemetryData[i].tyresPressure[0])
        values[i][7][1].append(packet.carTelemetryData[i].tyresPressure[1])
        values[i][7][2].append(packet.carTelemetryData[i].tyresPressure[2])
        values[i][7][3].append(packet.carTelemetryData[i].tyresPressure[3])
    
    return dict(zip(drivers, values))

def session_details(packet):
    global airtemp, tracktemp, sc
    #pitspeed = packet.pitSpeedLimit
    #tracklen = packet.trackLength
    #laps = packet.totalLaps
    #stype = packet.sessionType  #DOCS DICTIONARY
    #track = packet.trackId  #DOCS DICTIONARY
    #weather = packet.weather
    airtemp.append(packet.airTemperature)
    tracktemp.append(packet.trackTemperature)
    sc.append(packet.safetyCarStatus)
    #return pitspeed, tracklen, laps, stype, track, weather

def participants(packet, active):
    global drivers
    placeholders = []
    places = []
    times = []
    ers = []
    
    if len(drivers) == 0:
        for i in range(active):
            drivers.append(packet.participants[i].name.decode('utf-8')[:3])
            placeholders.append([[], [], [], [], [[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]])
            places.append({})
            times.append({})
            ers.append({1:[0, 0, 0]})
    
    return dict(zip(drivers, placeholders)), dict(zip(drivers, places)), dict(zip(drivers, times)), dict(zip(drivers, ers))

def lapsdata(packet, forlaps):
    drivers = list(forlaps.keys())
    pos = list(forlaps.values())
    for i in range(len(drivers)):
        currentLap = packet.lapData[i].currentLapNum
        position = packet.lapData[i].carPosition
        if currentLap == 1:
            pos[i][1] = position
        if currentLap not in pos[i]:
            pos[i][currentLap] = position
        if currentLap in pos[i] and (pos[i][currentLap] > position or pos[i][currentLap] < position) and currentLap != 1:
            pos[i][currentLap] = position
    
    return dict(zip(drivers, pos))

def timesdata(packet, fortimes):
    drivers = list(fortimes.keys())
    times = list(fortimes.values())
    for i in range(len(drivers)):
        currentLap = packet.lapData[i].currentLapNum
        currentTime = packet.lapData[i].currentLapTime
        if currentLap not in times[i]:
            times[i][currentLap] = currentTime
        if currentLap in times[i]:
            if currentTime > times[i][currentLap]:
                times[i][currentLap] = currentTime
    
    return dict(zip(drivers, times))

def ersdata(packet, forers):
    drivers = list(forers.keys())
    erss = list(forers.values())
    for i in range(len(drivers)):
        hark = packet.carStatusData[i].ersHarvestedThisLapMGUK
        harh = packet.carStatusData[i].ersHarvestedThisLapMGUH
        deployed = packet.carStatusData[i].ersDeployedThisLap
        lap = max(erss[i].keys())
        if hark > erss[i][lap][0] or harh > erss[i][lap][1] or deployed > erss[i][lap][2]:
            erss[i][lap] = [hark, harh, deployed]
        if hark < erss[i][lap][0] or harh < erss[i][lap][1] or deployed < erss[i][lap][2]:
            lap += 1            
            erss[i][lap] = [hark, harh, deployed]

    return dict(zip(drivers, erss))

while True:
    udp_packet = udp_socket.recv(2048)
    packet = unpack_udp_packet(udp_packet)
    if packet.header.packetId == 3:
        if b'SEND' in packet.eventStringCode:
            break
    
    if packet.header.packetId == 1:
        session_details(packet)
        if packet.header.sessionTime not in timestamps:
            timestamps.append(packet.header.sessionTime)
    
    if packet.header.packetId == 4:
        active = packet.numActiveCars
        if len(drivers) == 0:
            drives, forlaps, fortimes, forers = participants(packet, active)
    
    if packet.header.packetId == 2:
        if packet.header.sessionTime not in timestamps:
            timestamps.append(packet.header.sessionTime)
        forlaps = lapsdata(packet, forlaps)
        fortimes = timesdata(packet, fortimes)

    if packet.header.packetId == 6:
        drives = car_telemetry(packet, drives)
        if packet.header.sessionTime not in timestamps:
            timestamps.append(packet.header.sessionTime)
    
    if packet.header.packetId == 7:
        if packet.header.sessionTime not in timestamps:
            timestamps.append(packet.header.sessionTime)
        forers = ersdata(packet, forers)

def plot_telemetry(drives):
    drivers = list(drives.keys())
    values = list(drives.values())
    for i in range(len(drivers)):
        fig_main = make_subplots(rows=4, cols=1, subplot_titles=("Speed", "Gear", "Engine RPM", "Engine Temperature"))
        fig_main.add_trace(go.Scatter(y=values[i][0], mode='lines', name='Speed (km/h)', line=dict(color='blue')), row=1, col=1)
        fig_main.add_trace(go.Scatter(y=values[i][1], mode='lines', name='Gear', line=dict(color='green')), row=2, col=1)
        fig_main.add_trace(go.Scatter(y=values[i][2], mode='lines', name='Engine RPM', line=dict(color='red')), row=3, col=1)
        fig_main.add_trace(go.Scatter(y=values[i][3], mode='lines', name='Engine Temperature (°C)', line=dict(color='purple')), row=4, col=1)
        fig_main.update_layout(title_text="Main Telemetry Data", height=800)
        fig_main.write_html(f"{folder}{drivers[i]} Telemetry.html")
        
        fig_brakes = make_subplots(rows=2, cols=2, subplot_titles=("Rear Left Brake", "Rear Right Brake", "Front Left Brake", "Front Right Brake"))
        fig_brakes.add_trace(go.Scatter(y=values[i][4][0], mode='lines', name='Rear Left Brake', line=dict(color='orange')), row=1, col=1)
        fig_brakes.add_trace(go.Scatter(y=values[i][4][1], mode='lines', name='Rear Right Brake', line=dict(color='yellow')), row=1, col=2)
        fig_brakes.add_trace(go.Scatter(y=values[i][4][2], mode='lines', name='Front Left Brake', line=dict(color='pink')), row=2, col=1)
        fig_brakes.add_trace(go.Scatter(y=values[i][4][3], mode='lines', name='Front Right Brake', line=dict(color='cyan')), row=2, col=2)
        fig_brakes.update_layout(title_text="Brake Temperatures", height=600)
        fig_brakes.write_html(f"{folder}{drivers[i]} Brakes.html")

        fig_outer_temps = make_subplots(rows=2, cols=2, subplot_titles=("Rear Left Outer Temp", "Rear Right Outer Temp", "Front Left Outer Temp", "Front Right Outer Temp"))
        fig_outer_temps.add_trace(go.Scatter(y=values[i][5][0], mode='lines', name='RL Outer Temp', line=dict(color='orange')), row=1, col=1)
        fig_outer_temps.add_trace(go.Scatter(y=values[i][5][1], mode='lines', name='RR Outer Temp', line=dict(color='yellow')), row=1, col=2)
        fig_outer_temps.add_trace(go.Scatter(y=values[i][5][2], mode='lines', name='FL Outer Temp', line=dict(color='pink')), row=2, col=1)
        fig_outer_temps.add_trace(go.Scatter(y=values[i][5][3], mode='lines', name='FR Outer Temp', line=dict(color='cyan')), row=2, col=2)
        fig_outer_temps.update_layout(title_text="Outer Tire Temperatures", height=600)
        fig_outer_temps.write_html(f"{folder}{drivers[i]} Outer Tire Temps.html")

        fig_inner_temps = make_subplots(rows=2, cols=2, subplot_titles=("Rear Left Inner Temp", "Rear Right Inner Temp", "Front Left Inner Temp", "Front Right Inner Temp"))
        fig_inner_temps.add_trace(go.Scatter(y=values[i][6][0], mode='lines', name='RL Inner Temp', line=dict(color='orange')), row=1, col=1)
        fig_inner_temps.add_trace(go.Scatter(y=values[i][6][1], mode='lines', name='RR Inner Temp', line=dict(color='yellow')), row=1, col=2)
        fig_inner_temps.add_trace(go.Scatter(y=values[i][6][2], mode='lines', name='FL Inner Temp', line=dict(color='pink')), row=2, col=1)
        fig_inner_temps.add_trace(go.Scatter(y=values[i][6][3], mode='lines', name='FR Inner Temp', line=dict(color='cyan')), row=2, col=2)
        fig_inner_temps.update_layout(title_text="Inner Tire Temperatures", height=600)
        fig_inner_temps.write_html(f"{folder}{drivers[i]} Inner Tire Temps.html")

        fig_tire_pressures = make_subplots(rows=2, cols=2, subplot_titles=("Rear Left Tire Pressure", "Rear Right Tire Pressure", "Front Left Tire Pressure", "Front Right Tire Pressure"))
        fig_tire_pressures.add_trace(go.Scatter(y=values[i][7][0], mode='lines', name='RL Pressure', line=dict(color='orange')), row=1, col=1)
        fig_tire_pressures.add_trace(go.Scatter(y=values[i][7][1], mode='lines', name='RR Pressure', line=dict(color='yellow')), row=1, col=2)
        fig_tire_pressures.add_trace(go.Scatter(y=values[i][7][2], mode='lines', name='FL Pressure', line=dict(color='pink')), row=2, col=1)
        fig_tire_pressures.add_trace(go.Scatter(y=values[i][7][3], mode='lines', name='FR Pressure', line=dict(color='cyan')), row=2, col=2)
        fig_tire_pressures.update_layout(title_text="Tire Pressures", height=600)
        fig_tire_pressures.write_html(f"{folder}{drivers[i]} Tire Pressures.html")
plot_telemetry(drives)

def plot_positions(forlaps):
    drivers = list(forlaps.keys())
    laps = list(list(forlaps.values())[0].keys())
    changes = []
    for i in range(len(drivers)):
        changes.append(list(list(forlaps.values())[i].values()))

    for i in changes:
        if len(i) < len(laps):
            last = i[-1]
            for j in range(len(laps) - len(i)):
                i.append(last)

    fig = go.Figure()
    for i, driver in enumerate(drivers):
        fig.add_trace(go.Scatter(
            x=laps,
            y=changes[i],
            mode='lines+markers',
            name=driver,
            line=dict(width=2)
        ))
        fig.add_annotation(
            x=laps[0] - 0.5, y=changes[i][0],
            text=f"{driver} ({changes[i][0]})",
            showarrow=False,
            font=dict(size=10),
            xanchor='right',
            yanchor='middle'
        )
        fig.add_annotation(
            x=laps[-1] + 0.5, y=changes[i][-1],
            text=f"{driver} ({changes[i][-1]})",
            showarrow=False,
            font=dict(size=10),
            xanchor='left',
            yanchor='middle'
        )
    fig.update_layout(
        title='Driver Position Changes Over Laps',
        xaxis=dict(title='Laps', tickmode='array', tickvals=laps),
        yaxis=dict(title='Position', autorange='reversed', tickmode='linear', tick0=1, dtick=1),
        showlegend=False,
        template='plotly_white',
        margin=dict(l=80, r=80, t=80, b=80)
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGray')
    fig.write_html(f"{folder}Position Changes.html")
plot_positions(forlaps)

def plot_weather(airtemp, tracktemp, sc):
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Air Temperature", "Track Temperature", "Safety Car Status"))
    fig.add_trace(go.Scatter(x=timestamps, y=airtemp, mode='lines', name='Air Temperature (°C)', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=timestamps, y=tracktemp, mode='lines', name='Track Temperature (°C)', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=timestamps, y=sc, mode='lines', name='Safety Car Status', line=dict(color='purple')), row=3, col=1)
    fig.update_layout(title="Session Details", height=800)
    fig.write_html(f"{folder}Temparatures.html")
plot_weather(airtemp, tracktemp, sc)

def plot_laptimes(fortimes):
    fig = go.Figure()
    drivers = list(fortimes.keys())
    for i in range(len(drivers)):
        laps = list(list(fortimes.values())[i].keys())
        times = list(list(fortimes.values())[i].values())
        fig.add_trace(go.Bar(
            x=laps,
            y=times,
            text=times,  # Optional: show times on each bar
            textposition='auto'
        ))

        fig.update_layout(
            title="Lap Times per Driver",
            xaxis=dict(title="Laps"),
            yaxis=dict(title="Lap Time (seconds)"),
            barmode='group',  # Align bars for each lap next to each other
            template='plotly_white'
        )
        fig.write_html(f"{folder}{drivers[i]} Lap Times.html")
plot_laptimes(fortimes)