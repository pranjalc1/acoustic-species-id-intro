import pandas as pd


def stratified_random_sample(csv_path):
    """Creates a stratified random sample of a csv file

    Args:
        csv_path (str): path to csv file with complete data

    Returns:
        bool: whether the sampling is successful or not
    """
    # reads csv file
    data = pd.read_csv(csv_path, low_memory=False)

    # filter out data that is less than one minute, has an na StartDateTime, and/or is from a failed AudioMoth
    data = data[data["Duration"] > 60]
    data = data.dropna(axis='rows', subset=["StartDateTime"])

    audiomothsDropped = ["AM-21", "AM-19", "AM-8", "AM-28"]
    data = data[~data["AudioMothCode"].isin(audiomothsDropped)]

    # create data frame
    stratified_random_sample = pd.DataFrame(columns=data.columns)

    # iterate through all audiomoths
    for audiomoth in data.AudioMothCode.unique():

        # variable to check if it has all hours
        hasAllHours = True

        # create filtered data
        specific_data = data[data.AudioMothCode == audiomoth]

        # create data that will hold sample
        audiomoth_sample = pd.DataFrame(columns=data.columns)

        # iterate through all hours
        for hour in range(24):

            # create string to search for in StartDateTime column
            if (hour < 10):
                time_string = " 0" + str(hour)
            else:
                time_string = " " + str(hour)

            # filter hour-specific data
            hourly_data = specific_data[specific_data["StartDateTime"].str.contains(
                time_string)]

            # only continue if there exists a data entry for this hour
            if len(hourly_data) == 0:
                hasAllHours = False
                break
            audiomoth_sample = pd.concat(
                [audiomoth_sample, hourly_data.sample(1)])

        # only add audiomoth_sample if has sample from each hour
        if not hasAllHours:
            hasAllHours = True
            continue
        stratified_random_sample = pd.concat(
            [stratified_random_sample, audiomoth_sample])

    # convert DataFrame to csv file
    stratified_random_sample.to_csv(
        csv_path[:-4] + "_stratified_random_sample.csv", index=False)

    # check to see if right number of elements is in the csv file
    # print(len(stratified_random_sample), len(stratified_random_sample.AudioMothCode.unique()))

    # returns True if completed
    return True


print(stratified_random_sample("Peru_2019_AudioMoth_Data_Full.csv"))
