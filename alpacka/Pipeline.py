from alpacka.pipes.ncof_pipeline import ncof_pipeline
from alpacka.pipes.tfidf_pipeline import tfidf_pipeline

class Pipeline:
    def __init__(self):
        self.ncof = ncof_pipeline()
        self.ncof.set_class_perspective(1)
        self.tfidf = tfidf_pipeline()


def main():
    pipe = Pipeline()
    pipe.ncof.print_all_methods()
    pipe.tfidf.print_all_methods()

if __name__ == '__main__':

    main()
