import re

def str_sum(text, auto_space = False, gap = 8):
  '''
  function for concatenating a string
  -
    - `text` - string to be concatenated. list of strings or other iterable object containing strings.

    returns `sum`
    -

  How it works:
  -
  - This function takes a string or a list of strings as input.
  - It iterates through each character or string in the input and concatenates them with a space in between.
  - The final concatenated string is returned, with the last space character removed.
  '''
  if (type(text) == str) | (type(text) == list) | (type(text) == tuple):
    sum = ''

    if auto_space == False:
      for char in text:
        sum += char + ' '
      return sum[:-1]

    elif auto_space == True:
      for index, char in enumerate(text):
        if (index > 0) & (len(char) < gap):
          sum += ' '*(gap-len(char)) + char + ' '
        else:
          sum += char + ' '
      return sum[:-1]
  else:
    print('invalid input type! `text` must be a string or list of strings')

"""### file loader function"""

def file_loader(file_path):
  '''
  function for loading file
  -
    returns `file`, `file_name`, `file_path`
  -
  How it works:
  -
  - This function prompts the user for a file path.
  - It checks if the file has a `.txt` extension.
  - If the file is a text file, it opens the file, reads its contents, and closes the file.
  - It then extracts the file name from the file path and returns the file contents, file name, and file path.
  - If the file is not a text file, it prints an error message and calls itself recursively to prompt the user for a valid file path.
  '''

  file_name = re.split(r'[/\.\\]',file_path)[-1]

  # load txt file

  print(f"loading file at {file_path}  ...\n")
  with open(file_path, "r") as f:
      file = f.read()
      f.close()

  print(f'file name: {file_name}')
  return file, file_name, file_path


"""### data splitter function"""

# split file by line

def data_splitter(file):
  '''
  function for splitting file by line
  -
    - `file` - file contents

    retruns `data_head` and `data_body`

  How it works:
  -
  - The `data_splitter` function takes a text file as input and splits it into two parts: the header and the body.

  - The body is defined as the first line that starts with the letter "S" and all lines after. The header is defined as the lines before.

  - The function iterates through each line in the file and checks if it starts with the letter "S". If it does, the function sets the `data_head` variable to the lines in the file up to that point and the `data_body` variable to the remaining lines in the file.

  - The function then returns the `data_head` and `data_body` variables.
  '''

  # split data header from body

  for index, line in enumerate(file.splitlines()):
    if line.startswith('S'):
      data_head = file.splitlines()[:index]
      data_body = file.splitlines()[index:]
      break

  return data_head, data_body

"""### data cleaner function"""

# unpack dataset and correct anomalies

def data_cleaner(dataset):
  '''
  function for scanning for and removing anomalies
  -
    - `dataset` - data produced after splitting file by line

    returns `clean_data`
  -
  The `data_cleaner` function takes a dataset as input and scans for and removes anomalies.

  How it works:

  1. The function first iterates through the dataset and splits it into a list of source and receiver data.
  2. For each source, the function compares the index sequences of the receiver data.
  3. If the index suddenly drops or increases, the function annotates the data as an anomaly.
  4. The function then reassembles the data into three columns.
  5. The function drops the annotated rows.
  6. The function returns the clean data.
  '''

  marker_up, marker_dwn = ('000','000000 0000'), ('XXX', 'XXXXXX XXXX')

  data_list = []
  total_anoms = 0

  # sort data by source info
  for index, s_line in enumerate(dataset):

      if s_line.startswith('S'):
          annom_countr = 0

          supr_list = []
          inr_list = []

          # append source info to supr_list
          supr_list.append(s_line)

          # process receiver data, stop before next source number
          for r_line in dataset[index+1:]:
              if r_line.startswith('R'):
                  split_rx = r_line.split()[1:]

                  for inr_index in range(0, len(split_rx), 3):
                      inr_list.append((split_rx[inr_index],str_sum(split_rx[inr_index+1:inr_index+3], auto_space = True)))
                  continue
              else:
                  break

          # compare index sequences for anomalies: forward scan (1 - 240)
          ic_range = list(range(1,len(inr_list)+1)) # control number
          i_range = [int(i) for i,v in inr_list]    # rx station number

          for l_index, r_index in zip(ic_range, i_range):
              if r_index >= l_index:
                continue
              # if Rx index suddenly drops, annotate data
              elif r_index < l_index:
                inr_list[l_index - 1] = marker_up
                annom_countr += 1
                total_anoms += 1

          # compare index sequences for anomalies: reverse scan (240 - 1)
          ic_range.reverse(), i_range.reverse()

          for l_index, r_index in zip(ic_range, i_range):
            if l_index >= r_index:
              continue
            # if index suddenly increases, annotate data
            elif l_index < r_index:
              inr_list[l_index - 1] = marker_dwn
              annom_countr += 1
              total_anoms += 1

          supr_list.append(inr_list)
          data_list.append(supr_list)
          if annom_countr > 0:
            print(f'{annom_countr} anomalies discovered at {s_line}!')

          continue
      else:
          continue

  print(f'\n\ntotal anomalies detected: {total_anoms}')

  # reassemblying the data in 3 columns
  #
  annot_data = []

  for data in data_list:
    annot_data.extend([data[0]])


    one_line = ['R']

    for d_in,(station, point) in enumerate(data[1]):
      # if statements to adjust spacing based on station number
      if d_in < 9:
        one_line.append('  ' + station + ' ' + point + '    ')
      elif (d_in >= 9) & (d_in < 99):
        one_line.append(' ' + station + ' ' + point + '    ')
      elif d_in >= 99:
        one_line.append(station + ' ' + point + '    ')

      if len(one_line) == 4:
        annot_data.extend([str_sum(one_line[:])+' '])
        one_line = ['R']
      else:
        continue


  # clean data, dropping annotations
  #
  clean_data = []

  for data in annot_data:
    if data.split()[2].startswith('0') | data.split()[2].startswith('X'):     # <<<< ----- too much memory work
      continue
    else:
      clean_data.append(data)

  print('data cleaning complete!\n')
  print(f'Original data length: {len(annot_data)},\nClean data length: {len(clean_data)},\nTotal "R" rows dropped: {len(annot_data) - len(clean_data)}\n')

  return clean_data

