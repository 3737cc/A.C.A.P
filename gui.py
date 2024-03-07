import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import aligned
import calibrate
import fits_processor
import color
import meanstack
import bayer


# 降噪相关函数实现
def noise_image(input_folder_path, output_folder_path, method_combobox, kernel_size_entry):
    # 获取method_combobox的值
    selected_method = method_combobox.get()

    # 检查selected_method的合法性
    if selected_method not in ['median', 'gaussian', 'bilateral']:
        # 显示错误信息或采取其他适当的操作
        messagebox.showerror("错误", "不支持的降噪方法")
        return

    # 调用fits_processor.noise_image函数时，将StringVar转换为字符串
    fits_processor.noise_image(input_folder_path.get(), output_folder_path.get(), method_combobox, kernel_size_entry)

    # 显示成功信息
    messagebox.showinfo("图像已降噪并保存", "图像已成功降噪并保存")


# 校准所需函数
def calibrate_image(target_file_path, flat_files_path, dark_files_path, bias_files_path, output_folder_path):
    for calibrated_data, filename in calibrate.flat_calibration(target_file_path, flat_files_path):
        calibrated_data = calibrate.dark_calibration(calibrated_data, dark_files_path)
        calibrated_data = calibrate.bias_calibration(calibrated_data, bias_files_path)
        calibrate.save_image(calibrated_data, filename, output_folder_path)
    messagebox.showinfo("一键校准完成", "图像已成功校准并保存！")


def flat_calibrate_image(target_file_path, flat_files_path, output_folder_path):
    for calibrated_data, filename in calibrate.flat_calibration(flat_files_path, target_file_path):
        calibrate.save_image(calibrated_data, filename, output_folder_path)
    messagebox.showinfo("平场校准完成", "图像已成功校准并保存！")


def dark_calibrate_image(target_file_path, dark_files_path, output_folder_path):
    for calibrated_data, filename in calibrate.dark_calibration(dark_files_path, target_file_path):
        calibrate.save_image(calibrated_data, filename, output_folder_path)
    messagebox.showinfo("暗场校准完成", "图像已成功校准并保存！")


def bias_calibrate_image(target_file_path, bias_files_path, output_folder_path):
    for calibrated_data, filename in calibrate.bias_calibration(bias_files_path, target_file_path):
        calibrate.save_image(calibrated_data, filename, output_folder_path)
    messagebox.showinfo("偏置场校准完成", "图像已成功校准并保存！")


# 对齐所需函数
def align_and_save(target_file_path, input_folder_path, output_folder_path):
    aligned.align_all(target_file_path, input_folder_path)
    for aligned_data, filename in aligned.align_all(target_file_path, input_folder_path):
        aligned.save_all(aligned_data, filename, output_folder_path)
    aligned.process_fits_images(target_file_path, output_folder_path, output_folder_path)
    messagebox.showinfo("对齐完成", "图像已成功对齐并保存！")


# 叠加相关函数实现
def stack_button(input_folder_path, output_folder_path, method_combobox):
    # 获取method_combobox的值
    selected_method = method_combobox.get()

    # 检查selected_method的合法性
    if selected_method not in ['mean_stack', 'median_stack', 'max_stack', 'min_stack', 'sum_stack']:
        # 显示错误信息或采取其他适当的操作
        messagebox.showerror("错误", "不支持的叠加方法")
        return

    # 调用stack_image函数时，将StringVar转换为字符串
    meanstack.stack_image(input_folder_path.get(), output_folder_path.get(), method_combobox)

    # 显示成功信息
    messagebox.showinfo("图像已堆叠并保存", "图像已成功堆叠并保存")


# 进行解拜尔序列相关实现
def bayer_button(input_folder_path, output_folder_path, ):
    bayer.bayer_image(input_folder_path, output_folder_path)
    messagebox.showinfo("一键出图完成", "图像已成功保存")


# 自动一键式彩色出图

