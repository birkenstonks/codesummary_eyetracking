# Code Summarization
#### Code and Documentation written by Zach Karas. Email with any questions (z.karas@vanderbilt.edu)
### This repo contains the code for running, analyzing, and visualizing the code summarization project
The task has participants read snippets of Java code while their gaze is recorded using a Tobii eye-tracker. For half of the task, participants read pre-written summaries (human-written or AI-written), and for the other half, participants write their own summaries. It is randomized whether participants read or write summaries first. Java code comes from the FunCom dataset [2], and the AI summaries are generated by a Deep Learning Model [1]. 

## Running the Task
The main file for running the task is server2.py. It does not rely on any esoteric packages, other than perhaps tobii_research, so the setup should *hopefully* be straightforward. The task is randomized using each participant's ID number as a random seed, which ensures the order will be the same for each ID number. The task is designed so the participant gets a break in the middle of each section and in the middle of the whole task (between reading and writing). This was designed to give the participant breaks, and give the researchers the opportunity to recalibrate the eye-tracker every 15-20 minutes. 
The task is also designed so if the internet cuts out or if the task crashes, running server2.py with the same ID number will resume at the last save point. 
Below is a list of all the data types recorded during the task:

## Data - For access, please email Zach with your name and title (z.karas@vanderbilt.edu).
* Keystrokes: All keystrokes made by participants, including timepoints and the function name. Saved as <idnum>_keystrokes.csv
</br> (e.g. 008,showLatestPlan,18418213,S,2023-02-21 16:57:42.880827)
</br>
* Task: All ratings on summary reading section and all summaries on writing section. Saved as <idnum>_task.csv
</br> (e.g. ID#,	createServerChooser, 35553791,	reading,		 ,creates the server chooser, callcon,	neutral,	s_agree,	s_disagree,	agree,	36:35.9) where columns are participant_id, function_name, function_id, task, participant_summary, given_summary, summary_author, how_accurate, missing_info, unnecessary_info, end_time. For the writing condition, the ratings columns will be empty and the participant's summary will be recorded.
</br>
* Reading Save: The participant's progress on the reading task (e.g. how many stimuli they've seen)
</br>
* Writing Save: The participant's progress on the writing task (same as reading)
</br>
* Gaze folder: contains all the gaze files if eye-tracking is being recorded, split by file name. The column headers here are ['participant_id', 'function_name', 'function_id', 'system_timestamp', 'device_timestamp', 'valid_gaze_left', 'valid_gaze_right', 'gaze_left_eye', 'gaze_right_eye', 'valid_pd_left', 'valid_pd_right', 'gaze_left', 'gaze_right', 'irl_left_coord, irl_right_coord, irl_left_point_on_screen, irl_right_point_on_screen]
The irl points are the participants locations in physical space (used for creating fixation filter)

## Actual task design
The code responsible for the task is in the static/css folder and the templates folder. The templates folder contains html files corresponding to the task (reading template, writing template, rest slide template, etc.)

## Stimuli
This folder contains the "database." Just spreadsheets that store the Java functions, their id numbers, and summaries (human and AI written). 
* stimulus_selection.ipynb - takes the pruned_seeds2.csv and generates writing stimuli and reading stimuli, which don't share any functions. The task is designed so 60% of the functions seen by each participant are the same, with the other 40% being from a larger, random pool of stimuli. Here it's designed so there are 40 reading stimuli and 25 writing stimuli. This file also does a sort of bit flip for whether participants see the human-written or AI-written summaries.

## Bounding Boxes
This directory contains the code for creating the bounding boxes, intermediate data, and final bounding box files. The important folders are final_stimuli (images of each Java function) and word_coordinates_final (polished bounding boxes for each function). Below is a short description of each file:
* 1_draw_boxes.ipynb - this file takes the raw images from the final_stimuli folder and calculates the coordinates for the bounding boxes for each word, and symbol unfortunately. It saves a png for each word in a folder with the function name, and a word_coordinates file with each word's coordinates. Uses OCR to predict what word is in each word image. 
* 2_match_code.py - The above process isn't perfect, so I use spell check to get closer to the real words
* 3_bounding_boxes_preprocessing.ipynb - This file cleans all the csv files and removes trailing characters like ";" and boxes for paretheses only. Stores these polished files in word_coordinates_final
* 3.5_split_bounding_boxes.ipynb - Using OCR split the methods by spaces, but this did not split method calls (e.g. clock.getCurrentTime). This split was accomplished manually to differentiate the object from the method call.
* 4_localize_gaze.ipynb - Reads in the eye-tracking files and annotates each gaze point with the bounding box for the code the participant was looking at. Averages a participants left and right gaze coordinates.
#### Folders
* final_stimuli - contains screenshots of all 162 Java methods used in the study
* old_stimuli - contains a record of methods that were excluded.
* word_coordinates - contains the coordinates for every token in the Java methods. This folder contains an intermeidate representation, where some of the tokens have not been matched.
* word_coordinates_final - contains the coordinates for all the tokens in raw pixel coordinates, as well as pixel coordinates normalized to be between 0 and 1. (Tobii records eye-tracking coordinates using 0-1 values)
* word_coordinates_split - coordinates for tokens where object names and method calls are split
* word_coordinates_split_6_4 - intermediate representation.

## Analysis
This folder contains analysis code for both the Java methods, as well as the eye-tracking data. Java methods were parsed using srcML [3] to get the structural context of each token (e.g. variable declaration, conditional block, method name, etc.) based on the Abstract Syntax Tree (AST). These AST annotations were assigned to each token as a list, then combined with the bounding box coordinates to obtain unified spreadsheets of physical coordinates for the tokens as they were presented, and semantic information about the tokens. I then "abstracted" each token by giving it a generalized label based on its purpose in the methods ('Hello World' --> String Literal).

I then analyzed the eye-tracking metrics associated with these tokens. More specifically, I calculated the fixation counts and fixation durations on each token, then computed the scan paths  
* noise.py - crude metric for calculating noise. Basically looks at the ratio of NaN rows  when the eye-tracker couldn't record someone's eyes, and valid coordinates.




## Visualization
This folder takes either a screen recording or screenshot of a function, and plots a participant's gaze coordinates. Helpful for a sanity check. The actual output I generated is stored away because it bloated the repo. This code is from another repo (https://github.com/XiangGuo1992/ORCL_VR_EyeTracking.git), so I don't know exactly how it works. It also uses a lot of labmda functions.

The general workflow is:
* 1_video_to_img.py - the file splits a screen recording into png images.  
* 2_plot_eyetracking.py - Takes the video frames and plots eye-tracking coordinates onto each image from eye-tracking files
* 3_img_to_video.py - converts images back into a video
* plot_eyetracking_scrap.ipynb - scrap file where I tried out different code

## References
[1] Aakash Bansal, Zachary Eberhart, Zachary Karas, Yu Huang, and Collin McMillan. 2023. Function Call Graph Context Encoding for Neural Source
Code Summarization. IEEE Transactions on Software Engineering (2023).

[2] Alexander LeClair and Collin McMillan. 2019. Recommendations for datasets for source code summarization. arXiv preprint arXiv:1904.02660 (2019).

[3] Michael L Collard, Michael John Decker, and Jonathan I Maletic. 2013. srcml: An infrastructure for the exploration, analysis, and manipulation of
source code: A tool demonstration. In 2013 IEEE International conference on software maintenance. IEEE, 516–519.

