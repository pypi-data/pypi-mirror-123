
from pod_picker import *
from pod_picker.pod_picker import execute_pick_pod

if __name__ == '__main__':
    # pick_pod_version()
    main_path = '/Users/gujitao001/Documents/grt/APlus/Podfile.lock'
    component_path = '/Users/gujitao001/Documents/grt/LJBMapSearchHouse/Example/Podfile.lock'
    result_path = 'resultPath'
    execute_pick_pod(main_path, component_path, result_path)