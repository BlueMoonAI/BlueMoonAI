import platform
import subprocess
import psutil
import GPUtil
import pygetwindow as gw
from bluemoon.utils.logly import logly

def get_system_info():
    """
    Collects various system information including CPU, GPU, memory, hard disk space, and external GPU (if available).

    Returns:
    - dict: A dictionary containing system information.
    """
    system_info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Platform": platform.platform(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "GPU": get_gpu_info(),
        "External GPU": get_external_gpu_info(),
        "Disk Space": get_disk_space(),
    }
    return system_info

def get_gpu_info():
    """
    Retrieves information about the available GPUs, including integrated and external GPUs.

    Returns:
    - list or None: A list containing GPU information or None if no GPU is detected.
    """
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return None

        gpu_info = []
        for i, gpu in enumerate(gpus, 1):
            gpu_info.append(f"GPU {i}: {gpu.name}")
            gpu_info.append(f"  ROM: {gpu.rom}")

        return gpu_info
    except Exception as e:
        return [f"Error retrieving GPU information: {e}"]

def get_windows_gpu_info():
    try:
        gpus = gw.getWindowsWithTitle('Device Manager')
        gpu_info = [f"GPU {i}: {gpu.title}" for i, gpu in enumerate(gpus, 1)]
        return gpu_info
    except Exception as e:
        return [f"Error retrieving GPU information on Windows: {e}"]

def get_linux_gpu_info():
    try:
        external_gpu_info = subprocess.check_output(['lshw', '-C', 'display'], text=True)
        return [line.strip() for line in external_gpu_info.split('\n')]
    except subprocess.CalledProcessError as e:
        return [f"Error retrieving GPU information on Linux: {e}"]

def get_macos_gpu_info():
    try:
        external_gpu_info = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'], text=True)
        return [line.strip() for line in external_gpu_info.split('\n')]
    except subprocess.CalledProcessError as e:
        return [f"Error retrieving GPU information on macOS: {e}"]

def get_external_gpu_info():
    """
    Retrieves information about external GPUs based on the platform.

    Returns:
    - str or list or None: Information about external GPUs or None if no external GPU is detected.
    """
    try:

        if platform.system() == 'Windows':
            return get_windows_gpu_info()
        '''
        elif platform.system() == 'Darwin':  # macOS
            #return get_macos_gpu_info()
             return None
        elif platform.system() == 'Linux':
           # return get_linux_gpu_info()
            return None

        else:
            return None
            '''
    except subprocess.CalledProcessError as e:
        return [f"Error retrieving external GPU information: {e}"]

def get_disk_space():
    """
    Retrieves information about the available disk space.

    Returns:
    - str: A string containing disk space information.
    """
    partitions = psutil.disk_partitions()
    disk_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append(
            f"{partition.device} - Total: {usage.total / (1024 ** 3):.2f} GB, Used: {usage.used / (1024 ** 3):.2f} GB, Free: {usage.free / (1024 ** 3):.2f} GB")

    return disk_info

def save_to_file(data, filename='../system_info.txt'):
    """
    Saves the provided system information data to a text file.

    Parameters:
    - data (dict): A dictionary containing various system information.
    - filename (str, optional): The name or path of the file to save the data. Default is 'system_info.txt'.

    Returns:
    - None: The function writes the data to the specified file.
    """
    with open(filename, 'w') as file:
        for key, value in data.items():
            if isinstance(value, list):
                file.write(f"{key}:\n")
                for item in value:
                    file.write(f"  - {item}\n")
            else:
                file.write(f"{key}: {value}\n")

def check_system_info():
    system_info = get_system_info()
    save_to_file(system_info)

    if system_info["GPU"] is None:
        logly.error("No GPU detected.")
    elif "Error" in system_info["GPU"]:
        logly.error(system_info["GPU"])
        logly.error("Your GPU may not be compatible. Please check the system_info.txt file for more information.")
    else:
        logly.info("GPU information available:")
        for line in system_info["GPU"]:
            logly.info(f"   - {line}")

        external_gpu_info = system_info["External GPU"]
        if external_gpu_info is None:
            logly.info("No external GPU detected.")
        elif "External GPU" in external_gpu_info and any(external_gpu_info):
            logly.info("\nExternal GPU Information:")
            for line in external_gpu_info:
                logly.info(f"   - {line}")
        elif platform.system() == 'Darwin':  # macOS
            logly.info("\nWarning: External GPU information not available on macOS. Performance may decrease compared to dedicated GPU.")
        else:
            logly.info("\nWarning: No external GPU detected. Your GPU may not be compatible or not work properly.")

        # Display disk space information
        disk_space_info = system_info["Disk Space"]
        if disk_space_info:
            logly.info("\nDisk Space Information:")
            for line in disk_space_info:
                logly.info(f"   - {line}")
        else:
            logly.info("No disk space information available.")

if __name__ == "__main__":
    check_system_info()
