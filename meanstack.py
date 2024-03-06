import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from astropy.io import fits


def mean_stack_worker(args):
    fits_file, dtype = args
    with fits.open(fits_file) as hdul:
        data = hdul[0].data.astype(np.float64)
    return data


def mean_stack(input_folder):
    fits_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.fits')]

    if not fits_files:
        print("在指定的文件夹中找不到FITS文件。")
        return

    # 读取第一个FITS文件获取头文件信息和数据类型
    with fits.open(fits_files[0]) as hdul:
        header = hdul[0].header
        data_type = hdul[0].data.dtype  # 获取数据类型

    # 使用ThreadPoolExecutor并行加载FITS文件
    with ThreadPoolExecutor() as executor:
        # 提交任务，每个任务加载一个FITS文件
        tasks = [(fits_file, data_type) for fits_file in fits_files]
        stacked_data_list = list(executor.map(mean_stack_worker, tasks))

    # 将加载的数据堆叠并计算均值
    stacked_data = np.sum(stacked_data_list, axis=0) / len(fits_files)

    return stacked_data, header, data_type


def save_fits(stacked_data, header, data_type, output_folder, base_filename='MeanStack'):
    existing_files = [file for file in os.listdir(output_folder) if file.startswith(base_filename)]
    num_existing_files = len(existing_files)

    # 构造新的输出文件名
    output_filename = f'{base_filename}_{num_existing_files + 1}.fits'

    # 创建新的HDU并保存为新的FITS文件，使用原始数据类型
    output_file = os.path.join(output_folder, output_filename)
    hdu = fits.PrimaryHDU(stacked_data.astype(data_type), header=header)
    hdulist = fits.HDUList([hdu])

    # 保存文件
    hdulist.writeto(output_file, overwrite=True)

    print(f"堆叠完成。结果保存在 {output_file}")

# 调用示例
# stacked_data, header, data_type = mean_stack(input_folder, output_folder)
# save_fits(stacked_data, header, data_type, output_folder)
