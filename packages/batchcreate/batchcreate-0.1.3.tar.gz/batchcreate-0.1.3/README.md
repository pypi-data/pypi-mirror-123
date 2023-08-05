Batchcreator takes an array of records as input and splits it into suitably sized batches of records which can be further processed or passed to any other system/s.

Quick start:

1.Install:

    $ pip install batchcreate

2.Import BatchCreator iterator class and instantiate it. You can use below parameters to define output batch limits. These parameters are optional. If neither of these parameters is specified then the default values will be used. The default limits as :


   - max_record_size=1MB

      The maximum size limit for a record in the output batch. Any record with larger size than this will be skipped from batching. 
   
   - max_batch_size=5MB

      The maximum size limit for a batch. 
   
   - max_batch_num_records=500

      The maximum number of records limit for a batch. BatchCreator will put maximum these many records per batch provided batch size satisfies the limit. 
   

    from batchcreate import BatchCreator
    
    batches = BatchCreator(records,
                           max_record_size=60,
                           max_batch_size=200,
                           max_batch_num_records=4)

3.The iterable BatchCreator object can give suitable batches as needed on iteration. The BatchCreator object can be used in a regular 'for' loop.

    for batch in batches:
        print(batch) #batch processing here
        print('\n')
   
   OR
     
    batchItr = iter(batches)
    print(next(batchItr)) #batch processing here

4.BatchCreator can return the list of all the batches as well.

    batches = BatchCreator(records).batches()

Docs:

[batchcreate](https://pypi.org/project/batchcreate/)
[Batchcreate Documentation](https://batchcreate.readthedocs.io/en/latest/)