def automatic_color_button(input_folder, output_folder, flat_folder, dark_folder, bias_folder, target_folder):
    color.color_image(input_folder, output_folder, flat_folder, dark_folder, bias_folder, target_folder)
    messagebox.showinfo("一键彩色出图完成", "图像已成功保存")


# 自动一键式黑白出图

def automatic_black_button(input_folder, output_folder, flat_folder, dark_folder, bias_folder, target_folder):
    color.color_image(input_folder, output_folder, flat_folder, dark_folder, bias_folder, target_folder)
    messagebox.showinfo("一键黑白出图完成", "图像已成功保存")


# 读取，打开，保存fits文件
def browse_target_file(target_file_path):
    file_path = filedialog.askopenfilename(filetypes=[("FITS 文件", "*.fits")])
    if file_path:
        target_file_path.set(file_path)


def browse_input_folder(input_folder_path):
    folder_path = filedialog.askdirectory()
    if folder_path:
        input_folder_path.set(folder_path)


def browse_output_folder(output_folder_path):
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_path.set(folder_path)


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图像处理应用")
        root.geometry("520x150+700+100")

        # 创建一级页面的按钮
        self.btn_goto_second_page = tk.Button(root, text="降噪功能", command=self.setup_noise_reduction_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(root, text="校准功能", command=self.setup_calibrate_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(root, text="对齐功能", command=self.setup_alignment_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(root, text="叠加功能", command=self.setup_meanstck_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(root, text="一键彩色出图", command=self.setup_bayer_page_wrapper_color)
        self.btn_goto_second_page.pack(side='top', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(root, text="一键黑白出图", command=self.setup_bayer_page_wrapper_black)
        self.btn_goto_second_page.pack(side='top', padx=20, pady=20)

    # 降噪ui界面相关实现
    def setup_noise_reduction_page_wrapper(self):
        # 销毁一级页面组件
        # self.destroy_current_page()

        # 创建一个新的窗口作为二级页面
        second_page_window = tk.Toplevel(self.root)
        second_page_window.title("降噪页面")
        second_page_window.geometry("490x350+1320+600")
        self.setup_noise_reduction_page(second_page_window)

    def setup_noise_reduction_page(self, frame):
        tk.Label(frame, text="选择降噪方法:").grid(row=0, column=0, padx=10, pady=10)

        method_combobox = ttk.Combobox(frame, values=['median', 'gaussian', 'bilateral'])
        method_combobox.grid(row=0, column=1, padx=10, pady=10)
        method_combobox.current(0)  # 设置默认值为中值滤波

        input_folder_path = tk.StringVar()
        tk.Label(frame, text="输入文件夹:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=input_folder_path, state='readonly').grid(row=1, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_input_folder(input_folder_path)).grid(row=1, column=2)

        output_folder_path = tk.StringVar()
        tk.Label(frame, text="输出文件夹:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=output_folder_path, state='readonly').grid(row=2, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_output_folder(output_folder_path)).grid(row=2,
                                                                                                     column=2)

        tk.Label(frame, text="核心大小:").grid(row=3, column=0, padx=10, pady=10)

        kernel_size_entry = tk.Entry(frame)
        kernel_size_entry.insert(0, "3")  # 默认值为3
        kernel_size_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(frame, text="开始降噪",
                  command=lambda: noise_image(input_folder_path, output_folder_path, method_combobox,
                                              kernel_size_entry)).grid(
            row=4, column=1, padx=10, pady=10)

        status_label = tk.Label(frame, text="")
        status_label.grid(row=5, column=1, padx=10, pady=10)

        # 添加返回按钮
        btn_back = tk.Button(frame, text="返回主页面", command=self.back_to_first_page)
        btn_back.grid(row=6, column=1, pady=20)

    # 校准ui界面相关实现
    def setup_calibrate_page_wrapper(self):
        # 销毁一级页面组件
        # self.destroy_current_page()
        # 创建一个新的窗口作为二级页面
        second_page_window = tk.Toplevel(self.root)
        second_page_window.title("校准页面")
        second_page_window.geometry("500x400+1320+100")
        self.setup_calibrate_page(second_page_window)

    def setup_calibrate_page(self, frame):
        tk.Label(frame, text="选择平场FITS文件:").grid(row=0, column=0)
        falt_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=falt_file_path, state='readonly').grid(row=0, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(falt_file_path)).grid(row=0, column=2)

        tk.Label(frame, text="选择暗场FITS文件:").grid(row=1, column=0)
        dark_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=dark_file_path, state='readonly').grid(row=1, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(dark_file_path)).grid(row=1, column=2)

        tk.Label(frame, text="选择偏置场FITS文件:").grid(row=2, column=0)
        bias_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=bias_file_path, state='readonly').grid(row=2, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(bias_file_path)).grid(row=2, column=2)

        input_folder_path = tk.StringVar()
        tk.Label(frame, text="输入文件夹:").grid(row=3, column=0)
        tk.Entry(frame, textvariable=input_folder_path, state='readonly').grid(row=3, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_input_folder(input_folder_path)).grid(row=3, column=2)

        output_folder_path = tk.StringVar()
        tk.Label(frame, text="输出文件夹:").grid(row=4, column=0)
        tk.Entry(frame, textvariable=output_folder_path, state='readonly').grid(row=4, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_output_folder(output_folder_path)).grid(row=4,
                                                                                                     column=2)

        tk.Button(frame, text="一键校准并保存",
                  command=lambda: calibrate_image(input_folder_path.get(), falt_file_path.get(),
                                                  dark_file_path.get(), bias_file_path.get(),
                                                  output_folder_path.get())).grid(row=5, column=1)

        tk.Button(frame, text="平场校准并保存",
                  command=lambda: flat_calibrate_image(input_folder_path.get(), falt_file_path.get(),
                                                       output_folder_path.get())).grid(row=0, column=4)

        tk.Button(frame, text="暗场校准并保存",
                  command=lambda: dark_calibrate_image(input_folder_path.get(), dark_file_path.get(),
                                                       output_folder_path.get())).grid(row=1, column=4)

        tk.Button(frame, text="偏置场校准并保存",
                  command=lambda: bias_calibrate_image(input_folder_path.get(), bias_file_path.get(),
                                                       output_folder_path.get())).grid(row=2, column=4)

        btn_back = tk.Button(frame, text="返回主页面", command=self.back_to_first_page)
        btn_back.grid(row=6, column=1, pady=20)

    # 对齐ui界面相关实现
    def setup_alignment_page_wrapper(self):
        # 销毁一级页面组件
        # self.destroy_current_page()
        # 创建一个新的窗口作为二级页面
        second_page_window = tk.Toplevel(self.root)
        second_page_window.title("对齐页面")
        second_page_window.geometry("300x200+300+400")
        self.setup_alignment_page(second_page_window)

    def setup_alignment_page(self, frame):
        target_file_path = tk.StringVar()
        tk.Label(frame, text="目标 FITS 文件:").grid(row=0, column=0)
        tk.Entry(frame, textvariable=target_file_path, state='readonly').grid(row=0, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(target_file_path)).grid(row=0, column=2)

        input_folder_path = tk.StringVar()
        tk.Label(frame, text="输入文件夹:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=input_folder_path, state='readonly').grid(row=1, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_input_folder(input_folder_path)).grid(row=1, column=2)

        output_folder_path = tk.StringVar()
        tk.Label(frame, text="输出文件夹:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=output_folder_path, state='readonly').grid(row=2, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_output_folder(output_folder_path)).grid(row=2,
                                                                                                     column=2)

        tk.Button(frame, text="对齐并保存",
                  command=lambda: align_and_save(target_file_path.get(), input_folder_path.get(),
                                                 output_folder_path.get())).grid(row=3, column=1)

        # 添加返回按钮
        btn_back = tk.Button(frame, text="返回主页面", command=self.back_to_first_page)
        btn_back.grid(row=6, column=1, pady=20)

    # 叠加ui页面相关实现
    def setup_meanstck_page_wrapper(self):
        # 销毁一级页面组件
        # self.destroy_current_page()
        # 创建一个新的窗口作为二级页面
        second_page_window = tk.Toplevel(self.root)
        second_page_window.title("叠加页面")
        second_page_window.geometry("400x200+200+100")
        self.setup_meanstck_page(second_page_window)

    def setup_meanstck_page(self, frame):
        tk.Label(frame, text="选择叠加方法:").grid(row=0, column=0, padx=10, pady=10)

        method_combobox = ttk.Combobox(frame,
                                       values=['mean_stack', 'median_stack', 'max_stack', 'min_stack', 'sum_stack'])
        method_combobox.grid(row=0, column=1, padx=10, pady=10)
        method_combobox.current(0)

        browse_button = tk.StringVar()
        tk.Label(frame, text="输入文件夹:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=browse_button, state='readonly').grid(row=1, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_input_folder(browse_button)).grid(row=1, column=2)

        browse_output_button = tk.StringVar()
        tk.Label(frame, text="输出文件夹:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=browse_output_button, state='readonly').grid(row=2, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_output_folder(browse_output_button)).grid(row=2,
                                                                                                       column=2)

        tk.Button(frame, text="堆叠并保存",
                  command=lambda: stack_button(browse_button, browse_output_button,
                                               method_combobox, )).grid(row=3, column=1)

        # 添加返回按钮
        btn_back = tk.Button(frame, text="返回主页面", command=self.back_to_first_page)
        btn_back.grid(row=6, column=1, pady=20)

    def setup_bayer_page_wrapper_color(self):
        # 销毁一级页面组件
        # self.destroy_current_page()
        # 创建一个新的窗口作为二级页面
        second_page_window = tk.Toplevel(self.root)
        second_page_window.title("一键出RGB图页面")
        second_page_window.geometry("520x600+700+350")
        self.setup_bayer_page_color(second_page_window)

    def setup_bayer_page_color(self, frame):
        target_file_path = tk.StringVar()
        tk.Label(frame, text="输入目标文件:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=target_file_path, state='readonly').grid(row=1, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(target_file_path)).grid(row=1, column=2)

        browse_button = tk.StringVar()
        tk.Label(frame, text="输入文件夹:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=browse_button, state='readonly').grid(row=2, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_input_folder(browse_button)).grid(row=2, column=2)

        browse_output_button = tk.StringVar()
        tk.Label(frame, text="输出文件夹:").grid(row=3, column=0)
        tk.Entry(frame, textvariable=browse_output_button, state='readonly').grid(row=3, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_output_folder(browse_output_button)).grid(row=3, column=2)

        tk.Label(frame, text="选择平场FITS文件:").grid(row=4, column=0)
        falt_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=falt_file_path, state='readonly').grid(row=4, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(falt_file_path)).grid(row=4, column=2)

        tk.Label(frame, text="选择暗场FITS文件:").grid(row=5, column=0)
        dark_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=dark_file_path, state='readonly').grid(row=5, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(dark_file_path)).grid(row=5, column=2)

        tk.Label(frame, text="选择偏置场FITS文件:").grid(row=6, column=0)
        bias_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=bias_file_path, state='readonly').grid(row=6, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(bias_file_path)).grid(row=6, column=2)

        tk.Button(frame, text="一键出图",
                  command=lambda: automatic_color_button(browse_button.get(), browse_output_button.get(),
                                                         falt_file_path.get(),
                                                         dark_file_path.get(), bias_file_path.get(),
                                                         target_file_path.get(), )).grid(row=7, column=1)

        # 添加返回按钮
        btn_back = tk.Button(frame, text="返回主页面", command=self.back_to_first_page)
        btn_back.grid(row=8, column=1, pady=20)

    def setup_bayer_page_wrapper_black(self):
        # 销毁一级页面组件
        # self.destroy_current_page()
        # 创建一个新的窗口作为二级页面
        second_page_window = tk.Toplevel(self.root)
        second_page_window.title("一键出黑白图页面")
        second_page_window.geometry("520x600+700+350")
        self.setup_bayer_page_black(second_page_window)

    def setup_bayer_page_black(self, frame):
        target_file_path = tk.StringVar()
        tk.Label(frame, text="输入目标文件:").grid(row=1, column=0)
        tk.Entry(frame, textvariable=target_file_path, state='readonly').grid(row=1, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(target_file_path)).grid(row=1, column=2)

        browse_button = tk.StringVar()
        tk.Label(frame, text="输入文件夹:").grid(row=2, column=0)
        tk.Entry(frame, textvariable=browse_button, state='readonly').grid(row=2, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_input_folder(browse_button)).grid(row=2, column=2)

        browse_output_button = tk.StringVar()
        tk.Label(frame, text="输出文件夹:").grid(row=3, column=0)
        tk.Entry(frame, textvariable=browse_output_button, state='readonly').grid(row=3, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_output_folder(browse_output_button)).grid(row=3, column=2)

        tk.Label(frame, text="选择平场FITS文件:").grid(row=4, column=0)
        falt_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=falt_file_path, state='readonly').grid(row=4, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(falt_file_path)).grid(row=4, column=2)

        tk.Label(frame, text="选择暗场FITS文件:").grid(row=5, column=0)
        dark_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=dark_file_path, state='readonly').grid(row=5, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(dark_file_path)).grid(row=5, column=2)

        tk.Label(frame, text="选择偏置场FITS文件:").grid(row=6, column=0)
        bias_file_path = tk.StringVar()
        tk.Entry(frame, textvariable=bias_file_path, state='readonly').grid(row=6, column=1)
        tk.Button(frame, text="浏览", command=lambda: browse_target_file(bias_file_path)).grid(row=6, column=2)

        tk.Button(frame, text="一键出图",
                  command=lambda: automatic_black_button(browse_button.get(), browse_output_button.get(),
                                                         falt_file_path.get(),
                                                         dark_file_path.get(), bias_file_path.get(),
                                                         target_file_path.get(), )).grid(row=7, column=1)

        # 添加返回按钮
        btn_back = tk.Button(frame, text="返回主页面", command=self.back_to_first_page)
        btn_back.grid(row=8, column=1, pady=20)

    # 销毁当前页面
    def destroy_current_page(self):
        # 遍历当前页面的所有部件并销毁它们
        for widget in self.root.winfo_children():
            widget.destroy()

    # 返回一级ui界面
    def back_to_first_page(self):
        # 销毁二级页面的部件
        self.destroy_current_page()

        # 重新创建一级页面的部件
        self.btn_goto_second_page = tk.Button(self.root, text="降噪功能",
                                              command=self.setup_noise_reduction_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(self.root, text="校准功能", command=self.setup_calibrate_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=60)

        self.btn_goto_second_page = tk.Button(self.root, text="对齐功能",
                                              command=self.setup_alignment_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=40)

        self.btn_goto_second_page = tk.Button(self.root, text="叠加功能", command=self.setup_meanstck_page_wrapper)
        self.btn_goto_second_page.pack(side='left', padx=20, pady=60)

        self.btn_goto_second_page = tk.Button(self.root, text="一键彩色出图",
                                              command=self.setup_bayer_page_wrapper_color)
        self.btn_goto_second_page.pack(side='top', padx=20, pady=20)

        self.btn_goto_second_page = tk.Button(self.root, text="一键黑白出图",
                                              command=self.setup_bayer_page_wrapper_black)
        self.btn_goto_second_page.pack(side='top', padx=20, pady=20)
