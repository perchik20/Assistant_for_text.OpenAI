# Assistant_for_text.OpenAI

Assistant for text recognition with OpenAI

This program is designed to make it easy to find the answer to a question on a given topic (A bot for cheating. 
I do not approve of this, all for the sake of experiment)
The program is divided into 2 components: A Bot and a Website
Bot - takes a photo with the answers to the test and the name of the work (so that it is easier to navigate the tests), 
after receiving the picture, it will be saved in a separate folder. After that, in a separate function, using the openal library tesseract, 
the photo from the picture is converted into text and stored in a database for further extraction
Website - there is a search bar on the site in which the user scores part of the question and with the help of the code, 
a search is performed on the database of data. After several lines of a question or even words are entered, 
the program immediately displays possible answers, this is realized thanks to AJAX requests. 
Also, in addition, there is a correction of the entered words using the fuzzy fuzzy library.
