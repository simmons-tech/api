// SIMMONS API CLIENT STUBS FOR JAVASCRIPT
// This code was auto-generated by stubgen.py
// DO NOT EDIT IT BY HAND. Edit apis.yaml instead.
// This will ensure that changes are reflected in other
// languages stubs.

this.RPC_call = function( path, callback ) {
	console.log("Tried to call to {{server_path}}" + path);
        return $.getJSON("{{server_path}}" + path, callback);
}

{% for api in apis %}
// Beginning stubs for {{api['name']}}:
// {{api['desc']}}
this.{{api['name']}} = {
	{% for method in api['fxns'] %}
	// {{method['desc']}}
	{{method['name']}}: function( {% for arg in method['args'] %}{{arg}}, {% endfor %}callback ) {
		return RPC_call( {{ f( api['path'] + method['path'] ) }}, callback );
	},
{% endfor %}}; // End of stubs for {{api['name']}}
{% endfor %}
