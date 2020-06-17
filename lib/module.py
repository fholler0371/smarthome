import importlib.util
import os

def load(sh, name, cfg):
    sh.log.info(name)
    cls = None
    file = sh.basepath + '/module/' + name + '.py'
    if not os.path.exists(file):
        sh.log.error(file + ' nicht gefunden')
        return cls
    try:
        spec = importlib.util.spec_from_file_location(name, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cls = mod.modul(sh, cfg)
    except:
        sh.log.error(name + ' Fehler beim laden')
    return cls
