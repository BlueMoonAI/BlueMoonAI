import gradio as gr
import os
import random

def character_custom_wildcards_ui(prompt):
    # Create a tab wildcards_enhance wildcard enhancement
    with gr.Tab(label="Characters Wildcards", default=True, identifier="characters_wildcards"):

       # Specify the folder as a subfolder wildcards in the current directory
        wildcards_path = './characters'

       # Read all txt file names in the wildcards folder, excluding the suffix txt
        wildcard_file_names = [os.path.splitext(file_name)[0] for file_name in os.listdir(wildcards_path) if file_name.endswith(".txt")]
    # Add "__" before and after each string in the wildcard_file_names list to form a string like __xxx__
        wildcard_file_names = ["__" + file_name + "__" for file_name in wildcard_file_names]

        with gr.Row():
            # Create a click button with the label "Add pinch data to the prompt box"
            add_artist_to_prompt_button = gr.Button(label="add Custom Characters To The Prompt Box", value="Add to Prompt", scale=2)
           #Create a checkbox labeled "Clear the original prompt words before adding"
            clear_before_add_prompt_checkbox = gr.Checkbox(label="Clear before add", value=True)


        wildcard_artist_file_names = ['shot', 'gender', 'region', 'age', 'bodytype', 'angle', 'job', 'faceshape', 'hairstyle', 'haircolor',
                                           'eye', 'bangs', 'beard', 'otherfeatures', 'faceexp', 'chest', 'waist', 'legs', 'gesture', 'pose', 'hanfu',
                                           'suit', 'topwear', 'bottomwear', 'socks', 'shoes', 'accessories', 'lighting', 'color', 'camera', 'quality',
                                           'artist', 'preset']


        #Initialize an empty dictionary to save all drop-down menu options
        wildcard_artist_dropdown_choices = {}

        #Define a reading function read_wildcard_artist_file to read the specified wildcard file so that it can be called repeatedly later
        def read_wildcard_artist_file(wildcard_artist_file_names):
            for x_file_name in wildcard_artist_file_names:
                with open(os.path.join(wildcards_path, f'{x_file_name}.txt'), 'r') as f:
                 # Save the contents of each file into the dictionary, with the file name as the key and the file content as the value
                    wildcard_artist_dropdown_choices[x_file_name] = [line.strip() for line in f.readlines()]

        read_wildcard_artist_file(wildcard_artist_file_names)
        #printTheContentsOfTheDictionary
        #print(wildcard_artist_dropdown_choices)

     # Assign the contents of each saved file to the options of the drop-down menu
        with gr.Tab(label="General"):
            with gr.Row():
                wildcard_11_dropdown = gr.Dropdown(label="Shot", choices=wildcard_artist_dropdown_choices['shot'], value=wildcard_artist_dropdown_choices['shot'][0], scale=2)
                wildcard_11_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.3, scale=1)

                wildcard_12_dropdown = gr.Dropdown(label="Gender", choices=wildcard_artist_dropdown_choices['gender'], scale=2)
                wildcard_12_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.1, scale=1)

                wildcard_13_dropdown = gr.Dropdown(label="Region", choices=wildcard_artist_dropdown_choices['region'], scale=2)
                wildcard_13_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.1, scale=1)

                wildcard_14_dropdown = gr.Dropdown(label="Age", choices=wildcard_artist_dropdown_choices['age'], scale=2)
                wildcard_14_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.1, scale=1)

                wildcard_15_dropdown = gr.Dropdown(label="Body Type", choices=wildcard_artist_dropdown_choices['bodytype'], scale=2)
                wildcard_15_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.1, scale=1)

                wildcard_16_dropdown = gr.Dropdown(label="Angle and Gaze", choices=wildcard_artist_dropdown_choices['angle'], value=wildcard_artist_dropdown_choices['angle'][4], scale=2)
                wildcard_16_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.1, scale=1)

                wildcard_17_dropdown = gr.Dropdown(label="Job", choices=wildcard_artist_dropdown_choices['job'], scale=2)
                wildcard_17_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=1.1, scale=1)

        with gr.Tab(label="Face"):
            with gr.Row():
                wildcard_21_dropdown = gr.Dropdown(label="Face Shape", choices=wildcard_artist_dropdown_choices['faceshape'], scale=2)
                wildcard_21_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_22_dropdown = gr.Dropdown(label="Hair Style", choices=wildcard_artist_dropdown_choices['hairstyle'], scale=2)
                wildcard_22_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_23_dropdown = gr.Dropdown(label="Hair Color", choices=wildcard_artist_dropdown_choices['haircolor'], scale=2)
                wildcard_23_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_24_dropdown = gr.Dropdown(label="Eye", choices=wildcard_artist_dropdown_choices['eye'], scale=2)
                wildcard_24_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_25_dropdown = gr.Dropdown(label="Bangs", choices=wildcard_artist_dropdown_choices['bangs'], scale=2)
                wildcard_25_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_26_dropdown = gr.Dropdown(label="Beard", choices=wildcard_artist_dropdown_choices['beard'], scale=2)
                wildcard_26_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_27_dropdown = gr.Dropdown(label="Other Features", choices=wildcard_artist_dropdown_choices['otherfeatures'], scale=2)
                wildcard_27_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_28_dropdown = gr.Dropdown(label="Facial Expression", choices=wildcard_artist_dropdown_choices['faceexp'], scale=2)
                wildcard_28_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)


        with gr.Tab(label="Body"):
            with gr.Row():
                wildcard_31_dropdown = gr.Dropdown(label="Chest", choices=wildcard_artist_dropdown_choices['chest'], scale=2)
                wildcard_31_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_32_dropdown = gr.Dropdown(label="Waist", choices=wildcard_artist_dropdown_choices['waist'], scale=2)
                wildcard_32_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_33_dropdown = gr.Dropdown(label="Legs", choices=wildcard_artist_dropdown_choices['legs'], scale=2)
                wildcard_33_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_34_dropdown = gr.Dropdown(label="Gesture", choices=wildcard_artist_dropdown_choices['gesture'], scale=2)
                wildcard_34_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_35_dropdown = gr.Dropdown(label="Pose", choices=wildcard_artist_dropdown_choices['pose'], scale=2)
                wildcard_35_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

        with gr.Tab(label="Attire"):
            with gr.Row():
                wildcard_40_dropdown = gr.Dropdown(label="Hanfu", choices=wildcard_artist_dropdown_choices['hanfu'], scale=2)
                wildcard_40_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_41_dropdown = gr.Dropdown(label="Suit", choices=wildcard_artist_dropdown_choices['suit'], scale=2)
                wildcard_41_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_42_dropdown = gr.Dropdown(label="Topwear", choices=wildcard_artist_dropdown_choices['topwear'], value=wildcard_artist_dropdown_choices['topwear'][0], scale=2)
                wildcard_42_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_43_dropdown = gr.Dropdown(label="Bottomwear", choices=wildcard_artist_dropdown_choices['bottomwear'], scale=2)
                wildcard_43_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_44_dropdown = gr.Dropdown(label="Socks", choices=wildcard_artist_dropdown_choices['socks'], scale=2)
                wildcard_44_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_45_dropdown = gr.Dropdown(label="Shoes", choices=wildcard_artist_dropdown_choices['shoes'], scale=2)
                wildcard_45_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_46_dropdown = gr.Dropdown(label="Accessories", choices=wildcard_artist_dropdown_choices['accessories'], scale=2)
                wildcard_46_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)


        with gr.Tab(label="Other"):
            with gr.Row():
                wildcard_51_dropdown = gr.Dropdown(label="Lighting", choices=wildcard_artist_dropdown_choices['lighting'], scale=2)
                wildcard_51_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_52_dropdown = gr.Dropdown(label="Color", choices=wildcard_artist_dropdown_choices['color'], scale=2)
                wildcard_52_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_53_dropdown = gr.Dropdown(label="Camera Parameters", choices=wildcard_artist_dropdown_choices['camera'], scale=2)
                wildcard_53_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_54_dropdown = gr.Dropdown(label="Quality Words", choices=wildcard_artist_dropdown_choices['quality'], scale=2)
                wildcard_54_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_55_dropdown = gr.Dropdown(label="Artist", choices=wildcard_artist_dropdown_choices['artist'], value=wildcard_artist_dropdown_choices['artist'][0], scale=2)
                wildcard_55_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)

                wildcard_56_dropdown = gr.Dropdown(label="Preset", choices=wildcard_artist_dropdown_choices['preset'], scale=2)
                wildcard_56_weight = gr.Slider(label='Weight', minimum=-2, maximum=2, step=0.1, value=0.9, scale=1)


        #Create a button click event handler, splice the pinch data prompt word and add it to the prompt box
        def add_artist_to_prompt(prompt, clear_before_add_prompt_checkbox, *args):

            # If the "Clear original prompt words before adding" checkbox is selected, clear the prompt.
            if clear_before_add_prompt_checkbox:
                prompt = ""

           # Process "lens type" wildcard_11_dropdown and wildcard_11_weight separately
            x_dropdown = args[0]
            x_weight = args[1]
            if f"{x_dropdown}" != "None" and x_dropdown != "" and f"{x_weight}" != "None" and x_weight != "":
                prompt = f"a masterpiece of ({x_dropdown}:{x_weight}) " + prompt

          # Splice the pinch data prompt words and add them to the prompt box
            for i in range(2, len(args), 2):
                x_dropdown = args[i]
                x_weight = args[i+1]
                if f"{x_dropdown}" != "None" and x_dropdown != "" and f"{x_weight}" != "None" and x_weight != "":
                    prompt += f", ({x_dropdown}:{x_weight})"
            return prompt

        #Set the button click event handler, accept parameters, execute the function, and finally return to prompt and add the pinch data prompt word to the prompt box
        add_artist_to_prompt_button.click(add_artist_to_prompt, inputs=[
            prompt, clear_before_add_prompt_checkbox,
            wildcard_11_dropdown, wildcard_11_weight,
            wildcard_12_dropdown, wildcard_12_weight,
            wildcard_13_dropdown, wildcard_13_weight,
            wildcard_14_dropdown, wildcard_14_weight,
            wildcard_15_dropdown, wildcard_15_weight,
            wildcard_16_dropdown, wildcard_16_weight,
            wildcard_17_dropdown, wildcard_17_weight,

            wildcard_21_dropdown, wildcard_21_weight,
            wildcard_22_dropdown, wildcard_22_weight,
            wildcard_23_dropdown, wildcard_23_weight,
            wildcard_24_dropdown, wildcard_24_weight,
            wildcard_25_dropdown, wildcard_25_weight,
            wildcard_26_dropdown, wildcard_26_weight,
            wildcard_27_dropdown, wildcard_27_weight,
            wildcard_28_dropdown, wildcard_28_weight,

            wildcard_31_dropdown, wildcard_31_weight,
            wildcard_32_dropdown, wildcard_32_weight,
            wildcard_33_dropdown, wildcard_33_weight,
            wildcard_34_dropdown, wildcard_34_weight,
            wildcard_35_dropdown, wildcard_35_weight,

            wildcard_40_dropdown, wildcard_40_weight,
            wildcard_41_dropdown, wildcard_41_weight,
            wildcard_42_dropdown, wildcard_42_weight,
            wildcard_43_dropdown, wildcard_43_weight,
            wildcard_44_dropdown, wildcard_44_weight,
            wildcard_45_dropdown, wildcard_45_weight,
            wildcard_46_dropdown, wildcard_46_weight,

            wildcard_51_dropdown, wildcard_51_weight,
            wildcard_52_dropdown, wildcard_52_weight,
            wildcard_53_dropdown, wildcard_53_weight,
            wildcard_54_dropdown, wildcard_54_weight,
            wildcard_55_dropdown, wildcard_55_weight,
            wildcard_56_dropdown, wildcard_56_weight

           # You can continue to add more dropdowns and weights
        ], outputs=[prompt])


        with gr.Row():
           # Create a click button with the label "Give me inspiration, pick random people", first clear the original prompt words, and then add the random preset to the prompt box
            add_randompreset_to_prompt_button = gr.Button(label="Give me inspiration and randomly pinch people", value="Randomize Character", scale=3)

            # Create a click button with the label "Reread wildcard file content, refresh options" (unfinished)
            #wildcard_refresh_button = gr.Button(label="refreshOptions", value="refreshOptions", scale=1, visible=False)


     #Create a button click event handler, click the "Random Pinch" button, and add a random line of prompt words in the __preset__ preset to the prompt box
        def add_random_to_prompt(prompt):
            # First clear the original prompt words, and then add a random line of prompt words in the default file to the prompt box
            prompt = "---" + random.choice(wildcard_artist_dropdown_choices['artist']) + ", " + random.choice(wildcard_artist_dropdown_choices['preset'])
            return prompt

 # Set the button click event handler, click, accept parameters, execute the function, return prompt, and add __wildcard__ to the prompt box
        add_randompreset_to_prompt_button.click(add_random_to_prompt, inputs=[prompt],outputs=[prompt])



        with gr.Row():
          #Create a drop-down menu "Select Wildcard File", the option is the txt file name in the wildcard folder to be read, excluding the suffix .txt
            wildcard_file_names_dropdown = gr.Dropdown(label="Select Wildcard File", choices=wildcard_file_names, value="__color__", scale=2)

            # Create a click button with the label "Add wildcard to prompt box"
            add_wildcard_file_name_to_prompt_button = gr.Button(label="add Wildcard Characters To The Prompt Box", value="Add Wildcard to Prompt", scale=1)

        #Create a button click event handler, obtain the selected value of the drop-down menu, and then assign the result to the text in the prompt box
        def add_wildcard_file_name_to_prompt(prompt,wildcard_file_names_dropdown):
           # Add the obtained drop-down menu option value result to the prompt box
            prompt += f", {wildcard_file_names_dropdown}"
            return prompt

       # Set the button click event handler, click, accept parameters, execute the function, return prompt, and add __wildcard__ to the prompt box
        add_wildcard_file_name_to_prompt_button.click(add_wildcard_file_name_to_prompt, inputs=[prompt,wildcard_file_names_dropdown],outputs=[prompt])