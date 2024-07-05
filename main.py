import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def read_file_and_calculate():
    file_path = filedialog.askopenfilename() #selecting a file from filedialog
    try:
        with open(file_path, 'r') as file:
            numbers = [int(line.strip()) for line in file]
            total = sum(numbers)
            average = total / len(numbers)
            minimum = min(numbers)
            maximum = max(numbers)
            
            print(f"Sum: {total}")
            print(f"Average: {average}")
            print(f"Minimum: {minimum}")
            print(f"Maximum: {maximum}")
            
            messagebox.showinfo("File Stats", f"Sum: {total}\nAverage: {average}\nMinimum: {minimum}\nMaximum: {maximum}")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except ValueError:
        print("The file contains non-numeric data.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_random_numbers(count, start, end):
    numbers = [random.randint(start, end) for _ in range(count)] #random numbers is generated
    with open('random_numbers.txt', 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")
    print(numbers)
    os.system('open random_numbers.txt')

def apply_standard_scaler(matrix):
    scaler = StandardScaler() 
    return scaler.fit_transform(matrix)

def apply_min_max_scaler(matrix):
    scaler = MinMaxScaler()
    return scaler.fit_transform(matrix)

def log_transform(matrix): #(log(value + 1)) to reduce skewness
    return np.log1p(matrix)  #log1p for avoiding log(0)

def get_normalization_method(data_type):
    if data_type == 'standard':
        return apply_standard_scaler
    elif data_type == 'min-max':
        return apply_min_max_scaler
    elif data_type == 'log':
        return log_transform
    else:
        raise ValueError(f"Unknown datatype: {data_type}")

def perform_matrix_operations():
    file1_path = filedialog.askopenfilename(title="Select First Matrix File")
    file2_path = filedialog.askopenfilename(title="Select Second Matrix File")
    
    try:
       # Load the matrices from files you choose
        matrix1 = np.loadtxt(file1_path, delimiter=' ')
        matrix2 = np.loadtxt(file2_path, delimiter=' ')
        
        #normalization method
        normalization_method = get_normalization_method('standard')  # Change 'standard' to 'min-max' or 'log' as needed
        
        # Applying normalization to matrices
        matrix1_normalized = normalization_method(matrix1)
        matrix2_normalized = normalization_method(matrix2)
        
        matrix_sum_normalized = matrix1_normalized + matrix2_normalized
        matrix_diff_normalized = matrix1_normalized - matrix2_normalized
        matrix_prod_normalized = np.dot(matrix1_normalized, matrix2_normalized)
        
        print("Matrix Sum:")
        print(matrix_sum_normalized)
        print("Matrix Difference:")
        print(matrix_diff_normalized)
        print("Matrix Product:")
        print(matrix_prod_normalized)
        
        messagebox.showinfo("Matrix Operations", f"Matrix Sum:\n{matrix_sum_normalized}\n\nMatrix Difference:\n{matrix_diff_normalized}\n\nMatrix Product:\n{matrix_prod_normalized}")
    except Exception as e:
        print(f"An error occurred: {e}")

root = tk.Tk()
root.title("GUI")

frame = tk.Frame(root)
frame.pack(pady=20)

load_file_button = tk.Button(frame, text="Load File and Display Stats", command=read_file_and_calculate)
load_file_button.grid(row=0, column=0, padx=10)

tk.Label(frame, text="Count:").grid(row=1, column=0, sticky='e')
count_entry = tk.Entry(frame)
count_entry.grid(row=1, column=1, padx=5)

tk.Label(frame, text="Start:").grid(row=2, column=0, sticky='e')
start_entry = tk.Entry(frame)
start_entry.grid(row=2, column=1, padx=5)

tk.Label(frame, text="End:").grid(row=3, column=0, sticky='e')
end_entry = tk.Entry(frame)
end_entry.grid(row=3, column=1, padx=5)

generate_numbers_button = tk.Button(frame, text="Generate Random Numbers", command=lambda: generate_random_numbers(int(count_entry.get()), int(start_entry.get()), int(end_entry.get())))
generate_numbers_button.grid(row=4, column=0, columnspan=2, pady=10)

matrix_operations_button = tk.Button(frame, text="Perform Matrix Operations", command=perform_matrix_operations)
matrix_operations_button.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
