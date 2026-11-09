import subprocess

subprocess.run(
	["ifconfig", "wlan0"],
	shell=True,
)
