import yaml
import pod_picker.pod_model
import argparse


# https://www.jianshu.com/p/eaa1bf01b3a6

def read_yaml_map(path):
    file = open(path, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    print(file_data)
    print("类型：", type(file_data))

    # 将字符串转化为字典或列表
    print("***转化yaml数据为字典或列表***")
    data = yaml.load(file_data)
    print(data)
    print("类型：", type(data))
    return data


def pod_str_from_dict(pod_part) -> str:
    if isinstance(pod_part, str):
        return pod_part
    name_dict = pod_part
    name_key_list = list(name_dict.keys())
    if not len(name_key_list) == 1:
        return None
    pod_name_key = name_key_list[0]
    return pod_name_key;


def real_pod_name(pod_part, pod_name) -> str:
    pod_part_string = pod_str_from_dict(pod_part)
    prefix1 = '{pod_name} ('.format(pod_name=pod_name)
    prefix2 = '{pod_name}/'.format(pod_name=pod_name)
    if pod_part_string.startswith(prefix1) or pod_part_string.startswith(prefix2):
        return pod_name
    return None

    # if isinstance(dep_pod_str, str):
    #     prefix = '{pod_name} ('.format(pod_name=pod_name)
    #     if not dep_pod_str.startswith(prefix):
    #         return None
    #     return pod_name
    # else:
    #     name_dict = dep_pod_str
    #     name_key_list = list(name_dict.keys())
    #     if not len(name_key_list) == 1:
    #         return None
    #     pod_name_key = name_key_list[0]
    #     return real_pod_name(pod_name_key, pod_name)


def pod_model_from_dependencies(pod_name, main_pod_list) -> pod_picker.pod_model.PodModel:
    pm = pod_picker.pod_model.PodModel()
    for dep_name in main_pod_list:
        dep_name = pod_str_from_dict(dep_name)
        name = real_pod_name(dep_name, pod_name)
        if not name == pod_name:
            continue
        if name is not None:
            pm.name = name
        version = pod_version_from_dependency(dep_name)
        if version is not None:
            pm.version = version
        subspec = pod_subspec_from_dependency(pod_name, dep_name)
        if subspec is not None:
            pm.sub_spec_list.append(subspec)
    if len(pm.name) == 0:
        print("{name} is not find".format(name=pod_name))
    return pm


def pod_version_from_dependency(dep_name):
    left = '('
    right = ')'
    start_index = dep_name.find(left) + len(left)
    end_index = dep_name.find(right)
    sub = dep_name[start_index:end_index]
    return sub


def pod_subspec_from_dependency(pod_name, dep_name):
    start_string = pod_name + '/'
    start_index = dep_name.find(start_string)
    if -1 == start_index:
        return None
    start_index += len(start_string)
    right_string = ' ('
    right_index = dep_name.find(right_string)
    sub_string = dep_name[start_index:right_index]
    return sub_string


def fetch_steady_pod_map_list(pod_list, full_pod_map):
    result_list = []
    dependency_list = full_pod_map['DEPENDENCIES']
    main_pods_list = full_pod_map['PODS']
    for pod_name in pod_list:
        if not isinstance(pod_name, str):
            continue
        pm = pod_model_from_dependencies(pod_name, main_pods_list)
        if len(pm.name) == 0:
            continue
        result_list.append(pm)
    return result_list


def sub_spec_string(sub_spec_list):
    index = 0
    sps = ''
    for sub_spec in sub_spec_list:
        sps += "'{name}'".format(name=sub_spec)
        if 0 != len(sub_spec_list) - 1:
            sps += ','
        index += 1
    return sps


def export_result(pod_map_list, result_path):
    if result_path is None or 0 == len(result_path):
        result_path = 'pickPodResult.txt'
    fo = open(result_path, "w")
    for pm in pod_map_list:
        pod_string = "pod '{name}','{version}'".format(name=pm.name, version=pm.version)
        if len(pm.sub_spec_list) > 0:
            sps = sub_spec_string(pm.sub_spec_list)
            pod_string += " , :subspecs=>[{sps}]".format(sps=sps)
        fo.write(pod_string)
        fo.write('\n')
    fo.close()

    print('pod pick result is writen in {path}'.format(path=result_path))

    return


def pod_name_list(pod_yaml_dict):
    spec_dict = pod_yaml_dict['SPEC CHECKSUMS']
    key_list = list(spec_dict.keys())
    return key_list


def execute_pick_pod(fullPodLockPath, subPodLockPath, resultPath):
    full_pod_map = read_yaml_map(fullPodLockPath)
    sub_pod_map = read_yaml_map(subPodLockPath)
    pod_lst = pod_name_list(sub_pod_map)
    trgt_pod_map_lst = fetch_steady_pod_map_list(pod_lst, full_pod_map)
    export_result(trgt_pod_map_lst, resultPath)

    return


def parse_args():
    description = "you should add those parameter"
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument('--main', help='主工程的Podfile.lock', required=True)
    parser.add_argument('--component', help='子模块demo工程的Podfile.lock', required=True)
    parser.add_argument('--result', help='输出结果的文件路径', default='resultPodfile')

    args = parser.parse_args()
    return args


def command_pick_pod_version():
    args = parse_args()
    execute_pick_pod(args.main, args.component, args.result)


if __name__ == '__main__':
    args = parse_args()
    print(args.main)
    print(args.component)
    print(args.result)

    # --main /Users/gujitao001/Documents/wangjie/user/IMPodfile.lock --component /Users/gujitao001/Documents/wangjie/user/UserPodfile.lock --result resultPath
    execute_pick_pod(args.main, args.component, args.result)
