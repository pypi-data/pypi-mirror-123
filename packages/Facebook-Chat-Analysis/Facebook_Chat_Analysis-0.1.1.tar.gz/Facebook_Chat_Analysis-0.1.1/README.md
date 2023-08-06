# Facebook_Analysis
Extract and Analyse Facebook data - I will add Instructions and useage examples later (below is the easiest/recommend use)

### MOST BACIS USAGE 

        all_pre_processing(Zipp_path,save_unzipped, delete=True, save=True)

This function works as follows:

        '''Takes Zipped Facebook data, extracts, pre-processes and saved an All_Chat_History csv and individual chat Text Files.

            Inputs:

                Zipp_path = Directory where Zipped Folder is saved

                save_path = Directory where you wish to save all Facebook Information

                delete = Will remove Zipped FB data is no longer desired & Individual JSON files - Set to "True" if you wish to delete everything (Recommend setting to False initially for testing)

                save = Will save the dataFrame to csv - Set to "True" if you wish to save

            Outputs:

                All_Chat_History.csv: DataFrame of all previous messages sent and received - along with key metrics for each

                Text_Files folder: Folder with a .txt file for each conversation - containing: 'Time_stamp', 'ConvoTitle', 'sender', 'message'   

            Useage:

                all_pre_processing(Zipp_path,save_path, delete=True, save=True)'''

