def main():   # add colon here
    print("Starting program")
    
    for i in range(5):   # Add colon at end of loop declaration
        print(i)         # Close parenthesis is missing here
        
        if i==3:   # Add colon at start of condition statement and close quote 
            print("Found 3")  
            
    return "Done"  # Return value should be outside function, not inside. It's better to have a separate main() function call for this result.

main()  # Call the main function to run the program