# Optimization Library 

The optimization library measures the general speed of a program based on the last run.

![alt text](https://media1.giphy.com/media/YHYmMLkOmqoo/giphy.webp?cid=ecf05e47v65rqtldq6gxecdovfuuw6sw99cg7jccb7ityvrw&rid=giphy.webp&ct=g)

## Example Usage:
First, import the library:

    import OptimizationLibrary 

Next, the library needs to be initialized:

    opt = OptimizationLibrary()

Finally, we can start and stop the timer:
    
    opt.start_timer()
    opt.end_timer()

## Example File

    import optimization
    def test():
        opt = optimization.OptimizationLibrary() 
        opt.start_timer()
        your_function()
        opt.end_timer()
    if __name__ == '__main__':
        test()

### Additional Notes: 

This is a developer tool. \
The library has a small performance window (to account for natural program variance). \
The library can also be initialized with an optional parameter to show performance increases/decreases visually:        

    opt = optimization.OptimizationLibrary(variance=2.5, color=True) 
