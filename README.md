# UCIe 2.5D/3D Test System - Comprehensive Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Hardware Components](#hardware-components)
4. [Software Architecture](#software-architecture)
5. [I2C Communication System](#i2c-communication-system)
6. [Proteantecs Integration](#proteantecs-integration)
7. [Board and Chip Initialization](#board-and-chip-initialization)
8. [Test Modes and Configurations](#test-modes-and-configurations)
9. [GUI and User Interface](#gui-and-user-interface)
10. [Test Tools and Utilities](#test-tools-and-utilities)
11. [Register Maps and Documentation](#register-maps-and-documentation)
12. [Installation and Setup](#installation-and-setup)
13. [Usage Guide](#usage-guide)
14. [Troubleshooting](#troubleshooting)
15. [API Reference](#api-reference)

## Project Overview

This is a comprehensive test system for UCIe (Universal Chiplet Interconnect Express) 2.5D and 3D chip testing. The system provides automated testing capabilities for multi-die configurations, hardware training, BIST (Built-In Self-Test), power management, and performance validation.

### Key Features
- **Multi-Die Testing**: Support for Die0, Die1, and Die2 configurations
- **Hardware Training**: Automated eye diagram optimization and signal integrity testing
- **BIST Testing**: Built-in self-test capabilities for PMAD and PCS layers
- **Power Management**: Comprehensive power supply control and monitoring
- **Proteantecs Integration**: Advanced testing and monitoring capabilities
- **I2C Communication**: Full register-level control and monitoring
- **GUI Interface**: User-friendly testing interface with real-time monitoring

### Supported Chip Versions
- **EZ0005A**: Primary test chip with 2.5D configuration
- **EZA001A**: Alternative chip configuration
- **GLink 2.5D/3D**: Different interconnect specifications

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Test PC       │    │   Raspberry Pi  │    │   Test Board    │
│   (GUI/Control) │◄──►│   (I2C Bridge) │◄──►│   (UCIe Chips)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Test Tools    │    │   I2C Protocol  │    │   Power Supply  │
│   & Reporting   │    │   & Monitoring  │    │   & Instruments │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components
1. **Main Control System** (`Glink_Top.py`)
2. **Test Execution Engine** (`Glink_run.py`)
3. **Hardware Abstraction Layer** (`Glink_phy.py`)
4. **Function Library** (`Glink_function.py`)
5. **Instrument Control** (`Instrument.py`)
6. **GUI Interface** (`gui.py`)
7. **Raspberry Pi Interface** (`Raspberry_Pico.py`)

## Hardware Components

### Test Board Configuration
The test system supports a multi-die configuration with the following components:

#### Die Configuration
- **Die 0**: Primary die with TPORT, H, and V groups
- **Die 1**: Secondary die with TPORT, H, and V groups  
- **Die 2**: Tertiary die with TPORT, H, and V groups

#### Group Types
- **TPORT**: Test port group (Group 0)
- **H**: Horizontal group (Group 1)
- **V**: Vertical group (Group 2)

#### Slice Configuration
Each die contains 4 slices (S0, S1, S2, S3) with independent control and monitoring capabilities.

### Power Supply System
The system supports multiple power supply configurations:

#### On-Board Power
- **LDO**: Low Dropout Regulator
- **PMIC**: Power Management IC with voltage sensing
- **PMIC No Sense**: PMIC without voltage sensing

#### External Power Supplies
- **Keysight E36233A**: Dual-channel power supply
- **Keysight E3631xA**: Triple-channel power supply with data logging
- **Keysight E36313A**: Advanced power supply with DMM integration

### Instrument Integration
- **VISA Communication**: Standard instrument control protocol
- **Data Logging**: Real-time voltage and current monitoring
- **Thermal Monitoring**: Temperature sensing and control
- **Signal Analysis**: Eye diagram and signal integrity testing

## Software Architecture

### Core Classes and Modules

#### UCIe_2p5D Class (`Glink_Top.py`)
The main test controller class that orchestrates all testing activities.

**Key Methods:**
- `PLL_Checking()`: Validates PLL lock status across all dies
- `Hardware_Training_Non()`: Performs hardware training for signal optimization
- `PCS_BIST_Check_NON()`: Executes PCS layer BIST testing
- `VCO()`: VCO frequency and performance testing
- `proteantecs()`: Proteantecs integration and testing

#### Test Mode Configurations
The system supports multiple test modes:

**M4_D1H_D2V_mode**: Die1 Horizontal to Die2 Vertical communication
**M4_D0V_D1V_mode**: Die0 Vertical to Die1 Vertical communication

Each mode configures:
- TX/RX die assignments
- Group configurations
- Slice mappings
- PCS group assignments

#### Hardware Training System
The hardware training system optimizes signal integrity through:

1. **Vref Optimization**: Reference voltage adjustment for optimal eye opening
2. **Eye Diagram Analysis**: 1D and 2D eye diagram generation and analysis
3. **Training Result Analysis**: Automated optimization of signal parameters
4. **Center Vref Calculation**: Optimal reference voltage determination

## I2C Communication System

### I2C Architecture
The system uses I2C for register-level control and monitoring of the UCIe chips.

#### Slave Address Configuration
```python
self.EHOST = [
    [0x01, 0x02, 0x03],  # Die0: TPORT, H, V
    [0x01, 0x02, 0x03],  # Die1: TPORT, H, V  
    [0x01, 0x02, 0x03]   # Die2: TPORT, H, V
]
```

#### Register Access Methods
- **Indirect Read/Write**: Register access through I2C protocol
- **Die Selection**: Automatic die selection for register access
- **Slice Addressing**: Per-slice register control with 0x10000 offset

#### Key Register Categories

##### PLL Control Registers
- **CMU Reset Control**: PLL reset and initialization
- **VCO Control**: Frequency and tuning control
- **Clock Distribution**: Clock routing and enable control

##### Slice Control Registers
- **TX Control**: Transmitter configuration and control
- **RX Control**: Receiver configuration and control
- **Training Control**: Hardware training parameter control
- **BIST Control**: Built-in self-test configuration

##### Power Management Registers
- **Voltage Control**: Supply voltage adjustment
- **Current Monitoring**: Power consumption monitoring
- **Thermal Control**: Temperature monitoring and control

### I2C Communication Flow
1. **Die Selection**: Select target die using die_sel()
2. **Slave Address Resolution**: Determine I2C slave address based on die and group
3. **Register Access**: Perform read/write operations with proper addressing
4. **Error Handling**: Implement retry and error recovery mechanisms

## Proteantecs Integration

### Proteantecs Overview
Proteantecs provides advanced testing and monitoring capabilities for the UCIe system, enabling comprehensive signal integrity analysis and performance validation.

### Key Proteantecs Components

#### TCA (Test and Characterization Array)
- **Block Configuration**: Multiple test blocks for comprehensive testing
- **Measurement Control**: Automated measurement execution and data collection
- **Data Analysis**: Real-time analysis of test results

#### Configuration Parameters
```python
# Proteantecs configuration ranges
cfg_range = [0x1e, 0xe, 0x5, 0x2, 0x1, 0x0]  # Configuration values
EW_range = [1, 2, 3, 4]  # Edge window configurations
qdca_osc_bypass_cfg_range = [[0, 0]]  # QDCA oscillator configurations
```

#### Measurement Process
1. **Global Configuration**: Set up Proteantecs global parameters
2. **Block Configuration**: Configure individual test blocks
3. **Measurement Execution**: Run automated measurements
4. **Data Collection**: Collect and process measurement results
5. **Result Analysis**: Analyze and report test results

### Proteantecs Register Map
- **Base Offset**: 0x40000 for Proteantecs registers
- **FIFO Management**: Data collection and processing
- **Command Interface**: Control and status registers
- **Measurement Control**: Start/stop and configuration registers

## Board and Chip Initialization

### Initialization Sequence
The board and chip initialization follows a specific sequence to ensure proper operation:

#### 1. Power-On Sequence
1. **Power Supply Initialization**: Configure and enable power supplies
2. **Voltage Ramping**: Gradual voltage ramp-up to prevent damage
3. **Current Monitoring**: Monitor startup current consumption
4. **Thermal Monitoring**: Check initial temperature conditions

#### 2. Chip Reset and Configuration
1. **Global Reset**: Assert global reset to initialize all dies
2. **Die-by-Die Initialization**: Initialize each die individually
3. **Register Configuration**: Load initial register values
4. **Clock Distribution**: Enable and configure clock distribution

#### 3. PLL Initialization
1. **PLL Reset**: Reset all PLLs to known state
2. **VCO Configuration**: Configure VCO parameters
3. **PLL Lock**: Wait for PLL lock confirmation
4. **Clock Validation**: Verify clock distribution

#### 4. Slice Configuration
1. **Slice Reset**: Reset all slices to default state
2. **Basic Configuration**: Load basic slice configurations
3. **Training Preparation**: Prepare slices for training
4. **BIST Preparation**: Configure BIST capabilities

### Initialization Parameters
- **Voltage Levels**: AVDD, AVSS, IOVDD configuration
- **Clock Frequencies**: System clock and data rate configuration
- **Process Corners**: TT, FF, SS process corner support
- **Temperature Conditions**: Operating temperature range

## Test Modes and Configurations

### Test Mode Categories

#### Training Modes
- **Hardware Training**: Automated signal optimization
- **Software Training**: Software-based training algorithms
- **Manual Training**: User-controlled training parameters

#### BIST Modes
- **PMAD BIST**: Physical Media Access Device BIST
- **PCS BIST**: Physical Coding Sublayer BIST
- **Function BIST**: Functional BIST testing

#### Loopback Modes
- **Near Loopback**: Local loopback testing
- **Far Loopback**: Remote loopback testing

#### Power Modes
- **Power Consumption**: Current consumption measurement
- **Power Noise Immunity**: Noise immunity testing
- **Voltage Margin**: Voltage margin testing

### Configuration Management
The system uses JSON configuration files for test parameter management:

```json
{
    "EZ0005A_D2D": {
        "Corner_Version_wx_json": ["TT", "FF", "SS"],
        "Function_select_wx_json": ["AutoTest"],
        "power": ["OFF", "OnBoard LDO", "OnBoard PMIC", "Keysight_E36233A"],
        "instrument_visa": ["USB0::0x2A8D::0x3302::MY59001241::0::INSTR"]
    }
}
```

## GUI and User Interface

### Main GUI Components (`gui.py`)

#### Main Window Features
- **Specification Selection**: Choose between GLink 2.5D/3D
- **IP Version Selection**: Select chip version (EZ0005A/EZA001A)
- **Connection Control**: Connect/disconnect to test system
- **I2C Information Display**: Real-time I2C communication status

#### Test Configuration Panels
- **Eye Scan Setup**: Receiver eye diagram configuration
- **Training Configuration**: Hardware training parameters
- **BIST Configuration**: Built-in self-test settings
- **Power Configuration**: Power supply and voltage settings
- **Instrument Configuration**: Test instrument setup

#### Real-Time Monitoring
- **Test Progress**: Real-time test execution status
- **Error Reporting**: Immediate error detection and reporting
- **Data Logging**: Continuous data collection and logging
- **Result Display**: Test results and analysis display

### Event Handling (`event.py`)
- **User Input Processing**: Handle user interactions
- **Test Execution Control**: Start/stop test execution
- **Error Handling**: Manage and report system errors
- **Status Updates**: Real-time status updates

## Test Tools and Utilities

### Data Analysis Tools

#### Eye Diagram Analysis (`Graph.py`)
- **2D Eye Diagram Generation**: Comprehensive eye diagram visualization
- **Signal Integrity Analysis**: Signal quality assessment
- **Margin Analysis**: Timing and voltage margin calculation
- **Result Export**: Export analysis results to various formats

#### Report Generation (`Report.py`)
- **Word Document Reports**: Comprehensive test reports
- **Excel Data Export**: Test data in spreadsheet format
- **Chart Generation**: Graphical representation of test results
- **Custom Formatting**: Configurable report formatting

### Utility Functions

#### File Management
- **Test Data Storage**: Organized test data storage
- **Log File Management**: Comprehensive logging system
- **Backup and Recovery**: Data backup and recovery capabilities

#### Data Processing
- **Real-Time Analysis**: Live data analysis during testing
- **Statistical Analysis**: Statistical processing of test results
- **Trend Analysis**: Long-term trend monitoring

## Register Maps and Documentation

### Register Map Structure
The system includes comprehensive register maps for all chip components:

#### EHOST Register Map
- **Programming Guide**: Complete register programming documentation
- **Register Descriptions**: Detailed register field descriptions
- **Access Methods**: Read/write access procedures

#### PLL Register Map
- **PLL Control Registers**: Clock generation and control
- **VCO Configuration**: Voltage-controlled oscillator settings
- **Clock Distribution**: Clock routing and enable control

#### Slice Register Map
- **TX/RX Control**: Transmitter and receiver control
- **Training Registers**: Hardware training configuration
- **BIST Registers**: Built-in self-test control

### Documentation Files
- **Datasheets**: Complete chip datasheets and specifications
- **Programming Guides**: Step-by-step programming instructions
- **Test Procedures**: Detailed test execution procedures
- **Troubleshooting Guides**: Common issues and solutions

## Installation and Setup

### System Requirements
- **Operating System**: Windows 10/11 or Linux
- **Python Version**: Python 3.8 or higher
- **Hardware**: Test board with UCIe chips
- **Instruments**: Compatible power supplies and measurement equipment

### Software Dependencies
```bash
pip install pyvisa
pip install openpyxl
pip install pandas
pip install matplotlib
pip install numpy
pip install tabulate
pip install python-docx
pip install wxpython
pip install mpremote
pip install psutil
pip install pyautogui
```

### Hardware Setup
1. **Test Board Connection**: Connect test board to control system
2. **Power Supply Connection**: Connect and configure power supplies
3. **Instrument Connection**: Connect measurement instruments
4. **Raspberry Pi Setup**: Configure Raspberry Pi for I2C communication

### Configuration Setup
1. **VISA Configuration**: Configure instrument VISA addresses
2. **I2C Configuration**: Set up I2C communication parameters
3. **Test Parameters**: Configure test-specific parameters
4. **Report Configuration**: Set up reporting and logging

## Usage Guide

### Basic Test Execution
1. **System Initialization**: Power on and initialize test system
2. **GUI Launch**: Start the test GUI application
3. **Configuration**: Select test parameters and configurations
4. **Test Execution**: Run automated test sequences
5. **Result Analysis**: Review and analyze test results

### Advanced Testing
1. **Custom Test Sequences**: Create custom test sequences
2. **Parameter Sweeping**: Perform parameter sweeps
3. **Statistical Testing**: Execute statistical test procedures
4. **Long-term Testing**: Run extended test campaigns

### Data Management
1. **Test Data Storage**: Organize and store test data
2. **Report Generation**: Generate comprehensive test reports
3. **Data Analysis**: Perform detailed data analysis
4. **Trend Monitoring**: Monitor long-term trends

## Troubleshooting

### Common Issues

#### Connection Problems
- **I2C Communication Errors**: Check I2C connections and addresses
- **Instrument Communication**: Verify VISA addresses and connections
- **Power Supply Issues**: Check power supply connections and settings

#### Test Execution Issues
- **PLL Lock Failures**: Check clock connections and power supplies
- **Training Failures**: Verify signal connections and configurations
- **BIST Failures**: Check chip configuration and connections

#### Software Issues
- **GUI Responsiveness**: Check system resources and performance
- **Data Logging**: Verify file permissions and disk space
- **Report Generation**: Check template files and dependencies

### Debugging Tools
- **I2C Logging**: Comprehensive I2C communication logging
- **Error Reporting**: Detailed error reporting and analysis
- **Status Monitoring**: Real-time system status monitoring
- **Diagnostic Tests**: Built-in diagnostic test capabilities

## API Reference

### Core Classes

#### UCIe_2p5D Class
```python
class UCIe_2p5D:
    def __init__(self, phy, gui):
        # Initialize test controller
        
    def PLL_Checking(self, **kwargs):
        # Check PLL lock status
        
    def Hardware_Training_Non(self, **kwargs):
        # Perform hardware training
        
    def PCS_BIST_Check_NON(self, **kwargs):
        # Execute PCS BIST testing
```

#### Instrument Control
```python
class D2D_Subprogram:
    def __init__(self, gui):
        # Initialize instrument control
        
    def E363xA_Setup(self, CH1_V, **kwargs):
        # Configure power supply
        
    def Keysight_DataLog_793(self, **kwargs):
        # Data logging functionality
```

#### Raspberry Pi Interface
```python
class Pico:
    def __init__(self, i2c_address):
        # Initialize Raspberry Pi interface
        
    def scan(self):
        # Scan I2C devices
        
    def write(self, slave, offset, data):
        # Write I2C data
```

### Key Methods and Functions

#### Register Access
- `indirect_read(slave, offset, bit, slice_num)`: Read register
- `indirect_write(slave, offset, bit, data, slice_num)`: Write register
- `die_sel(die)`: Select target die

#### Test Execution
- `reg_user_set(die_arr, group_arr, tx_slice, rx_slice, reg_arr, mode)`: Configure registers
- `train_result(die, group, group_n, slice)`: Get training results
- `BIST_ERR_COUNT(die, group, slice)`: Get BIST error counts

#### Power Management
- `TPSM831D31_VoltageSet(channel, ch_type, voltage)`: Set power supply voltage
- `avdd_sense(mode, voltage_sense_avdd)`: Perform voltage sensing
- `thermal_voltage_read()`: Read thermal voltages

---

## Conclusion

This UCIe 2.5D/3D Test System provides a comprehensive solution for testing and validating UCIe chip implementations. The system combines advanced hardware control, automated testing capabilities, and comprehensive analysis tools to ensure reliable and thorough testing of multi-die UCIe configurations.

The modular architecture allows for easy extension and customization, while the comprehensive GUI and API provide both user-friendly operation and programmatic control capabilities.

For additional support or questions, please refer to the troubleshooting section or contact the development team.

---

*Last Updated: [Current Date]*
*Version: 1.0*
*Compatible with: EZ0005A, EZA001A, GLink 2.5D/3D*
