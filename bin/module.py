import importlib.util
import os
import bin.file_tools as tools

def scan(cls):
    cls.log.info(scan)
    folder =  cls.basepath + '/module'
    files = tools.find_files(folder, '*.py')
    change = False
    if not ('module' in  cls.cfg.data):
        cls.cfg.data['module'] = {}
    for file in files:
        name = file.split('/')[-1][:-3]
        if not name.startswith('__'):
            if not name in cls.cfg.data['module']:
                cls.cfg.data['module'][name] = {}
                change = True
            if not 'active' in cls.cfg.data['module'][name]:
                cls.cfg.data['module'][name]['active'] = False
                change = True
    if change:
        cls.cfg.save()

def load(sh, name):
    sh.log.info(name)
    cfg = sh.cfg.data['module'][name]
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
        cls.modul_name = name
    except Exception as e:
        sh.log.error(str(e))
    return cls
