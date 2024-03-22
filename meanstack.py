import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from astropy.io import fits
import dask.array as da
import dask


def mean_stack_worker(args):
    fits_file, dtype = args
    with fits.open(fits_file) as hdul:
        data = hdul[0].data.astype(np.float64)
    return data


def median_stack_worker(args):
    fits_file, dtype = args
    with fits.open(fits_file) as hdul:
        data = hdul[0].data.astype(np.float64)
    return np.median(data, axis=0)


def max_stack_worker(args):
    fits_file, dtype = args
    with fits.open(fits_file) as hdul:
        data = hdul[0].data.astype(np.float64)
    return np.max(data, axis=0)


def min_stack_worker(args):
    fits_file, dtype = args
    with fits.open(fits_file) as hdul:
        data = hdul[0].data.astype(np.float64)
    return np.min(data, axis=0)


def sum_stack_worker(args):
    fits_file, dtype = args
    with fits.open(fits_file) as hdul:
        data = hdul[0].data.astype(np.float64)
    return np.sum(data, axis=0)


def mean_stack(input_folder):
    fits_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.fits')]

    if not fits_files:
        print("在指定的文件夹中找不到FITS文件。")
        return

    # 读取第一个FITS文件获取头文件信息和数据类型
    with fits.open(fits_files[0]) as hdul:
        header = hdul[0].header
        data_type = hdul[0].data.dtype  # 获取数据类型
        shape = hdul[0].data.shape  # 获取数据形状

    chunk_size = 10  # 每次处理10个文件
    results = []
    for i in range(0, len(fits_files), chunk_size):
        chunk_files = fits_files[i:i + chunk_size]
        fits_arrays = [da.from_delayed(dask.delayed(fits.getdata)(f, header=False),
                                       shape=shape, dtype=data_type)
                       for f in chunk_files]
        chunk_result = da.stack(fits_arrays, axis=0).mean(axis=0).compute()
        results.append(chunk_result)

    stacked_data = np.mean(results, axis=0)
    return stacked_data, header, data_type


def median_stack(input_folder):
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


def max_stack(input_folder):
    # 1. 遍历输入文件夹中的所有 FITS 文件
    fits_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.fits')]

    if not fits_files:
        print("在指定的文件夹中找不到FITS文件。")
        return

    # 2. 读取第一个 FITS 文件作为参考
    with fits.open(fits_files[0]) as hdul:
        header = hdul[0].header
        data_shape = hdul[0].data.shape  # 获取数据形状
        reference_data = hdul[0].data  # 获取参考数据

    # 3. 初始化堆叠数据
    stacked_data = np.zeros(data_shape, dtype=np.float32)

    # 4. 遍历每个像素位置
    for i in range(data_shape[0]):
        for j in range(data_shape[1]):
            # 5. 获取每个像素位置的所有值
            pixel_values = [fits_file[i, j] for fits_file in map(fits.getdata, fits_files)]

            # 6. 与参考数据比较，取较大值
            stacked_data[i, j] = np.max([reference_data[i, j]] + pixel_values)

    # 7. 读取第一个 FITS 文件获取数据类型
    with fits.open(fits_files[0]) as hdul:
        data_type = hdul[0].data.dtype  # 获取数据类型

    return stacked_data, header, data_type


def min_stack(input_folder):
    # 1. 遍历输入文件夹中的所有 FITS 文件
    fits_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.fits')]

    if not fits_files:
        print("在指定的文件夹中找不到FITS文件。")
        return

    # 2. 读取第一个 FITS 文件作为参考
    with fits.open(fits_files[0]) as hdul:
        header = hdul[0].header
        data_shape = hdul[0].data.shape  # 获取数据形状
        reference_data = hdul[0].data  # 获取参考数据

    # 3. 初始化堆叠数据
    stacked_data = np.zeros(data_shape, dtype=np.float32)

    # 4. 遍历每个像素位置
    for i in range(data_shape[0]):
        for j in range(data_shape[1]):
            # 5. 获取每个像素位置的所有值
            pixel_values = [fits_file[i, j] for fits_file in map(fits.getdata, fits_files)]

            # 6. 与参考数据比较，取较大值
            stacked_data[i, j] = np.min([reference_data[i, j]] + pixel_values)

    # 7. 读取第一个 FITS 文件获取数据类型
    with fits.open(fits_files[0]) as hdul:
        data_type = hdul[0].data.dtype  # 获取数据类型

    return stacked_data, header, data_type


def sum_stack(input_folder):
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
    stacked_data = np.sum(stacked_data_list, axis=0)

    return stacked_data, header, data_type


def save_fits(stacked_data, header, data_type, output_folder, base_filename='Stack'):
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


def stack_image(input_folder_path, output_folder_path, method_combobox, ):
    # 获取method_combobox的值
    global stacked_data, header, data_type
    selected_method = method_combobox.get()
    if selected_method == 'mean_stack':
        stacked_data, header, data_type = mean_stack(input_folder_path)
    elif selected_method == 'median_stack':
        stacked_data, header, data_type = median_stack(input_folder_path)
    elif selected_method == 'max_stack':
        stacked_data, header, data_type = max_stack(input_folder_path)
    elif selected_method == 'min_stack':
        stacked_data, header, data_type = min_stack(input_folder_path)
    elif selected_method == 'sum_stack':
        stacked_data, header, data_type = sum_stack(input_folder_path)

    save_fits(stacked_data, header, data_type, output_folder_path)
