import numpy as np
from astropy.io import fits
import os


def save_image(calibrated_data, filename, save_folder):
    # 构建保存路径
    save_path = os.path.join(save_folder, f"dark_{filename}")

    # 保存对齐后的图像
    fits.writeto(save_path, calibrated_data, overwrite=True)
    print(f"Saved dark image: {save_path}")


def flat_calibration(input_folder, target_filename):
    flat_image = fits.getdata(target_filename)
    # 获取目标图像的数据类型
    target_dtype = flat_image.dtype

    # 创建掩码
    mask = np.ones(flat_image.shape)
    # 如果没有提供掩码，则创建一个与原始图像形状相同的掩码，其中所有像素的值均为 1。
    if mask is None:
        mask = np.ones(flat_image.shape)

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            original_image = fits.getdata(os.path.join(input_folder, filename))

            # 将平场图像应用于原始图像。
            calibrated_image = np.where(mask == 1, original_image / flat_image, )

            # 裁剪校准后的图像。
            calibrated_image = calibrated_image[:original_image.shape[0], :original_image.shape[1]]
            calibrated_data = calibrated_image.astype(target_dtype)

            yield calibrated_data, filename


def flat_calibration_data(calibrated_image, flat_image):
    # 获取目标图像的数据类型
    target_dtype = flat_image.dtype

    # 创建掩码
    mask = np.ones(flat_image.shape)
    # 如果没有提供掩码，则创建一个与原始图像形状相同的掩码，其中所有像素的值均为 1。
    if mask is None:
        mask = np.ones(flat_image.shape)

        # 将平场图像应用于原始图像。
        calibrated_image = np.where(mask == 1, calibrated_image / flat_image, )

        # 裁剪校准后的图像。
        calibrated_image = calibrated_image[:calibrated_image.shape[0], :calibrated_image.shape[1]]
        calibrated_data = calibrated_image.astype(target_dtype)

        yield calibrated_data


def dark_calibration(input_folder, target_filename):
    # 读取目标图像
    target_data = fits.getdata(target_filename)

    # 获取目标图像的数据类型
    target_dtype = target_data.dtype

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))

            # 执行暗场校准
            calibrated_image = current_data - target_data
            calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值

            # 将校准后的图像数据类型转换为与目标图像相同的数据类型
            calibrated_data = calibrated_image.astype(target_dtype)

            yield calibrated_data, filename


def dark_calibration_data(calibrated_image, dark_image):
    target_dtype = dark_image.dtype
    calibrated_image = calibrated_image - dark_image
    calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值
    calibrated_data = calibrated_image.astype(target_dtype)
    yield calibrated_data


def bias_calibration(input_folder, target_filename):
    # 读取目标图像
    target_data = fits.getdata(target_filename)

    # 获取目标图像的数据类型
    target_dtype = target_data.dtype

    # 遍历文件夹内所有fits文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".fits"):
            # 加载当前文件
            current_data = fits.getdata(os.path.join(input_folder, filename))

            # 执行偏置场校准
            calibrated_image = current_data - target_data
            calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值

            # 将校准后的图像数据类型转换为与目标图像相同的数据类型
            calibrated_data = calibrated_image.astype(target_dtype)

            yield calibrated_data, filename


def bias_calibration_data(calibrated_image, bias_image):
    target_dtype = bias_image.dtype
    calibrated_image = calibrated_image - bias_image
    calibrated_image[calibrated_image < 0] = 0  # 确保不会出现负值
    calibrated_data = calibrated_image.astype(target_dtype)
    yield calibrated_data

# # 使用示例
# for calibrated_data, filename in dark_calibration(input_folder, target_filename, save_folder):
#     save_dark_image(calibrated_data, filename, save_folder)
