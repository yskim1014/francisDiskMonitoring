# Call by import
import re
import json
import subprocess
# Disk handling
class DiskChecker:
    def __init__(self) -> None:
        self.drives_prev, self.drives_curr, self.storcli_results = {}, {}, {}

    def get_drive_status(self) -> None:
        self.drives_prev, self.drives_curr, self.storcli_results = self.drives_curr, {}, {}
        try:
            outputs = json.loads(subprocess.run(["storcli", "/c0/eall/sall", "show", "all", "J"], capture_output = True, text = True, check = True).stdout)
        except subprocess.CalledProcessError as e:
            print('Fail to Call Process')

        for key, value in outputs.get('Controllers',[{'Response Data':''}])[0]['Response Data'].items():
            if 'Detailed Information' in key:
                for key, value in value.items():
                    if 'State' in key:
                        self.storcli_results[key] = value

    def get_drive_missing(self) -> None:
        for i in (set(f'Drive /c0/e252/s{i} State' for i in range(8)) - set(self.storcli_results.keys())):
            self.drives_curr[i] = {'State': 'Missing'}

    def get_drive_differences(self) -> None:
        for drive, states in self.storcli_results.items():
            for state, value in states.items():
                if (('Count' in state) and value) or (('Temperature' in state) and int(value.split('C')[0])>=45) or (('flagged' in state) and value != 'No'):
                    self.drives_curr[drive] = self.drives_curr.get(drive, {})
                    self.drives_curr[drive][state] = value

    def get_pretty_str(self) -> str:
        text = ''
        for drive, states in self.drives_curr.items():
            text += drive + "\n"
            for state, value in states.items():
                text += f"  {state}: {value}\n"
        return text.strip()
