import platform
import GPUtil

def get_system_info():
    system_info = f"System Information:\n\n"
    system_info += f"Platform: {platform.platform()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"System Architecture: {platform.architecture()}\n"

    try:
        # Use 'GPUtil' package to check GPU information
        gpus = GPUtil.getGPUs()
        if gpus:
            system_info += "\nGPU Information:\n\n"
            for i, gpu in enumerate(gpus, 1):
                system_info += f"GPU {i}:\n"
                system_info += f"  Name: {gpu.name}\n"
                system_info += f"  Driver: {gpu.driver}\n"
                system_info += f"  Memory Total: {gpu.memoryTotal} MB\n"
        else:
            system_info += "\nNo GPU Available.\n"
    except ImportError:
        system_info += "\nNo GPU Information (GPUtil package not installed).\n"

    return system_info

def check_system_info():
    # Get system information
    system_info = get_system_info()

    # Print system information
    print(system_info)

    # Save system information to a file
    with open("../system_info.txt", "w") as file:
        file.write(system_info)
