# RH_Factor

This Python script is searching for a pattern and prints the line of matching text in different specified formats.
The design pattern that is used for this exercise is Factory. 
The solution should be compatible with any Python3 version, it doesnt use any external libraries. Log file is created in 'logs' folder in current working directory. 

Execution command format is _python3 main.py -r <regex_pattern> -f <file/files to search> -u|-c|-m_
Where -f should be full/relative file path. When -f is omitted user will be prompted for input. 'STDIN' will appear as filename when results are printed. 

Few examples of usage and output:

_$ python3 main.py -r [J][a][z]+ -f input/input_1.txt -c_

![Screenshot from 2021-05-16 03-35-51](https://user-images.githubusercontent.com/18490872/118381853-08dab580-b5f8-11eb-93ff-3780fbfa247a.png)

_$ python3 main.py -r [J][a][z]+ -f input/input_1.txt -u_

![Screenshot from 2021-05-16 03-38-32](https://user-images.githubusercontent.com/18490872/118381895-67a02f00-b5f8-11eb-9579-4feb29d62797.png)

_$ python3 main.py -r [J][a][z]+ -f input/input_1.txt -m_

![Screenshot from 2021-05-16 03-40-57](https://user-images.githubusercontent.com/18490872/118381912-8b637500-b5f8-11eb-98d3-6a3df0199d7a.png)

_$ python3 main.py -r [J][a][z]+ -f input/input_1.txt input/input_2.txt input/input_3 -c_

![Screenshot from 2021-05-16 03-42-21](https://user-images.githubusercontent.com/18490872/118381953-ce254d00-b5f8-11eb-8e24-38c927b76cb6.png)

