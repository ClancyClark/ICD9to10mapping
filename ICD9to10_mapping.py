import numpy as np
import pandas as pd
import os
import re
import csv
import datetime


# ICD9 and ICD10 GEMS .txt files
i9_cm_source_path = r'gem_files\2018\2018_I9_cm_gem.txt'
i10_cm_source_path = r'gem_files\2018\2018_I10_cm_gem.txt'
i9_pcs_source_path = r'gem_files\2018\2018_I9_pcs_gem.txt'
i10_pcs_source_path = r'gem_files\2018\2018_I10_pcs_gem.txt'


class ICD_CM_Conversion:

    def __init__(self, i9_cm_path = i9_cm_source_path, i10_cm_path = i10_cm_source_path):
        # cm
        self.i9_cm_path = i9_cm_path
        self.i10_cm_path = i10_cm_path
        self.df9_cm= self.get_data(self.i9_cm_path, ['I9', 'I10', 'FLAG'])
        self.df10_cm = self.get_data(self.i10_cm_path, ['I10', 'I9', 'FLAG'])

    def get_data(self, path, cols):
        """
        Creates dataframe using ICD GEM text file.
        :param path: path to ICD GEM text file
        :param cols: column names as list
        :return: dataframe
        """
        reg = re.compile(r'(\w*) +(\w*) +(\w*)')
        with open(path) as file:
            reader = csv.reader(file)
            cm_df = pd.DataFrame([list(reg.search(str(i)).groups()) for i in reader], columns=cols)
            return cm_df

    def dict_append(self, base, new):
        """
        Returns base dictionary containing data structure as item, with appended items of new dictionary to base dictionary
        :param base:
        :param new:
        :return: dtype(dict)
        """
        for i in new:
            if i not in base.keys():
                base[i] = new[i]
                continue
            else:
                base[i].extend(new[i])
                base[i] = list(set(base[i]))
        return base

    def icd9_to_10_cm(self, los):
        """
        Forward match from I9 GEMS to I10 GEMS
        :param los: list of codes
        :return: dtype(dict)
        """
        a = dict()

        for i in los:
            a[i] = list(self.df9_cm[self.df9_cm['I9']==i][['I10', 'FLAG']].values)
        return a

    def icd10_to_9_cm(self, list_of_codes):
        """
        Backward match from I10 GEMs to I9 GEMS
        :param list_of_codes: list of codes
        :return: dtype(dict)
        """
        a = dict()

        for i in list_of_codes:
            a[i] = list(self.df10_cm[self.df10_cm['I10']==i][['I9', 'FLAG']].values)
        return a

    def fwb_cm(self, list_of_codes):
        """
        Combined result of forward and backward matching
        :param list_of_codes: list of codes
        :return: dtype(dict)
        """
        f = self.icd9_to_10_cm(list_of_codes)
        b = self.icd10_to_9_cm(list_of_codes)
        return self.dict_append(f, b)

    def sm_cm(self, list_of_codes):
        """
        Secondary matching, where secondary ICD9 codes are identified, and provided a forward backward match as well.
        Seconary ICD9 codes are identified as other ICD9 codes that share ICD-10 codes, either through forward or
        backward matching.
        :param list_of_codes: list of codes
        :return: dtype(dict)
        """
        fwb_1 = self.fwb_cm(list_of_codes)
        secondary = list()
        # forward match of secondary
        secondary.extend(list(set(self.df9_cm[self.df9_cm['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))
        # backward match of secondary
        secondary.extend(list(set(self.df10_cm[self.df10_cm['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))
        print('Secondary ICD-9-cm_source codes: {}'.format(secondary))

        return self.dict_append(fwb_1, self.fwb_cm(secondary))


class ICD_PCS_Conversion:
    def __init__(self, i9_pcs_path = i9_pcs_source_path, i10_pcs_path = i10_pcs_source_path):

        # pcs
        self.i9_pcs_path = i9_pcs_path
        self.i10_pcs_path = i10_pcs_path
        self.df9_pcs = self.get_data(self.i9_pcs_path, ['I9', 'I10', 'FLAG'])
        self.df10_pcs = self.get_data(self.i10_pcs_path, ['I10', 'I9', 'FLAG'])

    def get_data(self, path, cols):
        """
        Creates dataframe using ICD GEM text file.
        :param path: path to ICD GEM text file
        :param cols: column names as list
        :return: dataframe
        """
        reg = re.compile(r'(\w*) +(\w*) +(\w*)')
        with open(path) as file:
            reader = csv.reader(file)
            pcs_df = pd.DataFrame([list(reg.search(str(i)).groups()) for i in reader], columns=cols)
            return pcs_df

    def dict_append(self, base, new):
        """
        Returns base dictionary containing data structure as item, with appended items of new dictionary to base dictionary
        :param base:
        :param new:
        :return: dtype(dict)
        """
        for i in new:
            if i not in base.keys():
                base[i] = new[i]
                continue
            else:
                base[i].extend(new[i])
                base[i] = list(set(base[i]))
        return base

    def icd9_to_10_pcs(self, los):
        """
        Forward match from I9 GEMS to I10 GEMS
        :param los: list of codes
        :return: dtype(dict)
        """
        a = dict()

        for i in los:
            a[i] = list(self.df9_pcs[self.df9_pcs['I9']==i][['I10', 'FLAG']].values)
        return a

    def icd10_to_9_pcs(self, list_of_codes):
        """
        Backward match from I10 GEMs to I9 GEMS
        :param list_of_codes: list of codes
        :return: dtype(dict)
        """
        a = dict()

        for i in list_of_codes:
            a[i] = list(self.df10_pcs[self.df10_pcs,['I10']==i][['I9', 'FLAG']].values)
        return a

    def fwb_pcs(self, list_of_codes):
        """
        Combined result of forward and backward matching
        :param list_of_codes: list of codes
        :return: dtype(dict)
        """
        f = self.icd9_to_10_pcs(list_of_codes)
        b = self.icd10_to_9_pcs(list_of_codes)
        return self.dict_append(f, b)

    def sm_pcs(self, list_of_codes):
        """
        Secondary matching, where secondary ICD9 codes are identified, and provided a forward backward match as well.
        Seconary ICD9 codes are identified as other ICD9 codes that share ICD-10 codes, either through forward or
        backward matching.
        :param list_of_codes: source code file
        :return: dtype(dict)
        """
        fwb_1 = self.fwb_pcs(list_of_codes)
        secondary = list()
        # forward match of secondary
        secondary.extend(list(set(self.df9_pcs[self.df9_pcs['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))
        # backward match of secondary
        secondary.extend(list(set(self.df10_pcs[self.df10_pcs['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))
        print('Secondary ICD-9-CM Codes: {}'.format(secondary))

        return self.dict_append(fwb_1, self.fwb_pcs(secondary))


def read_files(rootdir, gem_type):
    for subdir, dirs, files in os.walk(rootdir):
        print(f'Number of Files: {len(files)}')
        dfs = []
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file
            filename = file
            current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
            df = process_file(filepath, gem_type)
            # save data to file
            df.to_csv(f'{current_time}_{filename}.csv', index=False)


def process_file(data_file, gem_type):
    print(data_file)
    code_file = open(data_file, 'r')

    list_of_codes = []
    for line in code_file:
        stripped_line = line.strip()
        list_of_codes.append(stripped_line)

    # remove duplicates
    list_of_codes = list(set(list_of_codes))

    code_file.close()

    icd_cm_converter = ICD_CM_Conversion()
    icd_pcs_converter = ICD_PCS_Conversion()

    if gem_type == 'cm':
        converted_data = icd_cm_converter.icd9_to_10_cm(list_of_codes)
    elif gem_type == 'pcs':
        converted_data = icd_pcs_converter.icd9_to_10_pcs(list_of_codes)
    else:
        expanded = pd.DataFrame()
        return expanded

    df = pd.DataFrame.from_dict(converted_data.items())
    df.rename(columns={0: 'ICD9', 1: 'ICD10-code_and_flag'}, inplace=True)
    expanded_df = df.explode('ICD10-code_and_flag')
    expanded_with_codes_df = expanded_df.dropna()
    expanded_with_codes_df['ICD10'], expanded_with_codes_df['FLAG'] = zip(*expanded_with_codes_df.pop('ICD10-code_and_flag'))

    nan_codes_df = expanded_df[expanded_df['ICD10-code_and_flag'].isnull()]
    nan_codes_df['ICD10'] = np.nan
    nan_codes_df['FLAG'] = np.nan
    nan_codes_df.drop(columns=['ICD10-code_and_flag'], inplace=True)

    complete_df = expanded_with_codes_df.append(nan_codes_df)

    return complete_df


def main():
    print('Start mapping...')
    read_files(r'ICD-9-cm_source', gem_type='cm')
    read_files(r'ICD-9-pcs_source', gem_type='pcs')


if __name__ == '__main__':
    main()
