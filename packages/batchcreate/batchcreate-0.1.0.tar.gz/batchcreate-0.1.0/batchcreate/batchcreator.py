import sys


class BatchCreator:
    """
    Instantiate a batching operation. The array input data will be split into batches
    of required batch size consisting of records of given size.

    Attributes:
        records : []
            Input list of records to split into batches.
        max_record_size : int
            The maximum size limit for a record.
        max_batch_size : int
            The maximum size limit for a batch.
        max_batch_num_records : int
            The maximum number of records limit for a batch.

    Methods:
        batches :
            Lists batches created.
    """

    def __init__(
        self,
        records,
        max_record_size=1000000,
        max_batch_size=5000000,
        max_batch_num_records=500
    ):
        """
        Instantiates BatchCreator. If the arguments max_record_size, max_batch_size and
        max_batch_num_records are not passed then uses the default values.

        :param records (list): Input list of records to split into batches.
        :param max_record_size (int, optional): The maximum size limit for a record if other than default.
        :param max_batch_size (int, optional): The maximum size limit for a batch if other than default.
        :param max_batch_num_records (int, optional): The maximum number of records limit for a batch if other
        than default.
        """
        self.records = records
        self.max_record_size = max_record_size
        self.max_batch_size = max_batch_size
        self.max_batch_num_records = max_batch_num_records

    def _get_batch_size(self):
        """
        Gets the size of a batch.

        :return: The size of a batch.
        """
        return sys.getsizeof(self.batch)

    def _get_batch_num_records(self):
        """
        Gets the number of records of a batch.

        :return: The number of records of a batch.
        """
        return len(self.batch)

    def _get_record_size(self, record):
        """
        Gets the size of a given record.

        :param record: A record from input list of records.
        :return: The size of the record.
        """
        return sys.getsizeof(record)

    def _validate_batch_size(self, record):
        """
        Checks if the current batch size will be less than the max_batch_size limit
        upon adding the new record. Returns True if less than max_batch_size else False.

        :param record: A record from input list of records.
        :return: Returns True if less than max_batch_size else False.
        """
        new_batch_size = (self._get_batch_size() + self._get_record_size(record))
        return new_batch_size < self.max_batch_size

    def _validate_batch_num_records(self):
        """
        Checks if the number of records in the batch are less than the
        max_batch_num_records limit.

        :return: Returns True if less than max_batch_num_records else False.
        """
        return self._get_batch_num_records() < self.max_batch_num_records

    def _validate_record_size(self, record):
        """
        Checks if the size of the record is less than the max_record_size limit.

        :param record: A record from input list of records.
        :return: Returns True if less than max_record_size else False.
        """
        return self._get_record_size(record) < self.max_record_size

    def __iter__(self):
        """
        Creates BatchCreator iterator object.
        Creates generator iter_records from input records list and an empty batch
        to save the valid records.

        :return: BatchCreator iterator object.
        """
        self.iter_records = (r for r in self.records)

        self.batch = []
        return self

    def __next__(self):
        """
        If the records generator exists then traverse through it. Check if the
        record is of valid size. If the record is not of valid size then skip it.
        If the record is of valid size then check if the current batch is of valid size
        and has less records than the max_batch_num_records limit. If yes then add
        the record to the current batch else create a new batch having this record.

        :return: Batch of record/s.
        """
        batch = self.batch

        if not self.iter_records:
            raise StopIteration

        for record in self.iter_records:
            if self._validate_record_size(record):
                if self._validate_batch_num_records() and self._validate_batch_size(record):
                    batch.append(record)
                else:
                    self.batch = [record]
                    return batch

        self.iter_records = None
        return batch

    def batches(self):
        """
        Creates a list of batches by iterating over BatchCreator iterator.

        :return: List of batches.
        """
        return list(iter(self))
