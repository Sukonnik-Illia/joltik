import openpyxl
from openpyxl.styles import PatternFill

# Load the workbook and select the active worksheet
file_path = './Test_excel_file.xlsx'  # Path to Excel file
wb = openpyxl.load_workbook(file_path)

# Select the worksheet by name (replace 'Sheet1' with your sheet name)
sheet_name = 'Sheet1'  # Set the name of the worksheet you want to work with
ws = wb[sheet_name]

# Define a fill style for highlighting cells (e.g., red background for invalid cells)
highlight_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

# Column name to validate (assuming "Amount" is in one of the columns)
amount_column = None
error_list = []

# Find the "Amount" column (assuming it's in the first row)
for cell in ws[1]:
    if cell.value == "Amount":
        amount_column = cell.column_letter
        break

# If the "Amount" column is found, validate its values
if amount_column:
    # Start iterating from the second row (assuming the first row is the header)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=openpyxl.utils.column_index_from_string(amount_column), max_col=openpyxl.utils.column_index_from_string(amount_column)):
        cell = row[0]  # The only cell in this range
        try:
            # Check if the value is a float
            float(cell.value)
        except (ValueError, TypeError):
            # If not a float, highlight the cell
            cell.fill = highlight_fill
            # Append the error details (row and cell value) to the error list
            error_list.append(f"Row {cell.row}: Invalid value '{cell.value}' in Amount column")

else:
    print("Amount column not found")

# Add a new worksheet for error log
error_ws = wb.create_sheet("Error Log")

# Add the error list to the new worksheet
error_ws.append(["Error List"])
if error_list:
    for error in error_list:
        error_ws.append([error])
else:
    error_ws.append(["No errors found"])

# Save the modified Excel file with highlighted cells and error log
output_file = 'validated_data.xlsx'
wb.save(output_file)

print(f"Validation completed. File saved as {output_file}.")
