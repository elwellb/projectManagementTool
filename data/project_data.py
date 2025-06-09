from utils.file_utils import load_data, save_data

class ProjectStore:
    def __init__(self):
        self.data = load_data()

    def save(self):
        save_data(self.data)

    def get_projects(self):
        return list(self.data.get("projects", {}).keys())

    def get_assets(self, project):
        return self.data["projects"].get(project, {}).get("assets", [])

    def add_project(self, project):
        self.data.setdefault("projects", {})
        self.data["projects"].setdefault(project, {"assets": []})
        self.save()

    def add_asset(self, project, asset_name, asset_type):
        self.data["projects"].setdefault(project, {})
        self.data["projects"][project].setdefault("assets", [])

        asset_entry = {
            "name": asset_name,
            "type": asset_type
        }

        # Avoid duplication
        if not any(a for a in self.data["projects"][project]["assets"] if a["name"] == asset_name and a["type"] == asset_type):
            self.data["projects"][project]["assets"].append(asset_entry)
            self.save()