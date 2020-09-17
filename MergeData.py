import pandas as pd
import glob


class MergeData:
    def iterate(self):
        # Read the files into two dataframes.
        my_list=list()
        for fname in glob.glob('data/*.csv'):
            print(fname)
            df = pd.read_csv(fname)
            my_list.append(df)
            
        # # Merge the two dataframes, using _ID column as key
        df3 = pd.concat(my_list)
        df3 = df3.drop(df3.columns[[0]], axis=1)
        df3 = df3.drop_duplicates(subset=['id'])
        print(df3)

        # # Write it to a new CSV file
        df3.to_csv('SpotifyDataTotal.csv')
Object = MergeData()
Object.iterate()
