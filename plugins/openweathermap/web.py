def sm_backend(sh, plugin, data):
   out = {}
   out['friendly_name']= plugin.cfg['friendly_name']
   out['api']= plugin.cfg['api']
   out['intervall']= plugin.cfg['intervall']
   return out
