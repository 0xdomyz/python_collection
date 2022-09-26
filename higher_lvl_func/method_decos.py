import functools

def dec1(x):
    def decorate(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            print(f"dec1 {x}")
            return func(*args, **kwargs)
        return new_func
    return decorate


class A:

    def __init__(self):
        #initialize a function that is a decorated method.
        self.func2 = dec1(1)(self._func)

    def dec2(self,x):
        """a method that is a wrapper of a decorator"""
        return dec1(x)

    def dec3(self,x):
        """a decorator method"""
        def decorate(func):
            @functools.wraps(func)
            def new_func(*args, **kwargs):
                print(f"dec1 {x}")
                return func(*args, **kwargs)
            return new_func
        return decorate

    def func3(self,x):
        """
        Examples
        ----------------
        Wrapper function that make use of a decorator method that is wrapper of
        decorator::
        
            a = A()
            a.func3(1)
            print(a.func3.__doc__)
        """
        func = self.dec2(1)(self._func)
        res = func(x)
        return res

    def func4(self,x):
        """
        Examples
        ----------------
        Wrapper function that make use of a decorator method::
        
            a = A()
            a.func4(1)
            print(a.func4.__doc__)
        """
        func = self.dec3(2)(self._func)
        res = func(x)
        return res

    @dec1(1)
    @dec1(2)
    @dec1(3)
    def func(self,x):
        """
        Examples
        ----------------
        Decorate a method::

            exit()
            python -i higher_lvl_func//method_decos.py 
        
            a = A()
            a.func(1)
            print(a.func.__doc__)
        """
        return x+1


    def _func(self,x):
        """
        Examples
        ----------------
        ::
        
            a = A()
            a.func2(1)
            print(a.func2.__doc__)
        """
        return x+1

if __name__ == "__main__":
    pass




