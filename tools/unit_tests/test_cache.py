import os, sys, inspect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

sys.path.insert(0, parent_dir)


from demo_data_gen import get_demo_data

from rtg_cache import RTGCache


if __name__ == '__main__':
    demo = RTGCache()

    demo.data = get_demo_data()  # Only for unit test

    print("Cache: Should be graphing flat lines.")

    demo.start()
