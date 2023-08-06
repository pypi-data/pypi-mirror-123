import typer
import glob, json, re
from pathlib import Path
from datetime import datetime
import os
from typing import Optional

# explicitly initiating typer 
app = typer.Typer()

__version__ = "1.0"


def version_callback(value: bool):
    if value:
        typer.echo(f"{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(None,"--version", "-v", callback=version_callback),
):
    typer.echo(f"{version}")

# helper functoins
# Natural Sorting algorithm
def natural_key(string_: str):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def getUsersByType(processed_data: list, user_type: str):
    # sample for processed_date = [ { "userId": { "days": [day_id_1, day_id_2, day_id_3], "meals": [meal_id_1, meal_id_2, meal_id_3], "meal_count": 29, "type": "superactive" } }, { "userId": { "days": [day_id_1, day_id_2, day_id_3], "meals": [meal_id_1, meal_id_2, meal_id_3], "meal_count": 8, "type": "active" } }, ]
    unsorted = [ next(iter(i)) for i in processed_data if next(iter(i.values()))["type"] == user_type]
    return sorted(unsorted, key=natural_key)
    
  
def prepare_data(dateKey: str, mealKey: str, start_date: str, end_date: str):
    '''
    This is the place where major operations are being done\n
    dateKey: to get the Day ids\n
    mealKey: to get the Meal ids\n
    '''
    data = []
    # here glob is being used to get paths for all the json files in the data directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = glob.glob(dir_path+'\data\*.json', recursive=True)
    # print(os.path.exists("data"))
    # print(f"files: {files}")
    for single_file in files:
        outer_temp_dict = {} #outer dictionary to create list of users. user id will be the key for this dictionary/object
        inner_temp_dict = {} #inner dictionary which will contain user information as Day IDs, Meal Ids, Meal Counts and user type based on the meal count
        userId = Path(single_file).stem # it return the filename without extension from the filepath
        
        # utf-8 encoding is necessary to parse non-english data
        with open(single_file, 'r', encoding='utf-8') as file:
            # Using 'try-except' to skip files with missing or corrupted data
            try:
                json_file = json.load(file)
                date_filtered_data = get_data_from_date_range(json_file["calendar"][dateKey],start_date, end_date)
                # print("date_filtered_data", date_filtered_data)
                inner_temp_dict["days"] = date_filtered_data
                filtered_meals = {key:val for key, val in json_file["calendar"][mealKey].items() if val in date_filtered_data}
                inner_temp_dict["meals"] = filtered_meals
                meal_count = len(filtered_meals)
                inner_temp_dict["meal_count"] = meal_count
                
                if (meal_count > 10):
                    inner_temp_dict["type"] = "superactive"
                elif (meal_count >= 5):
                    inner_temp_dict["type"] = "active"
                else:
                    temp_type = "None"

                    data_to_check_bored_users = get_data_from_date_range(json_file["calendar"][dateKey],None, end_date, True)
                    if(len(data_to_check_bored_users) > 0):
                        bored_meal_count = len({key:val for key, val in json_file["calendar"][mealKey].items() if val in date_filtered_data})
                        if(bored_meal_count >= 5):
                            temp_type = "bored"    
                    
                    inner_temp_dict["type"] = temp_type
                
                outer_temp_dict[userId] = inner_temp_dict
                # outer_temp_dict["meal_count"] = len(date_filtered_data)
                data.append(outer_temp_dict)
            
            except KeyError:
                print(f'Skipping {single_file}')
    return data

def convert_to_date_type(date: str):
    '''
    date string to _date type
    '''
    return datetime.strptime(date, '%Y-%m-%d').date()

def get_data_from_date_range(data: dict, start_date: str, end_date: str, bored: bool = False):
    '''
    This method takes dateToDayId, start date and end date as params\n
    Returns a list of Day Ids within the date range\n
    By default bored has been kept false\n
    '''
    end_date = convert_to_date_type(end_date)
    if(not bored):
        start_date = convert_to_date_type(start_date)
        return [ val for key, val in data.items() if start_date <= convert_to_date_type(key) and end_date >= convert_to_date_type(key) ]
    else:
        return [ val for key, val in data.items() if end_date >= convert_to_date_type(key) ]
# helper functoins

@app.command()
#help attribute of the function parameter will be dislayed in the "python main.py run --help" command
def run(
    user_type: str = typer.Argument("active", help="active or superactive or bored"),
    start_date: str = typer.Argument("2016-09-01", help="Prefered format: YYYY-MM-DD"), 
    end_date: str = typer.Argument("2016-09-08", help="Prefered format: YYYY-MM-DD")
    ):
    #run function code starts from here
    # since the date comes as string in the json, we need to convert to _date type to compare between two dates
    if(convert_to_date_type(start_date) < convert_to_date_type(end_date)):
        arr_data = prepare_data("dateToDayId", "mealIdToDayId", start_date, end_date)
        list_of_users = getUsersByType(arr_data, user_type)
        typer.echo(f"{list_of_users}")
    else:
        error_flag = typer.style(" Error: ", fg=typer.colors.WHITE, bg=typer.colors.RED)
        typer.echo(f"\n{error_flag} Start date can not be greater than End Date")
        raise typer.Exit()


@app.command()
def author():
    print("G A N Mahmud")


if __name__ == "__main__":
    app()
    # typer.run(main)