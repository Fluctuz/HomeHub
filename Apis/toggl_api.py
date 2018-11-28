from toggl.TogglPy import Toggl
from datetime import datetime
from Apis.config_loader import load_config


class TogglApi:

    def __init__(self):
        self.config = load_config()
        api_token = self.config['toggl']['token']
        self.toggl = Toggl()
        self.toggl.setAPIKey(api_token)

    def preset_projects(self):
        return self.config['toggl']['preset_projects']

    def current_timer(self):
        timer = self.toggl.currentRunningTimeEntry()['data']
        if timer:
            if 'pid' in timer:
                project = self.get_project_name(timer['pid'])
            else:
                project = ['Kein Projekt', (244, 244, 6)]

            timer_dic = {'name': timer.get('description',""), 'id': timer['id'],
                         'start_time': datetime.fromtimestamp(int(timer['duration']) * -1),
                         'project_name': project[0],
                         'project_color': project[1]}
            # start = datetime.strptime(timer['start'],"%Y-%m-%dT%H:%M:%S+00:00")
            return timer_dic
        else:
            return {'name': "",
                    'id': "1234",
                    'start_time': datetime.fromtimestamp(1542385078),
                    'project_name': "Kein Projekt",
                    'project_color': (30, 0, 0)}

    def get_project_name(self, pid):
        project = self.toggl.getProject(pid)['data']
        name = project['name']
        try:
            color = self.hex_to_rgb(project['hex_color'])
            color = (int(color[0]/2), int(color[1]/2), int(color[2]/2))
        except():
            color = (200, 200, 200)
        return name, color

    def start_timer(self, project_name, description):
        print(self.config['toggl']['project_ids'][project_name])
        self.toggl.startTimeEntry(description, self.config['toggl']['project_ids'][project_name])

    def stop_timer(self):
        current_timer_id = self.current_timer()['id']
        if current_timer_id:
            self.toggl.stopTimeEntry(current_timer_id)
            return True
        return False

    @staticmethod
    def hex_to_rgb(hex_str):
        hex = hex_str[1:]  # remove pound sign
        # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))


if __name__ == '__main__':
    api = TogglApi()
    print(api.current_timer())
    # TogglApi().start_timer("Ausruhen", "schnarch")
