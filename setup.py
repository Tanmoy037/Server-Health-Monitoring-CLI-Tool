from setuptools import setup, find_packages

setup(
    name="server-health-monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
        "argparse>=1.4.0",
        "rich>=13.0.0",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "server-monitor=server_health_monitor.entrypoint:main",
        ],
    },
    python_requires=">=3.8",
) 