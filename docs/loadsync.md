# LoadSync(tm) Guide

LoadSync(tm) is the building management software for your loadcenter. For hardware setup and UPS connections, see the [Loadcenter Guide](initial-setup.md#loadsynctm-setup).

LoadSync(tm) can be accessed remotely with the remote access web UI.  Please [contact us](contact.md) for the login.

## Navigation

The LoadSync(tm) interface uses a sidebar on the right side of the screen for navigating between pages.
The available pages depend on your loadcenter's hardware configuration.

!!! tip "Variable pages"

    LoadSync(tm) automatically selects which pages to display based on what type of unit you have.
    
    By default, the following pages will display:

    - [x] Home
    - [x] Miners
    - [x] Graphs
    - [x] Alarms
    - [x] Help

    Depending on what devices are communicating with LoadSync(tm), the follow pages may also appear:

    - [ ] Climate
    - [ ] Power
    - [ ] Engine
    - [ ] Market Sync

    !!! question "Missing pages/devices"
        
        If LoadSync(tm)  is having trouble communicating with a device, it may be missing some pages.
        Sometimes this can be rectified by running rediscovery, located on the `Help` page under `Advanced`.
    

## Home

The home page provides a quick overview of your loadcenter's status, organized into tabs:

<div class="grid cards" markdown>

-   :lucide-thermometer:{ .lg .middle } __Climate__

    ---

    - Fan status
    - Fan speed
    - Building temperature
    - Louver state
    
    ![Home page - Climate tab](images/loadsync-home-climate.png){ .fix-png }
    /// caption
    Climate tab
    ///

-   :lucide-zap:{ .lg .middle } __Power__

    ---

    - 3-phase amperage
    - Voltage
    - Kilowatt readings

    ![Home page - Power tab](images/loadsync-home-power.png){ .fix-png }
    /// caption
    Power tab
    ///

-   :lucide-cog:{ .lg .middle } __Engine__ *Hash Generator only*

    ---

    - RPM
    - Temperature
    - Oil Pressure
    - Gas Pressure
    - Battery Voltage
    
    ![Home page - Engine tab](images/loadsync-home-engine.png){ .fix-png }
    /// caption
    Engine tab
    ///
    

</div>

## Miners

The miners page displays a fleet overview of all discovered miners in a table with the following columns: 

- IP Address
- Hashrate
- Temperature
- Wattage
- Efficiency

![Miners fleet view](images/loadsync-miners.png){ .fix-png width="50%" }
/// caption
Miners page
///

### Scanning for Miners

To discover miners on the network, click the **Re-Scan Miners** button at the top of the page. LoadSync(tm) will scan the local network and populate the table with any miners it finds.

!!! note
    LoadSync(tm) automatically searches for miners on startup, so this may not even be required unless there are miners missing from the list.

### Individual Miner Controls

!!! tip "Miner Details"
    Clicking on a miner's IP address in the fleet table opens a detailed view with the tabs described below.

=== "Basic"

    Displays real-time miner metrics:

    <div class="grid cards" markdown>

    -   :lucide-hash:{ .lg .middle } __Hashrate__

        ---

        Current mining speed

    -   :lucide-thermometer:{ .lg .middle } __Board Temperatures__

        ---

        Temperature readings per hashboard

    -   :lucide-zap:{ .lg .middle } __Wattage__

        ---

        Current power consumption

    -   :lucide-gauge:{ .lg .middle } __Efficiency__

        ---

        Watts per terahash (W/TH)

    -   :lucide-clock:{ .lg .middle } __Uptime__

        ---

        Time since last restart

    </div>

    ![Miner detail - Basic tab](images/loadsync-miner-basic.png){ .fix-png width="50%" }
    /// caption
    Miner basic tab
    ///
    
=== "Settings"

    Provides controls for the miner:

    <div class="grid cards" markdown>

    -   :lucide-zap:{ .lg .middle } __Power Limit__

        ---

        Adjust the wattage limit

    -   :lucide-power:{ .lg .middle } __Enable/Disable Mining__

        ---

        Toggle mining on or off

    -   :lucide-lightbulb:{ .lg .middle } __Fault Light__

        ---

        Toggle the miner's fault indicator LED

    -   :lucide-refresh-cw:{ .lg .middle } __Reboot__

        ---

        Restart the miner

    </div>

    ![Miner detail - Settings tab](images/loadsync-miner-settings.png){ .fix-png width="50%" }
    /// caption
    Miner settings tab
    ///
    
=== "Advanced"

    Shows additional diagnostic data for the miner.

## Climate

The climate page monitors and controls the loadcenter's ventilation system. It is organized into tabs:

=== "Basic"

    Displays current climate readings:

    <div class="grid cards" markdown>

    -   :lucide-power:{ .lg .middle } __Fan Status__

        ---

        Whether the fan system is running

    -   :lucide-gauge:{ .lg .middle } __Fan Speed__

        ---

        Current speed as a percentage (0–100%)

    -   :lucide-thermometer:{ .lg .middle } __Building Temperature__

        ---

        Current internal temperature

    -   :lucide-droplets:{ .lg .middle } __Building Humidity__

        ---

        Current internal humidity

    -   :lucide-blinds:{ .lg .middle } __Louver State__

        ---

        Whether the building louvers are open or closed

    </div>

    ![Climate - Basic tab](images/loadsync-climate-basic.png){ .fix-png width="50%" }
    /// caption
    Climate basic tab
    ///
    
=== "Settings"

    Provides controls for the fan system:

    <div class="grid cards" markdown>

    -   :lucide-power:{ .lg .middle } __Fan Enabled__

        ---

        Turn the fan system on or off

    -   :lucide-bot:{ .lg .middle } __Fan Auto__

        ---

        Toggle automatic temperature-based fan control

    -   :lucide-gauge:{ .lg .middle } __Min. Speed__

        ---

        Set the minimum fan speed (0–100%)

    -   :lucide-thermometer:{ .lg .middle } __Target Temp.__

        ---

        Set the target temperature for auto mode

    </div>

    !!! tip "Auto Mode Behavior"
        When auto mode is enabled, the fans will automatically adjust speed to maintain the target temperature. When disabled, fans run at the minimum speed setting.

    ![Climate - Settings tab](images/loadsync-climate-settings.png){ .fix-png width="50%" }
    /// caption
    Climate settings tab
    ///
    
## Power

The power page monitors the loadcenter's power distribution units (PDUs) and electrical output.

=== "Basic"

    Displays per-phase power data:

    <div class="grid cards" markdown>

    -   :lucide-activity:{ .lg .middle } __Amperage__

        ---

        Current draw per phase

    -   :lucide-zap:{ .lg .middle } __Voltage__

        ---

        Voltage per phase

    -   :lucide-bolt:{ .lg .middle } __Kilowatts__

        ---

        Power output per phase

    </div>

    ![Power - Basic tab](images/loadsync-power-basic.png){ .fix-png width="50%" }
    /// caption
    Power basic tab
    ///
    
=== "PDUs"

    Lists all connected PDUs with their status.

    !!! tip "PDU Details"
        Clicking on an individual PDU shows detailed port-level information including per-phase amperage, voltage, and kilowatt readings.

    ![Power - PDU list](images/loadsync-power-pdus.png){ .fix-png width="50%" }
    /// caption
    PDU list
    ///
    
    ![Individual PDU detail](images/loadsync-pdu-detail.png){ .fix-png width="50%" }
    /// caption
    PDU details
    ///
    
## Engine

!!! info
    The engine page is only available on loadcenters equipped with an engine/generator.

The engine page monitors and controls the loadcenter's generator. It is organized into tabs:

=== "Basic"

    Displays real-time engine metrics:

    <div class="grid cards" markdown>

    -   :lucide-gauge:{ .lg .middle } __RPM__

        ---

        Current engine speed

    -   :lucide-thermometer:{ .lg .middle } __Temperature__

        ---

        Engine temperature

    -   :lucide-droplet:{ .lg .middle } __Oil Pressure__

        ---

        Current oil pressure

    -   :lucide-flame:{ .lg .middle } __Gas Pressure__

        ---

        Current gas pressure

    -   :lucide-battery:{ .lg .middle } __Battery Voltage__

        ---

        Engine battery voltage

    -   :lucide-zap:{ .lg .middle } __Phase Data__

        ---

        Per-phase voltage, amperage, and kilowatt output

    </div>

    ![Engine - Basic tab](images/loadsync-engine-basic.png){ .fix-png width="50%" }
    /// caption
    Engine basic tab
    ///
    
=== "Settings"

    Provides engine controls:

    <div class="grid cards" markdown>

    -   :lucide-octagon:{ .lg .middle } __ESD (Emergency Shutdown)__

        ---

        Opens a confirmation dialog to shut down the engine

    -   :lucide-flame:{ .lg .middle } __Minimum Gas Pressure Alert__

        ---

        Set the threshold for low gas pressure alarms

    -   :lucide-thermometer:{ .lg .middle } __High Temp. Alert__

        ---

        Set the threshold for high temperature alarms

    -   :lucide-scale:{ .lg .middle } __Auto Balance__

        ---

        When enabled, automatically distributes power across miners based on engine load

    </div>

    ![Engine - Settings tab](images/loadsync-engine-settings.png){ .fix-png width="50%" }
    /// caption
    Engine settings tab
    ///
    
    !!! danger "Emergency Shutdown"
        The ESD button will immediately shut down the engine. You will be prompted to confirm before the shutdown is executed.

## Graphs

The graphs page displays historical data charts for your loadcenter's systems. The available graph categories depend on your hardware configuration and may include **Engine**, **Power**, and **Climate**.

!!! tip "Chart timeframes"
    Each chart supports multiple timeframe selections:

    - 1 hour
    - 6 hours
    - 1 day
    - 1 week
    - 1 month

![Graphs page](images/loadsync-graphs.png){ .fix-png width="50%" }
/// caption
Graphs page
///

### Engine Graphs

Displays historical charts for RPM, temperature, oil pressure, gas pressure, battery voltage, and per-phase amperage. Alarm events are highlighted on the charts as colored overlays.

### Power Graphs

Displays historical charts for PDU amperage, voltage, and kilowatt readings. High-amperage alarm events are highlighted on the charts.

### Climate Graphs

Displays historical charts for fan speed, building temperature, and building humidity.

## Alarms

The alarms page tracks system alerts and is organized into tabs:

=== "Basic"

    Shows all currently active alarms with descriptions and icons.

=== "History"

    Shows a log of past alarms with timestamps, allowing you to review when issues occurred.

    ![Alarms - History tab](images/loadsync-alarms-history.png){ .fix-png width="50%" }
    /// caption
    Alarm history tab
    ///
    
=== "Callouts"

    Configures external alarm notifications via [ntfy.sh](https://ntfy.sh). When enabled, alarm events will be pushed as notifications to your device.

Alarm types include:

- **Engine alarms** — RPM, temperature, oil pressure, battery voltage, gas pressure
- **Power alarms** — High amperage on PDUs

## Market Sync

!!! info
    Market Sync is only available on loadcenters connected to the ERCOT power grid.

Market Sync allows LoadSync(tm) to automatically respond to real-time electricity pricing from ERCOT (Electric Reliability Council of Texas). When the price exceeds your configured limit, LoadSync(tm) will automatically pause mining operations and resume them when prices drop back down.

=== "Basic"

    Displays the current market price and sync status.

    ![Market Sync - Basic tab](images/loadsync-sync-basic.png){ .fix-png width="50%" }
    /// caption
    Market sync basic tab
    ///
    
=== "Settings"

    Provides configuration options:

    <div class="grid cards" markdown>

    -   :lucide-dollar-sign:{ .lg .middle } __Price Limit__

        ---

        Set the price threshold (in $/MWh) at which mining should be paused

    -   :lucide-timer:{ .lg .middle } __Sleep Time__

        ---

        Duration (in seconds) to maintain the current state after a price change; set to 0 to disable

    -   :lucide-scale:{ .lg .middle } __Auto Balance__

        ---

        Enable or disable automatic market sync response

    -   :lucide-map-pin:{ .lg .middle } __Region__

        ---

        Select your ERCOT pricing region from the dropdown

    </div>

    Available ERCOT regions:

    | Hub Regions   | Load Zone Regions |
    |---------------|-------------------|
    | HB_BUSAVG     | LZ_AEN            |
    | HB_HOUSTON    | LZ_CPS            |
    | HB_HUBAVG     | LZ_HOUSTON        |
    | HB_NORTH      | LZ_LCRA           |
    | HB_PAN        | LZ_NORTH          |
    | HB_SOUTH      | LZ_RAYBN          |
    | HB_WEST       | LZ_SOUTH          |
    |               | LZ_WEST           |

    ![Market Sync - Settings tab](images/loadsync-sync-settings.png){ .fix-png width="50%" }
    /// caption
    Market sync settings tab
    ///
    
## Help

The help page provides network information and setup tools, organized into tabs:

=== "Network"

    Displays the loadcenter's current network configuration including IP address and connection details.

=== "Tailscale"

    Provides Tailscale VPN setup with a scannable QR code for quick authentication.

    !!! tip "Full Setup Guide"
        See [Tailscale Remote Access](#tailscale-remote-access) below for a detailed walkthrough.

## Tailscale Remote Access

Tailscale allows for secure, remote access to any miners on a LoadSync(tm) accessible subnet.

### Prerequisites

1. Visit [tailscale.com/docs/install](https://tailscale.com/docs/install) to download and install the Tailscale client on your computer or mobile device.
2. Sign up for a Tailscale account if you don't have one.

### Setup

!!! tip "Connecting Tailscale"
    1. On the LoadSync interface, navigate to the **Help Page** and select the **Tailscale** tab.
    2. If you do not see a Login QR code, click the **New Login** button to generate one.
    3. Scan the QR code with your smartphone and log in using your Tailscale account.
    4. Once authenticated, press the **Connect** button on your smartphone device.

### Verification

After connecting, the **Tailscale State** should display as "Running" and your account email will appear in the **Profile** dropdown.

You may need to enable the routes on the Tailscale web admin panel.
To enable them, click the `...` dropdown next to a unit, select `Edit route settings...`, and ensure the route is enabled under `Subnet routes`.

!!! info "More Information"
    For a detailed walkthrough, see the [Tailscale Quickstart Guide](https://tailscale.com/docs/how-to/quickstart).

## Fleet Manager

*Coming soon.*