import subprocess
import time
class NetManager:
    def __init__(self):
        self.stop = 0

    def isNetworkConnected(self):
        host = "142.44.139.6"  # Replace with the host you want to ping
        result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    
    def isFlathubEnabled(self, progress):
        result = subprocess.run(["flatpak", "remotes"], capture_output=True, text=True)
        output = result.stdout.lower()
        flag = "flathub" in output
        if(flag == True):
            return True
        else:
            return False
    
    def cancelProcess(self, thread):
        self.stop = 1

    def installFlathub(self,progress, label):
        progress.set_text("Configurando...")
        label.set_text("Configurando Pacotes")
        # Add Flathub repository
        time.sleep(0.5)
        subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"])

        time.sleep(0.5)
        # Kill all gnome-software processes
        subprocess.run(["pkill", "gnome-software"])

        time.sleep(0.5)
        # Remove gnome-software cache
        subprocess.run(["rm", "-rf", "~/.cache/gnome-software"])
        return True

    def openGnomeNetwork(self, arg):
        try:
        # Execute the flatpak run command
            subprocess.Popen(['gnome-control-center', 'wifi'], start_new_session=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to run ")
            return False


    def openGnomeSoftware(self, args):
        try:
            subprocess.Popen(['gnome-software'], start_new_session=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to run ")
            return False

    def openApp(self, app_id):
        try:
        # Execute the flatpak run command
            subprocess.Popen(["flatpak", "run", app_id], start_new_session=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to run {app_id}")
            return False

    def isAppInstaled(self, exec_name):
        result = subprocess.run(["flatpak", "list"], capture_output=True, text=True)
        output = result.stdout

        if exec_name in output:
            return True
        else:
            return False

    def removeApp(self, app_id):
        try:
            # Execute the flatpak uninstall command
            subprocess.run(["flatpak", "uninstall", "-y", app_id ], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to uninstall {app_id}")
            return False

    def installApp(self, app_id, progress, label, name):
        i = 0
        progress.set_text("Configurando...")
        label.set_text("Instalando " + name)
        command = ["flatpak", "install", "-y", app_id]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in iter(process.stdout.readline, b''):
            time.sleep(0.1)
            i=i+1
            if(i > 20):
                progress.set_text(line)
            if(line == ""):
                return True
            if(self.stop == 1):
                process.terminate()
                self.removeApp(app_id)
                self.stop = 0
                return False
        process.communicate()
        return False

    def openApp(self, app_id):
        try:
        # Execute the flatpak run command
            subprocess.Popen(["flatpak", "run", app_id], start_new_session=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to run {app_id}")
            return False

