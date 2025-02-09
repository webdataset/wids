# The Web Indexed Datasets Library

The Web Indexed Datasets Library (`wids`) is a library for reading
WebDataset datasets in PyTorch with indexed (random) access.  WebDataset
datasets are simply collections of standard POSIX tar files containing
training samples.

The `wids` library is a drop-in replacement for other indexed datasets
in Python.  Despite being indexed and random access, it can work
with datasets larger than local disk storage and performs incremental
downloads.  Under the covers, it uses a very fast memory mapped tar
file reader.
