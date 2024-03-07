import os

import astroalign as aa
import cv2
import numpy as np
from astropy.io import fits

import calibrate
from bayer import read_fits, bayer_sequence, save_fits_rgb
from fits_processor import apply_bilateral_filter


def color_image(input_folder, output_folder, flat_fits, dark_fits, bias_fits, target_fits
                ):
    global img, calibrated_image
    base_filename = 'BlackImage'
    fits_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.fits')]

    if not fits_files:
        print("在指定的文件夹中找不到FITS文件。")
        return

    # 读取目标图像
    target_data = fits.getdata(target_fits)

    # 获取目标图像的数据类型
    target_dtype = target_data.dtype

    # 初始化叠加图像
    stacked_data_list = []

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 读取FITS文件数据
            fits_data = read_fits(os.path.join(input_folder, filename))
            # 双边降噪图像
            bilateral_data = apply_bilateral_filter(fits_data)
            # 对齐图像
            aligned_data, _ = aa.register(bilateral_data, target_data)
            # 将对齐后的图像数据类型转换为与目标图像相同的数据类型
            aligned_data = aligned_data.astype(target_dtype)
            # 平场校准
            # 暗场校准
            dark_data = calibrate.dark_calibration_data(aligned_data, dark_fits)
            # 偏置场校准
            bias_data = calibrate.dark_calibration_data(dark_data, bias_fits)

            # 直方图均值拉伸
            equalized_image = cv2.equalizeHist(bias_data)

            # 将处理好的图像输入到 list 中
            stacked_data_list.append(equalized_image)

    stacked_data = np.sum(stacked_data_list, axis=0) / len(fits_files)

    if stacked_data.dtype != np.uint8:
        img = stacked_data.astype(np.uint8)

    # 构造新的输出文件名
    existing_files = [file for file in os.listdir(output_folder) if file.startswith(base_filename)]
    num_existing_files = len(existing_files)
    output_filename = f'{base_filename}_{num_existing_files + 1}.fits'

    # 构建保存路径
    save_path = os.path.join(output_folder, output_filename)

    # 保存图像
    save_fits_rgb(img, save_path)
    print(f"Saved black image: {save_path}")

# if __name__ == "__main__":
#     # 设定参数
#     input_folder = "E:/Image/QHY5III715C/19_22_21"
#     output_folder = "E:/Image/QHY5III715C/3"
#     flat_folder = "E:/Image/QHY5III715C/19_24_15/Capture_00001.fits"
#     dark_folder = "E:/Image/QHY5III715C/19_24_15/Capture_00002.fits"
#     bias_folder = "E:/Image/QHY5III715C/19_24_15/Capture_00003.fits"
#     target_folder = "E:/Image/QHY5III715C/Capture_00016.fits"
#
#     # 运行程序
#     color_image(input_folder, output_folder, flat_folder, dark_folder, bias_folder, target_folder)
