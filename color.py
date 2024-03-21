import os

import astroalign
import numpy as np
from astropy.io import fits

import bayer
import fits_processor
import calibrate


def color_image(input_folder: str, output_folder: str, flat_folder: str = None, dark_folder: str = None, bias_folder: str = None, target_folder: str = None):
    """一键式彩色出图。

    此函数将输入文件夹中的所有 FITS 文件对齐、校准、解拜耳化并保存为彩色图像。

    参数：
        input_folder: 输入文件夹的路径。
        output_folder: 输出文件夹的路径。
        flat_folder: 平场图像的路径（可选）。
        dark_folder: 暗场图像的路径（可选）。
        bias_folder: 偏置场图像的路径（可选）。
        target_folder: 目标图像的路径（可选）。
    """

    # 检查输入的文件夹是否存在
    if not os.path.isdir(input_folder):
        raise ValueError(f"输入文件夹不存在：{input_folder}")
    if not os.path.isdir(output_folder):
        raise ValueError(f"输出文件夹不存在：{output_folder}")

    # 加载平场、暗场和偏置场图像（如果提供了路径）
    flat_image = None
    dark_image = None
    bias_image = None
    if flat_folder is not None:
        flat_image = fits.getdata(flat_folder)
    if dark_folder is not None:
        dark_image = fits.getdata(dark_folder)
    if bias_folder is not None:
        bias_image = fits.getdata(bias_folder)

    # 遍历输入文件夹中的所有 FITS 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))

            # 校准图像
            calibrated_image = current_data
            if flat_image is not None:
                calibrated_image = calibrate.flat_calibration_data(calibrated_image, flat_image)
            if dark_image is not None:
                calibrated_image = calibrate .dark_calibration_data(calibrated_image, dark_image)
            if bias_image is not None:
                calibrated_image = calibrate .bias_calibration_data(calibrated_image, bias_image)

            # 对齐图像
            if target_folder is not None:
                target_image = fits.getdata(target_folder)
                aligned_image, _ = astroalign.register(calibrated_image, target_image)
            else:
                aligned_image = calibrated_image

            # 解拜耳化
            bayer_image = bayer.bayer_sequence(aligned_image)

            # 保存彩色图像
            fits_rgb_data = np.transpose(bayer_image, (2, 0, 1))
            save_path = os.path.join(output_folder, f"color_{filename}")
            fits.writeto(save_path, fits_rgb_data, overwrite=True)

    print(f"彩色图像已保存至：{output_folder}")