"""### row trimmer function"""

# eliminate data with fewer than specified rows

def d_trimmer(data_to_cut, min_row = 70):
  '''
  function for dropping source data with fewer than specified number of rows
  -
    - `data_to_cut` - data produced after cleaning data with `data_cleaner()` function.
    - `min_row`     - defaults to 70 (i.e. 210 stations / 3 columns). minimum number of receiver rows to keep a source/receiver pair.

    returns `data_to_cut`
  -

  The `d_trimmer` function is designed to eliminate source data that has fewer than a specified number of rows.

  How it works:
  -
  1. The function iterates through the data and identifies source lines (`S`).
  2. For each source line, it counts the number of receiver rows (`R`) that follow it until the next source line is encountered.
  3. If the number of receiver lines is less than the specified minimum row count, the function adds the range of lines for that source to a list of sections to be dropped.
  4. Finally, the function iterates through the list of sections to be dropped in reverse order and removes them from the data.
  '''

  pre_len = len(data_to_cut)
  rows_2_drop = 0
  total_S = 0
  drop_at = []
  next_S_index = 0

  for index, source in enumerate(data_to_cut):
    if source.startswith('S'):
      total_S += 1
      for i_index, r_line in enumerate(data_to_cut[index+1:]):
        if r_line.startswith('R'):
          next_S_index = i_index + index + 2
          continue
        else:
          next_S_index = i_index + index + 1
          break

      if next_S_index - index < min_row:
        drop_at.append((index,next_S_index))
        print(f'data at "{source}" is too short ({next_S_index - index} rows)! eliminating...')
        rows_2_drop += 1
      else:
        continue
    else:
      continue


  # drop sections from bottom up
  drop_at.reverse()

  for top, bottom in drop_at:
    del(data_to_cut[top:bottom])

  print(f'\nPrevious data length: {pre_len},\nNew data length: {len(data_to_cut)}\nTotal sections dropped: {rows_2_drop}.\n')

  return data_to_cut

"""### deduplicator function"""

