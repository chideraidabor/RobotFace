import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

#********* DYNAMIXEL Model definition *********
#***** (Use only one definition at a time) *****
MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430
# MY_DXL = 'MX_SERIES'    # MX series with 2.0 firmware update.
# MY_DXL = 'PRO_SERIES'   # H54, H42, M54, M42, L54, L42
# MY_DXL = 'PRO_A_SERIES' # PRO series with (A) firmware update.
# MY_DXL = 'P_SERIES'     # PH54, PH42, PM54
# MY_DXL = 'XL320'        # [WARNING] Operating Voltage : 7.4V


# Control table address
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_PRESENT_POSITION       = 132
    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
    BAUDRATE                    = 1000000

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      = 1

# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/tty.usbserial-FT583QN8'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Wave motor configuration
wave_motor = 13  # Motor ID for waving gesture
wave_positions = [2301, 1828]  # Positions for waving gesture
wave_cycles = 3  # Number of cycles for the wave gesture
wave_delay = 1  # Delay in seconds between each wave position


# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 11, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 11, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 11, ADDR_GOAL_POSITION, 797)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 12, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, ADDR_GOAL_POSITION, 2011)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 14, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 14, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 14, ADDR_GOAL_POSITION, 2253)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 16, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 16, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 16, ADDR_GOAL_POSITION, 2870)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 13, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, ADDR_GOAL_POSITION, 2593)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 15, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, ADDR_GOAL_POSITION, 3322)

# Wait for upward movement to complete (adjust delay as needed)
import time
time.sleep(3)  # Delay to allow the arm to rise completely

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 11, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 11, ADDR_GOAL_POSITION, 1942)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 12, ADDR_GOAL_POSITION, 2084)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 14, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 14, ADDR_GOAL_POSITION, 1968)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 16, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 16, ADDR_GOAL_POSITION, 2002)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 13, ADDR_GOAL_POSITION, 2086)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, 112, 40)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 15, ADDR_GOAL_POSITION, 3049)

# Close port
portHandler.closePort()