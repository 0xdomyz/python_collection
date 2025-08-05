class SmartRepr:
    def __repr__(self):
        items = []
        for k, v in self.__dict__.items():
            try:
                item = f"{k}={repr(v)}"
                assert len(item) < 100
            except Exception:
                item = f"{k}=<{type(v).__name__}>"
            items.append(item)
        return f"{self.__class__.__name__}({', '.join(items)})"