import pandas as pd
import json
import os 
import numpy as np
from typing import Union

def get_participant_answers(folder: os.PathLike,id: int =0) -> Union[list[any], list[str]]:
    """This function reads the json file contained in the folder for each participant and
    parses the keys related to questions

    Args:
        folder (os.PathLike): folder path containing named PATXXX
        id (int, optional): ID of the participant for dataframe initialization purposes

    Returns:
        Union[list[any], list[str]]: returns 2 lists with the first containing the
            question answers and the second containing the question and shown in game.
    """
    data_dict = {}
    with open(os.path.join(folder,"data.json")) as f:
        data_dict = json.load(f)
    
    question_keys = [x for x in data_dict.keys() if "questions" in x]
    answers = [id]
    questions = ["PAT_ID"]
    for q_key in question_keys:
        question_dict = data_dict[q_key]
        
        #skip first key
        dict_keys_iter = iter(question_dict.keys())
        __level = next(dict_keys_iter)
        for sub_key in dict_keys_iter:
            answers.append(question_dict[sub_key][0])
            questions.append(sub_key)

    return answers, questions

def main():
    
    all_answers = []
    questions = []
    
    # read answers from the list of folders below
    # TODO: find the file contained in the directory. 
    #       Currently not sure how to determine which sub folder
    folders = ["data/PAT001/15_06_19",
               "data/PAT002/09_43_17",
               "data/PAT003/15_40_38",
               "data/PAT004/08_58_25"]
    for id, f in enumerate(folders):
        answers, questions= get_participant_answers(f,id+1)
        all_answers.append(answers)
        
    # convert to numpy for better dimension shaping
    all_answers = np.array(all_answers)
    questions = np.array(questions)
    
    # create dataframe and export to csv
    df = pd.DataFrame(data=all_answers, columns=questions)
    df.set_index("PAT_ID")
    df.to_csv("question_answers.csv",index=False)

if __name__ == "__main__":
    main()