
import pandas as pd
import re
import io

def parse_grades_from_string(content_string):
    lines = content_string.splitlines()

    data = []
    i = 0
    while i < len(lines):
        # Skip any empty lines at the beginning of a potential entry
        if not lines[i].strip():
            i += 1
            continue

        # An entry consists of 3 non-empty lines
        # Line 1: Course Name
        # Line 2: Letter Grade (Numerical Value)
        # Line 3: Coefficient

        # Find the next three non-empty lines
        entry_lines = []
        j = i
        while len(entry_lines) < 3 and j < len(lines):
            stripped_line = lines[j].strip()
            if stripped_line:
                entry_lines.append(stripped_line)
            j += 1
        
        if len(entry_lines) == 3:
            course_name = entry_lines[0]
            grade_info = entry_lines[1]
            value_str = entry_lines[2]

            try:
                value = float(value_str)
            except ValueError:
                print(f"Could not parse value: {value_str} for entry: {entry_lines}")
                i = j # Move past the lines we just tried to process
                continue

            match = re.match(r'([A-E]|F|Fx) \((\d\.?\d*)\)', grade_info)
            if match:
                letter_grade = match.group(1)
                numerical_grade = float(match.group(2))
                data.append([course_name, letter_grade, numerical_grade, value])
                i = j # Move past the lines we just processed
            else:
                print(f"Could not parse grade_info: {grade_info} for entry: {entry_lines}")
                i = j # Move past the lines we just tried to process
        else:
            # If we couldn't find 3 non-empty lines, something is wrong with the remaining data
            print(f"Skipping malformed entry (could not find 3 non-empty lines): {entry_lines}")
            i = j # Move past the lines we just tried to process

    df = pd.DataFrame(data, columns=['Course', 'LetterGrade', 'NumericalGrade', 'Value'])
    return df

# Remove the main execution block for file parsing as it will now be handled by Streamlit
# if __name__ == '__main__':
#     df = parse_grades('/home/ubuntu/upload/pasted_content.txt')
#     df.to_csv('grades.csv', index=False)
#     print('Grades parsed and saved to grades.csv')


