from lib import predicate

@predicate
def icon_available(build, platform, size):
	return "plugins" in build.config and \
		"icons" in build.config["plugins"] and \
		(size in build.config["plugins"]["icons"]["config"] or \
		size in build.config["plugins"]["icons"]["config"].get(platform, {}))

@predicate
def have_wp_launch(build):
	return "plugins" in build.config and \
		"launchimage" in build.config.get("plugins") and \
		"wp" in build.config["plugins"]["launchimage"].get("config") and \
		"wp-landscape" in build.config["plugins"]["launchimage"].get("config")
