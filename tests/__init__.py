
# tesing documentation,


# naming is important, where {file_name, function_name}, must start with test_<any_name>

# this __init__ file is important for creating a packge not just for testing it's general concept .

# to test a function write in command : $pytest -v
# -v, for show the test function and write either passed or field it's good for seeing, ``

# can pass different paramter for the same function to test it with more than one parameter
# e.g. @pytest.mark.paramterize("num1, num2, expeceted", [ (1, 2, 3), (), (), ...etc ]  )
# then with using must specify those variables to be used as a dynamic and pytest would change the value with each unique test based on number of list being speicifed in the parametarized annotation. 

# can execute a specific code before any function to start it's test, like @before annotation in android, 
# using a specific function annotation called :  ' fixture '
# e.g. @pythest.fixture
#      def before_func_test(# do any intialization being exeute before any test function )

# finally have to send this function being annotated with the fixture annotation as a parameter 
# into the test function just as a parameter without calling the () 
# e.g. def test_case(before_func_test), then use this parameter as variables of what ever return from the function, 

# note : you can create as much as you can from the fixture annotation functions. 

# how to make pytest expected to rais an exception, can using the 
#  " with pytest.raises(Exception): execute_function_would_rais_exception "

