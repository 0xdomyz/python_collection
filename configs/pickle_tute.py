import datetime
import pickle
from pathlib import Path

_pickle_path = Path(__file__).parent / "pickled_obj.pkl"

if __name__ == "__main__":

    dt = datetime.datetime.utcnow()

    with open(_pickle_path, "wb") as f:
        pickle.dump(dt, f)

    with open(_pickle_path, "rb") as f:
        res = pickle.load(f)

    print(res == dt)
