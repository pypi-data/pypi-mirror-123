import csv

# instead of using csv lets just directly use a pandas df to avoid the file path hastle


def LogNew(filepath):  # should be called at the start of every trading algorithm
    """
    ------------------------------------------------
    This function writes the column headers to the
    provided csv filepath. If the .scv file doesnt
    exist, a new one will be created.
    ------------------------------------------------
    Parameters:
        - filepath (str): full filepath of where
                          you want the log file
                          to be saved.
    ------------------------------------------------
    Returns:
        - None
    """
    if filepath == None or len(filepath) == 0:
        raise Exception("Can not leave filepath empty")
    else:
        # open the file to write, if it doesnt exist, new one is created
        csv_file = open(filepath, 'w', newline="")
        col_head = ('Buy(Date)', 'Buy(Price)', 'Sell(Date)',
                    'Sell(Price)', 'Diff. Bal.')  # add the folling col headings
        writer = csv.writer(csv_file)  # establish a writer for the csv file
        writer.writerow(col_head)  # write the col headings to the rows
        csv_file.close()  # close the file
    return


def LogSell(filepath, log_data):  # should be called when any sell order is placed
    """
    ------------------------------------------------
    This function appends selling data to the
    provided csv file.
    ------------------------------------------------
    Parameters:
        - filepath (str): full filepath of where
                          you want the log file
                          to be saved.
        - log_data (lis): require the following data:
        ['Buy(Date)', 'Buy(Price)', 'Sell(Date)', 'Sell(Price)', 'Diff. Bal.']
    ------------------------------------------------
    Returns:
        - None
    """
    if filepath == None or log_data == None:
        raise Exception("Please provide valid log_data and filepath")
    else:
        if len(log_data) != 5:
            raise Exception(
                "Please ensure log_data ONLY contains the required entries")
        else:
            # open the file for appending
            csv_file = open(filepath, 'a', newline="")
            data = (log_data[0], log_data[1], log_data[2],
                    log_data[3], log_data[4])  # create a tuple with the log data in order
            # establish a writer for the csv file
            writer = csv.writer(csv_file)
            writer.writerow(data)  # write the data to the csv files rows
            csv_file.close()  # clos the file
    return
