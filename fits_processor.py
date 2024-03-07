import os
from tkinter import messagebox
import cv2
import numpy as np
from astropy.io import fits
from scipy.ndimage import median_filter


def apply_median_filter(input_image, kernel_size):
    """ 使用中值滤波器对输入图像进行降噪。 """
    return median_filter(input_image, size=kernel_size)


def gaussian_kernel(size, sigma):
    """ 生成二维高斯滤波器。 """
    kernel = np.fromfunction(
        lambda x, y: (1 / (2 * np.pi * sigma ** 2)) * np.exp(
            -((x - size // 2) ** 2 + (y - size // 2) ** 2) / (2 * sigma ** 2)),
        (size, size)
    )
    return kernel / np.sum(kernel)


def auto_adjust_sigma(image):
    # 计算图像梯度
    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

    # 根据梯度信息动态计算标准差
    sigma_space = np.median(gradient_magnitude) * 0.1
    sigma_color = np.std(image) * 0.1

    return sigma_space, sigma_color


def apply_bilateral_filter(image):
    """ 对图像应用双边滤波器。 """
    # 自动调整标准差
    sigma_space, sigma_color = auto_adjust_sigma(image)

    # 使用双边滤波
    bilateral_filtered_image = cv2.bilateralFilter(image, d=9, sigmaColor=sigma_color, sigmaSpace=sigma_space)

    return bilateral_filtered_image


def apply_gaussian_filter(image, kernel):
    """ 对图像应用高斯滤波器。 """
    return cv2.filter2D(image, -1, kernel)


def noise_image(input_folder_path, output_folder_path, method_combobox, kernel_size_entry):
    # 获取method_combobox的值
    selected_method = method_combobox.get()

    # 检查selected_method的合法性
    if selected_method not in ['median', 'gaussian', 'bilateral']:
        # 显示错误信息
        messagebox.showerror("错误", "不支持的降噪方法")
        return

    # 读取输入文件夹中的FITS图像并进行降噪
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".fits"):
            # 读取当前文件
            current_data = fits.getdata(os.path.join(input_folder_path, filename))
            input_dtype = current_data.dtype

            # 根据选择的方法进行降噪
            if selected_method == 'median':
                processed_image = apply_median_filter(current_data, int(kernel_size_entry.get()))
            elif selected_method == 'gaussian':
                kernel_size = int(kernel_size_entry.get())
                sigma = 2
                kernel = gaussian_kernel(kernel_size, sigma)
                processed_image = apply_gaussian_filter(current_data, kernel)
            elif selected_method == 'bilateral':
                processed_image = apply_bilateral_filter(current_data)

            processed_data = processed_image.astype(input_dtype)

            # 保存处理后的图像到输出文件夹
            save_path = os.path.join(output_folder_path, f"noise_{filename}")
            fits.writeto(save_path, processed_data, overwrite=True)

    # 显示成功信息
    messagebox.showinfo("图像已降噪并保存", "图像已成功降噪并保存")

