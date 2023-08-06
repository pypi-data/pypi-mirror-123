#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 10:14:19 2021

@author: patrick
"""

''' This contains a bunch of functions for pro-cessing the facebook data'''


import os, json
import pandas as pd
import shutil
from pathlib import Path
import emojis
import zipfile


all_pre_processing(Zipp_path,save_unzipped, delete=True, save=True)

''' Takes Zipped Facebook data, extracts, pre-processes and saved an All_Chat_History csv and individual chat Text Files.
    Inputs:
        Zipp_path = Directory where Zipped Folder is saved
        save_path = Directory where you wish to save all Facebook Information
        delete = Will remove Zipped FB data is no longer desired & Individual JSON files - Set to "True" if you wish to delete everything (Recommend setting to False initially for testing)
        save = Will save the dataFrame to csv - Set to "True" if you wish to save
    Outputs:
        All_Chat_History.csv: DataFrame of all previous messages sent and received - along with key metrics for each
        Text_Files folder: Folder with a .txt file for each conversation - containing: 'Time_stamp', 'ConvoTitle', 'sender', 'message'   
    Useage:
        all_pre_processing(Zipp_path,save_path, delete=True, save=True)
'''
def all_pre_processing(Zipp_path,save_path, delete, save):
    #Extract Zipp
    print('Unzipping and Saving')
    extract_and_save_zipped_fb_data(Zipp_path,save_path, delete=True)
    print("Everything Unzipped OK")
    
    #Create Jsons
    print("Creating Jsons")
    extract_jsons(save_path, save_path+'/Only_Jsons/', delete=True)
    print("Created Jsons")
    
    #Create CSV
    print("Creating CSV")
    messages=create_single_data_frame(save_path+'/', save=True)
    print("Created CSV")
    
    
    #Create Individual Readble Files
    print("Creating Individual Files")
    create_individual_test_files(save_path)
    print("Created Individual Files")
    
    print("All Done!!!!!")


''' Takes Zipped Facebook data and extracts it to destination folder.
    Inputs:
        Zipp_path = Directory where Zipped Folder is saved
        save_path = Directory where you wish to save all Facebook Information
        delete = Will remove ZIpped FB data is no longer desired - Set to "True" if you wish to delete everything
    Outputs:
        Extracted Facebook Information
    Useage:
        extract_and_save_zipped_fb_data(Zipp_path,save_unzipped, delete=True)
'''
def extract_and_save_zipped_fb_data(Zipp_path,save_path, delete):
    shutil.rmtree(save_path, ignore_errors=True)  #Removes DIrectory if it already exists
    #Unzip and save to save_path destination
    with zipfile.ZipFile(Zipp_path, 'r') as zip_ref:
        zip_ref.extractall(save_path)
    #If delete is true - Delete the zipped version
    if delete:
        os.remove(Zipp_path)
        print("Deleted Zipp File")
    print('Extracted Information - Saved at: ',save_path)
    
    

''' Extract only the conversation JSON file from folder - Save in new directory with all other conversations
    Inputs:
        target_directory = Directory where Facebook Data is saved
        destination_directory = Directory where you wish to save all conversations
        delete = Will remove all FB data is no longer desired - Set to "True" if you wish to delete everything
    Outputs:
        A set of JSON files contained within the destination_directory
    Useage:
        extract_jsons(target_directory, destination_directory, delete=True)
'''
def extract_jsons(target_directory, destination_directory, delete):
    Path(destination_directory).mkdir(parents=True, exist_ok=True)    #Create folder if not exist
    for root, dirs, files in os.walk(target_directory+'/messages'):   #Get all subdirectories
         for file in files:     #Check each files in directory
             #If Json -> MOVE TO destination_directory:
             if file.endswith('.json'):
                 shutil.move(root+'/'+file, destination_directory+'/'+root.rsplit('/',1)[-1]+file)
    #If delete is true - then remove all old files 
    if delete:
        shutil.rmtree(target_directory+'/messages')
    print("Completed the move.\n Output Found at: ", destination_directory)







''' Converts All Jsons to single data frame and exports to CSV.
    Columns=['Time_stamp', 'sender', 'message', 'reacts', 'ConvoTitle',
       'Num_Participants', 'Participants', 'year', 'lenMsg', 'emojis', 'Emoji_Count']
    Inputs:
        json_path = Directory where all JSON files are saved (See extract_jsons for further info)
        save_path = Directory where you wish to save all conversation information from DataFrame
        save = Will save the dataFrame to csv - Set to "True" if you wish to save
    Outputs:
        A variable containing all the information provided in Columns - for all conversations
        A single csv containing all the information provided in Columns - for all conversations - IF save=True
    Useage:
        messages=create_single_data_frame(json_path, save_path, save=True)
'''
def create_single_data_frame(save_path, save):
    all_messages=load_message_info(save_path)  #Calling load_Message_info function
    print('Loaded the Initial DataFrame') 
    #If we wish to save the Data Frame
    if save:
        print('Saving data to:',save_path+'/All_Chat_History.csv' )
        all_messages.to_csv(save_path+'/All_Chat_History.csv', index=False)
        
    return all_messages




''' Converts All Jsons to single data frame.
    Columns=['Time_stamp','ConvoTitle', 'sender','message', 'reacts', 'Num_Participants', 'Participants', 
                          'year','lenMsg', 'emojis', 'Emoji_Count']
    Inputs:
        json_path = Directory where all JSON files are saved (See extract_jsons for further info)
    Outputs:
        A variable containing all the information provided in Columns - for all conversations
    Useage:
        messages=create_single_data_frame(json_path)
'''
def dataframe_all_convos(json_path):
    message_info=[]
    for root, dirs, files in os.walk(json_path):
        for name in files:
            if name.endswith((".json")):
                try:
                    file=os.path.join(root, name)
                    jsonFile = open(file, 'r') 
                    #jsonFile = open('%s' %f, 'r')
                    values = json.load(jsonFile)
                    jsonFile.close()
                    convo=values["title"]  #Who the conversation is with
                
                    participants=len(values['participants'])
                    participant_list=values['participants']
                    participants_in_convo= [item['name'] for item in participant_list]
                    #participants_in_convo= [item['name'] for item in participant_list    if item['name'] != main_name]
                
                        
                
                    for messages in values['messages']:
                        try:
                            time=messages['timestamp_ms']
                            sender=messages['sender_name']
                            content=messages['content']      
                            try:
                                reactions=len(messages['reactions'])
                                info=[time, sender,content, reactions, convo, participants, participants_in_convo]
                                message_info.append(info)
                    
                            except:
                                info=[time, sender,content, 0 ,convo, participants, participants_in_convo]
                                message_info.append(info)
                        except:
                            pass        
                except:
                    pass
    all_messages=pd.DataFrame(message_info)
    all_messages.columns=['Time_stamp','sender','message','reacts','ConvoTitle','Num_Participants', 'Participants']   
    all_messages['year']=pd.to_datetime(all_messages['Time_stamp'],unit='ms').dt.year
    all_messages['Time_stamp']=pd.to_datetime(all_messages['Time_stamp'],unit='ms')
    all_messages.columns=['Time_stamp','sender','message','reacts','ConvoTitle', 'Num_Participants', 'Participants', 'year']   
    all_messages['lenMsg']=all_messages['message'].str.split().str.len()
    
    
        #Encode and Decode for Emoji Stuff
    all_messages['encoded']= all_messages['message'].str.encode('latin_1') 
    all_messages['decoded']=all_messages['encoded'].str.decode("utf-8")
    
    all_messages['emojis']= [list(emojis.get(sentence)) for sentence in all_messages['decoded']]
    all_messages['Emoji_Count']=all_messages['emojis'].str.len()
    
    
    #DELETING AND RE-ARRANGING COLUMNS
    del all_messages['encoded']
    del all_messages['message']
   
    all_messages.columns=['Time_stamp', 'sender', 'reacts', 'ConvoTitle', 'Num_Participants', 'Participants', 'year', 
                          'lenMsg','message', 'emojis', 'Emoji_Count']
    
    all_messages=all_messages[['Time_stamp','ConvoTitle', 'sender','message', 'reacts', 'Num_Participants', 'Participants', 
                          'year','lenMsg', 'emojis', 'Emoji_Count']]

    all_messages=all_messages.sort_values(by='Time_stamp', ascending=True)
    return all_messages



''' Loads all message content int data frame.
    Seeks to use the main csv first - if that does not exist, it create the data frame using the dataframe_all_convos function.
    Columns=['Time_stamp','ConvoTitle', 'sender','message', 'reacts', 'Num_Participants', 'Participants', 
                          'year','lenMsg', 'emojis', 'Emoji_Count']
    Inputs:
        save_path = Directory where All_Chat_History would is/will be stored, if not there, 
            uses this directory to start search for all JSON that are saved (See extract_jsons for further info)
    Outputs:
        A variable containing all the information provided in Columns - for all conversations
    Useage:
        all_messages=load_message_info(save_path)
'''
def load_message_info(save_path):
    #Try to use the csv
    try:
        return pd.read_csv(save_path+'/All_Chat_History.csv')
    except:
    #Else do the big import
        return dataframe_all_convos(save_path)    



''' Splits all conversations into Readable Text Files.
    Inputs:
        message_path = Directory where all message data is stored
    Outputs:
        "Text_Files" Folder containing individual text files for each conversation.
        Columns= 'Time_stamp', 'ConvoTitle', 'sender', 'message'   
    Useage:
        create_individual_test_files(message_path)
'''
def create_individual_test_files(message_path):
    #Create directory to save individual CSVs
    text_file_path=message_path+'/Text_Files/'
    Path(text_file_path).mkdir(parents=True, exist_ok=True)    #Create folder if not exist
    
    #Load messages
    all_messages=load_message_info(message_path)
        
    #Split into individual conversations + Save in text file
    all_messages['ConvoTitle'].unique()
    for convo in all_messages['ConvoTitle'].unique():
        try:
            specific_convo=all_messages[all_messages['ConvoTitle']==convo]
            specific_convo[['Time_stamp', 'ConvoTitle', 'sender', 'message']].to_csv(text_file_path+convo+'.txt', sep='\t', index=False)
        except:
            pass
    print("Finished saving, files can be found at:",text_file_path )


    



