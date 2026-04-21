import os
import stat


class LogsManager:
    def __init__(self, log_dir):
        self.log_dir = os.path.abspath(log_dir)

    def create_log_dir(self):
        # create the logs directory with restricted permissions
        if os.path.exists(self.log_dir):
            if not os.path.isdir(self.log_dir):
                raise FileExistsError(f"'{self.log_dir}' exists and is not a directory")
            return self.log_dir

        os.makedirs(self.log_dir, mode=0o700, exist_ok=True)
        return self.log_dir

    def get_log_path(self, filename):
        # return a full path inside the log directory, preventing path traversal
        full_path = os.path.normpath(os.path.join(self.log_dir, filename))
        if not full_path.startswith(self.log_dir):
            raise ValueError("Invalid filename: path traversal detected")
        return full_path