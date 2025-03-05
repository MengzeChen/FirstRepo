import subprocess

class FileManager:
	def __init__(self, remote, local, cloud):
		self.remote_name = remote
		self.local_dir = local
		self.cloud_dir = cloud
	# store the name of the remote, the name of the master local directory and the name of the master cloud directory

	def convertCloudToLocal(self, filename):
		if filename.startswith(self.remote_name + ":"):
			return filename.replace(self.remote_name + ":", self.local_dir, 1)
		return filename
	# convert the name of the cloud location (which will include the remote) to the local name

	def convertLocalToCloud(self, filename):
		if filename.startswith(self.local_dir):
			return filename.replace(self.local_dir, self.remote_name + ":" + self.cloud_dir, 1)
		return filename
	# convert the name of the local location to the cloud location

	def uploadData(self, filename):
		cloud_path = self.convertLocalToCloud(filename)
		subprocess.run(["rclone", "copy", filename, cloud_path], check=True)
		print(f"Uploaded: {filename} -> {cloud_path}")
	# upload a local file to the cloud

	def downloadData(self, filename):
		local_path = self.convertCloudToLocal(filename)
		subprocess.run(["rclone", "copy", filename, local_path], check=True)
		print(f"Downloaded: {filename} -> {local_path}")
	# download a cloud file to the local drive






