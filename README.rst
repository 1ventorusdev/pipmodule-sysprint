========
sysprint
========
*help to create text*

Install and import
------------------

- For install sysprint : pip install sysprint
- For import sysprint: import sysprint

Functions
---------

- For loading:
    - Print.Loading.spinner(text, function to execute) 
        exemple:
                
                Print.Loading.spinner("loading... ", time.sleep(5))
                => loading... | # animated rotation

    - Print.Loading.bar(symbol, text, func, end symbol (default="OK"))
        exemple:

                Print.Loading.bar("*", "loading...", time.sleep(5))
                => [*     ]  loading...
                *30s later*
                   [  *   ]  loading...
                *at end of execution of function*
                   [  OK  ]  loading...

- For information and other:
    - Print.status(align, status, text) #align obligatory value is c for this moment
        exemple:

                Print.status("c", "SET", "modification of data")
                => [ SET  ]  modification of data

- For Execute a list of function or dico
    - *list1 = [func1, func2] | dico1 = {func1: "text", func2: "text"}*
    - Print.Execute.list(symbol, list of function, end symbol (default="OK"))
        exemple:
            
                Print.Execute.list("*", list1)
                => identic to loading bar but the end symbol spawn after executed all function in list, the text is "function {name of function}"
    
    - Print.Execute.dico(symbol, dico of function, end symbol (default="OK"))
        exemple:
                
                Print.Execute.list("*", dico1)
                => identic to loading bar but the end symbol spawn after executed all function in list, the text is defined by value of function key in dico 

- For other data to add in text:
    - timer()
        exemple:
                
                "timer()today i am happy"
                => [12:37:40.563]  today i am happy
