def uchart_plugin(plugin_class):
    """
        A decorator that registers uchart plugins
    """
    if not hasattr(uchart_plugin, 'plugins'):
        setattr(uchart_plugin, 'plugins', [])
    getattr(uchart_plugin, 'plugins').append(plugin_class)


def pprint_dict_to_json(collection):
    import json
    print(json.dumps(collection, indent=2))
