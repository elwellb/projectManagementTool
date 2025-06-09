from utils.file_utils import load_data, save_data

class ProjectStore:
    """
    Handles storage and management of project and asset data.
    """

    def __init__(self):
        """
        Initializes the ProjectStore by loading existing data.
        """
        self.data = load_data()
        self.data.setdefault("projects", {})  # Ensure 'projects' key exists

    def save(self):
        """
        Persists the current state of data to storage.
        """
        save_data(self.data)

    def get_projects(self):
        """
        Retrieves a list of all project names.
        """
        return list(self.data.get("projects", {}).keys())

    def get_assets(self, project):
        """
        Retrieves the list of assets for a given project.
        """
        return self.data["projects"].get(project, {}).get("assets", [])

    def add_project(self, project):
        """
        Adds a new project if it does not already exist.
        """
        self.data.setdefault("projects", {})  # Ensure 'projects' key exists
        self.data["projects"].setdefault(project, {"assets": []})  # Add project if missing
        self.save()

    def add_asset(self, project, asset_name, asset_type):
        """
        Adds a new asset to a project, avoiding duplicates.
        """
        self.data["projects"].setdefault(project, {})  # Ensure project exists
        self.data["projects"][project].setdefault("assets", [])  # Ensure 'assets' list exists

        asset_entry = {
            "name": asset_name,
            "type": asset_type
        }

        # Only add asset if it doesn't already exist in the project
        if not any(a for a in self.data["projects"][project]["assets"] if a["name"] == asset_name and a["type"] == asset_type):
            self.data["projects"][project]["assets"].append(asset_entry)
            self.save()

    def rename_project(self, old_name, new_name):
        if new_name in self.data["projects"]:
            raise ValueError(f"Project '{new_name}' already exists.")
        self.data["projects"][new_name] = self.data["projects"].pop(old_name)
        self.save()

    def delete_project(self, name):
        """
        Deletes a project and all its associated assets.
        """
        if name in self.data["projects"]:
            del self.data["projects"][name]
            self.save()

    def rename_asset(self, project, old_name, new_name):
        """
        Renames an asset within a project.
        """
        for asset in self.data["projects"].get(project, {}).get("assets", []):
            if asset["name"] == old_name:
                asset["name"] = new_name
                break
        self.save()

    def delete_asset(self, project, asset_name):
        """
        Deletes an asset from a project.
        """
        self.data["projects"][project]["assets"] = [
            a for a in self.data["projects"][project]["assets"] if a["name"] != asset_name]
        self.save()
                