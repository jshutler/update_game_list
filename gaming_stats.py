import gspread
import pandas as pd 
gc = gspread.service_account()

# Open a sheet from a spreadsheet in one go
# wks = gc.open("https://docs.google.com/spreadsheets/d/1PbX_6B8vIwehJr7XH_I0WzdhFrv6XH4o57VePYtvmfM/edit#gid=1798374768").sheet1
sheet = gc.open_by_key("1PbX_6B8vIwehJr7XH_I0WzdhFrv6XH4o57VePYtvmfM")
list_wks = sheet.worksheet("games_list")
basic_stats_wks = sheet.worksheet('basic_stats')
counts_by_console_wks = sheet.worksheet('counts_by_console')
counts_by_completion_wks = sheet.worksheet('counts_by_completion')
counts_by_console_and_completion_wks = sheet.worksheet('counts_by_console_and_completion')

raw_df = pd.DataFrame(list_wks.get_all_records())



basic_stats = raw_df.describe().reset_index().astype(str)#[['index', 'Console', 'Completion']]


raw_df['Completion_and_finished'] = raw_df['Completion'].apply(lambda x: x.replace('completed', 'finished'))

counts_by_console = raw_df.groupby('Console')['Completion_and_finished'].count().reset_index().rename(columns={"Completion_and_finished": 'count'})

counts_by_completion = raw_df.groupby('Completion')['Console'].count().reset_index().rename(columns={"Console": 'count'})

counts_by_console_and_completion = raw_df.groupby(['Console', 'Completion']).count().reset_index()

counts_by_console_wks.clear()
basic_stats_wks.clear()
counts_by_completion_wks.clear()
counts_by_console_and_completion_wks.clear()

counts_by_console_wks.update([counts_by_console.columns.values.tolist()] + counts_by_console.values.tolist())
basic_stats_wks.update([basic_stats.columns.values.tolist()] + basic_stats.values.tolist())
counts_by_completion_wks.update([counts_by_completion.columns.values.tolist()] + counts_by_completion.values.tolist())
counts_by_console_and_completion_wks.update([counts_by_console_and_completion.columns.values.tolist()] + counts_by_console_and_completion.values.tolist())
