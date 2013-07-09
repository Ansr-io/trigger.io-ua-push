forge.inspector = {
	getFixture: function (plugin, file) {
		var location = window.location.origin + window.location.pathname;
		var url = decodeURI(location.substring(0, location.length-10));
		url = url + 'fixtures/' + plugin + (file.substring(0, 1) == '/' ? '' : '/') + file;
		return {
			uri: url
		};
	}
}

$(function () {
	forge.internal.call('inspector.list', {}, function (methods) {
		var modules = {};
		for (method in methods) {
			var parts = method.split('.');
			apimethod = parts.pop();
			var module = parts.join('.');
			if (!modules[module]) {
				modules[module] = {};
			}
			modules[module][apimethod] = methods[method];
		}
		for (module in modules) {
			$('#_module').append('<option>'+module+'</option>');
		}
		$('#_module').change(function () {
			var methods = modules[$(this).val()]; 
			$('#_method').html('');
			for (method in methods) {
				$('#_method').append('<option>'+method+'</option>');
			}
			$('#_method').change();
		})
		$('#_module').change();
		$('#_method').change(function () {
			var module = $('#_module').val();
			var method = $(this).val(); 
			var params = modules[module][method];
			$('.api_input').detach();
			for (param in params) {
				$('#_actions').before('<div class="control-group api_input"><label class="control-label" for="'+param+'">'+param+'</label><div class="controls"><input type="text" class="input-xlarge" id="'+param+'"></div></div>');
			}
		})
		$('#_method').change();
		$('#_run').click(function () {
			var module = $('#_module').val();
			var method = $('#_method').val();
			var params = {};
			
			$('.api_input input').each(function (i, x) {
				params[$(x).attr('id')] = $(x).val();
			});
			
			$('#_output').prepend('<pre class="alert alert-info">Called "'+module+'.'+method+'" with "'+JSON.stringify(params, null, '')+'"</pre>');
			forge.internal.call(module+'.'+method, params, function () {
				$('#_output').prepend('<pre class="alert alert-success">Success for "'+module+'.'+method+'" with "'+JSON.stringify(arguments[0], null, '')+'"</pre>');
			}, function () {
				$('#_output').prepend('<pre class="alert alert-error">Error for "'+module+'.'+method+'" with "'+JSON.stringify(arguments[0], null, '')+'"</pre>');
			})
		});
	}, function () {
		alert("Error");
	});
	forge.internal.addEventListener('*', function (event, e) {
		if (event == 'inspector.eventTriggered') {
			$('#_output').prepend('<pre class="alert alert-warning">Native event triggered "'+e.name+'"</pre>');
		} else if (event == 'inspector.eventInvoked') {
			if (e['class'] == 'ForgeEventListener') {
				$('#_output').prepend('<pre class="alert alert-warning">Default event listener for "'+e.name+'" called</pre>');
			} else {
				$('#_output').prepend('<pre class="alert alert-warning">Calling event listener "'+e.name+'" in class "'+e['class']+'"</pre>');
			}
		} else {
			$('#_output').prepend('<pre class="alert alert-warning">Javascript event "'+event+'" triggered with data "'+JSON.stringify(e)+'"</pre>');
		}
	});
});