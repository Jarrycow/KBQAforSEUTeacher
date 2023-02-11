import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Predict masks from input',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-jsonCollege', metavar='INPUT', type=str, default='./data/settings/college.json')  # 数据文件夹
    parser.add_argument('-schoolUrl', metavar='INPUT', type=str, default='seu.edu.cn')  # 学校
    return parser.parse_args()
    

