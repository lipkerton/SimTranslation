# What is the project for #
Translation of individual tags in .xprt files while maintaining the structure and functionality of the original .xprt file. Creating a copy of the original file in Chinese/English and creating a list of all translations made while the program is running.

# Technologies #
Python

# How to start translation #
To start, follow these steps:
+ upload files that need translation to the trans_input_files folder
+ translated copies will be stored in trans_result_files
+ the binary dictionary maintranslation.trans (which contains the original SimInTech translations) should be located in the dictionaries folder
+ when all the necessary things are in place (files for translation in the trans_input_files and maintranslation.trans folder), you can run the .exe file in one of the launcher folders - the translation of all projects will be completed and the result can be found in the trans_result_files folder.
+ the list of completed translations can be viewed in the trans_csv_chn and trans_csv_eng folders

# Additional #
+ The binary dictionary (maintranslation.trans), which underlies the translation procedure, can be updated (if new translations were added through the SimInTech program). To do this, put a new dictionary (maintranslation.trans) in the dictionaries folder, replacing the existing file there. Then the program can be launched as usual.
+ After the files you need are translated, the entire list of new translations (which are not in the original SimInTech dictionary) will be displayed in csv files (they are located in the trans_csv_eng/trans_csv_chn folders in support directory); if you want to change any word in the translation, you do not need to look for a file with this word - you just need to go to the dictionaries folder and write the new translation to the file temp_english_dictionary.csv in the format: Russian word;English translation (for Russian-English translations) or to a file temp_chinese_dictionary.csv in the format: English word;Chinese translation (for English-Chinese translations). Even if you made a mistake with the value, simply enter a new value into the desired file and the old value will be replaced.