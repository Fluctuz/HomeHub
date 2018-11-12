from toggl.TogglPy import Toggl
import json


class TogglApi:
    CONFIG_FILENAME = "config.json"

    def __init__(self):
        self.config = self.load_config()
        api_token = self.config['toggl']['token']
        self.toggl = Toggl()
        self.toggl.setAPIKey(api_token)

    def load_config(self):
        with open(self.CONFIG_FILENAME, 'r') as f:
            return json.load(f)

    def current_timer(self):
        return self.toggl.currentRunningTimeEntry()

    def start_timer(self, project_name, description):
        print(self.config['toggl']['project_ids'][project_name])
        t = self.toggl.startTimeEntry(self.config['toggl']['project_ids'][project_name], description)
        print(t)

    def stop_timer(self):
        current_timer = self.current_timer()
        if current_timer:
            self.toggl.stopTimeEntry(current_timer['data']['id'])
            return True
        return False


if __name__ == '__main__':
    print(TogglApi().current_timer())
    TogglApi().start_timer("Ausruhen", "schnarch")

