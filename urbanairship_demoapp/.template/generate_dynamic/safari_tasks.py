def _generate_package_name(build):
	if "core" not in build.config:
		build.config["core"] = {}
	if "safari" not in build.config["core"]:
		build.config["core"]["safari"] = {}
	if "package_name" not in build.config["core"]["safari"]:
		build.config["core"]["safari"]["package_name"] = "forge.safari.{package_name}".format(package_name=build.config["package_name"])
	return build.config["core"]["safari"]["package_name"]
