import pandas as pd

from fuzzywuzzy import process


pub_data = pd.read_csv('publications_min.csv', header=0,index_col=0,usecols=range(1,9), delimiter=',')

inst_data = pub_data[['affiliations']] # institutions data - for not finished steps

pub_data['authors2'] = pub_data.authors.str.strip("[]").str.replace("'","").str.split(", ")

pub_data = pub_data.explode('authors2')

authors_list = list(pub_data['authors2'].unique())

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

authors_list = [x for x in authors_list if not isfloat(x)] # remove float values from dataset

def get_minlist(my_list,k):
    # for specific string the function returns only string longer than k
    return [item for item in my_list if len(item) > k]


def get_name(namelist,selected_name):
    results = get_minlist(namelist, len(selected_name[0]))
    if len(results) > 0:

        Ratios = process.extract(selected_name[0], results)
        Ratios_final = filter(lambda x: x[1] > 80, Ratios)
        answer = list(Ratios_final)

        if len(answer) == 0:
            answer = selected_name[0]
        else:
            answer = answer[0][0]
    else:
        answer = []
    return answer

results = []
for i in authors_list[0:10]:
    # within the time I spent on this task I decided to do the loop only on "sample" of data.
    # The whole dataset using the code below would take a lot of time
    sel_name = [i]
    results.append(get_name(authors_list, sel_name))

results_df = pd.DataFrame("author":results)
new = results_df["author"].str.split(" ", n = 10, expand = True)

output = {"first_name": new[0], "last_name": new.iloc[:, 1:].ffill(axis=1).iloc[:, -1]}
output = pd.DataFrame(output)

output.to_csv("unique_people.csv", sep=',',index=False)
