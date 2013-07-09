import pystache

def config_property_is_true(build_params, config_property):
	if isinstance(config_property, str) or isinstance(config_property, unicode):
		config_property = pystache.render(config_property, build_params['app_config'])

	return config_property == "True"