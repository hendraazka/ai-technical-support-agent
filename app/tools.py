import os
import platform
import shutil
import psutil
from datetime import timedelta
import json
import subprocess
import shutil
import time


def get_system_status():
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")
    boot_time = psutil.boot_time()
    uptime = timedelta(seconds=int(time.time() - boot_time))

    return {
        "hostname": platform.node(),
        "os": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "memory_total": round(memory.total / (1024 ** 3), 2),
        "memory_used": round(memory.used / (1024 ** 3), 2),
        "memory_percent": memory.percent,
        "disk_total": round(disk.total / (1024 ** 3), 2),
        "disk_used": round(disk.used / (1024 ** 3), 2),
        "disk_percent": round(disk.used / disk.total * 100, 2),
        "uptime": str(uptime),
    }


def format_system_status():
    status = get_system_status()

    return (
        "🖥️ SYSTEM STATUS\n\n"
        f"Hostname: {status['hostname']}\n"
        f"OS: {status['os']}\n"
        f"CPU: {status['cpu_percent']}% "
        f"({status['cpu_count']} cores)\n\n"
        "💾 MEMORY\n"
        f"Used: {status['memory_used']} GB / "
        f"{status['memory_total']} GB\n"
        f"Usage: {status['memory_percent']}%\n\n"
        "💿 DISK (/)\n"
        f"Used: {status['disk_used']} GB / "
        f"{status['disk_total']} GB\n"
        f"Usage: {status['disk_percent']}%\n\n"
        f"⏱️ Uptime: {status['uptime']}"
    )

def get_docker_status():
    if not shutil.which("docker"):
        return "Docker CLI tidak ditemukan."

    try:
        result = subprocess.run(
            ["docker", "ps", "--all", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        containers = [
            json.loads(line)
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if not containers:
            return "Tidak ada Docker container."

        output = ["🐳 DOCKER CONTAINERS\n"]

        for container in containers:
            output.append(
                f"Name: {container['Names']}\n"
                f"Image: {container['Image']}\n"
                f"Status: {container['Status']}\n"
                f"State: {container['State']}\n"
            )

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Docker command timeout."
    except subprocess.CalledProcessError as error:
        return f"Docker error: {error.stderr.strip()}"