def deduplicator(cleaned_data):
  '''
  function for removing duplicate data from cleaned data; returns updated cleaned data after removing all duplicate data sections

    - `cleaned_data` - data produced after trimming rows

  returns `cleaned_data`
  -


  The `deduplicator` function is designed to remove duplicate data from a list of cleaned data. It accomplishes this task through the following steps:

  1. **Identifying Duplicate Sources:**
    - The function iterates through the cleaned data and identifies lines starting with 'S', which represent source information.
    - These source lines are stored in a separate list `source_list`, and their corresponding indices are stored in `s_index`.
    - The `source_list` is then converted into a set to remove any duplicate source entries.

  2. **Comparing Similar Lines:**
    - For each unique source line in `source_list`, the function checks for similar lines within the cleaned data.
    - If more than one line matches the current source line, it is considered a duplicate.
    - The function prints a message indicating the number of similar lines found for each duplicate source.

  3. **Determining Duplicates with Lesser Rows:**
    - To handle duplicate sources with different data lengths, the function compares the number of rows between duplicates.
    - It creates a list `del_at` to store tuples containing the start and end indices of duplicate data sections that need to be deleted.

  4. **Deleting Duplicates:**
    - The `del_at` list is sorted and reversed to start the deletion process from the bottom of the cleaned data.
    - For each tuple in `del_at`, the function calculates the size (number of rows) of each duplicate data section.
    - It then deletes the duplicate with the lesser number of rows.
    - If multiple duplicates have the same size, the function keeps the first encountered duplicate and deletes the subsequent ones.

  5. **Returning Cleaned Data:**
    - After removing all duplicate data sections, the function returns the updated cleaned data.

  In summary, the `deduplicator` function effectively removes duplicate source data from a list of cleaned data while retaining the longest or first-occurring duplicate in case of equal lengths. This ensures that the cleaned data is free of redundant information.
  '''

  # find duplicates
  #
  pre_len = len(cleaned_data)
  source_list = []
  s_index = []
  duplicates = []
  total_dup = 0

  for index, line in enumerate(cleaned_data):
    if line.startswith('S'):
      source_list.append(line)
      s_index.append(index)
    else:
      continue

  source_list = list(set(source_list))

  for s_line in source_list:
    similar = 0

    for index in s_index:
      if cleaned_data[index] == s_line:
        similar += 1
        end_at = 0

        for range_, xx in enumerate(cleaned_data[index+1:]):
          if xx.startswith('R'):
            continue
          else:
            end_at = range_ + index + 1
            break

        if similar > 1:
          total_dup += 1
          duplicates.append(s_line)
          print(f'found {similar} similar line(s) for {s_line}')
      else:
        continue

  print(f'\nTotal duplicates found: {total_dup}')

  # compare length of duplicates, drop duplicate with lesser rows
  #
  del_at = []

  for dup_in, duplicate in enumerate(duplicates):
    dup_no = 0
    betwn = []
    for index, line in enumerate(cleaned_data):
      if line == duplicate:
        end_at = 0
        dup_no += 1

        for range_, xx in enumerate(cleaned_data[index+1:]):
          if xx.startswith('R'):
            continue
          else:
            end_at = range_ + index + 1
            betwn.append([index,end_at])
            break

        if dup_no == 2:
          del_at.append(tuple(betwn))
        elif dup_no > 2:
          del_at[dup_in] = tuple(betwn)
        else:
          continue

  # drop duplicate with lesser data
  # for equal lengths, maintain first appearing
  # start buttom up
  #
  del_at.sort()
  del_at.reverse()

  for copies_tupl in del_at:
    copy_inx = [x for x, y in enumerate(copies_tupl)]

    size = []
    for index in copy_inx:
      size.append(copies_tupl[index][1]-copies_tupl[index][0])

    counter = 0

    for index, siz in zip(copy_inx, size):
      start, end = tuple(copies_tupl[index])
      if siz < max(size):
        print(f'deleting lesser copy of {cleaned_data[start]} ...')
        del(cleaned_data[start:end])

      elif siz == max(size):
        counter += 1
        if counter > 1:
          print(f'dropping copy {counter} of {cleaned_data[start]} ...')
          del(cleaned_data[start:end])

  print(f'\nPrevious data length: {pre_len}\nFinal data length: {len(cleaned_data)}')
  return cleaned_data

"""### to file function"""

# write cleaned data to file
def to_file(data_to_write, file_name, file_path):
  '''
  function for writing cleaned data to file
  -
  creates a new file in the same directory as the original file
  does not save multiple clean copies of the same file, user must manually rename previous copies

    - `data_to_write` - data produced after all cleaning process has been completed
    - `file_name`     - original file name
    - `file_path`     - original file path

  How it works:
  -
  1. **File Location Determination**:

    - It first determines the location of the original file by extracting the directory path from the provided file path.
    - It does this by splitting the file path based on the '/' or '\' characters and then joining the resulting list up to the second-to-last element.

  2. **New File Name Generation**:

    - The function creates a new file name by appending "_clean.txt" to the original file name.

  3. **Writing to File**:

    - It opens a new file in write mode using the generated file name and the determined file location.
    - It iterates through the provided `data_to_write` list and writes each line to the new file, followed by a newline character.
    - After writing all the lines, it closes the file.

  4. **Printing Confirmation Message**:

    - Finally, it prints a message indicating that the file has been saved successfully, including the new file name and location.

  5. **Important Notes**:

    - The function does not save multiple clean copies of the same file. If the user wants to keep previous clean copies, they need to manually rename them.
    - The function assumes that the user has write permissions in the directory where the original file is located.
  '''

  file_loc = ''

  if '/' in file_path:
    file_loc = '/'.join(file_path.split('/')[:-1])+'/'
  elif '\\' in file_path:
    file_loc = '\\'.join(re.split(r'[\\]', file_path)[:-1])+'\\'

  new_file_name = file_name + '_clean'

  with open(file_loc + new_file_name, 'w') as f:
    for line in data_to_write:
      f.write(line + '\n')
    f.close()
  print(f'\nfile saved as "{new_file_name}" at {file_loc}')
