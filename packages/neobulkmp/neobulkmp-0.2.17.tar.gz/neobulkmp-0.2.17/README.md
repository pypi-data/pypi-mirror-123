# neo-mp-loader

res:
redis
graphio
jsonpickle



STATUS:

target_nodeSets in RelSetMeta need to be not based on existing nodesets but must be rely on relkey data to provide blocking data
# Strategies

* Seperated Datasets
    + Nodes and Relations are not interconnected to other datasets/workers
    + We can just run the relations after the nodes are created/merged
* Capsuled Datasets
    + Nodes and Relations are in one dataset, but nodes between datasets can overlap when merged
    + We need to make sure that the two nodeSets between a RelSet, and the RelSet itself, is in a stable status (=only finished workers discharged in these nodesets and the relset. no currently running worker are allowed to discharge in these nodeset and the relset) before loading the relations
* Mixed Datasets
    + Nodes and Relations are scattered over multiple datasets/workers.
    + We first need to load all nodes before loading relations.
    + this could blast memory on large loading runs. any ideas? maybe an emergency discharge to disk if relations are eating too much memory? quite complex...


# Issues

* Make sure that new related NodeSetLoading workers are blocked if a RelationshipSetLoading Worker is waiting for a drain and/or loading. otherwise we could provoke nodelocks

* Tidy up:_
    * Finished Drain orders should remove  entries from "DRAIN_ORDERS_NODESETS_DONE"
    * Finished Drain orders can be removed from "DRAIN_ORDERS_READY"
    * Remove unnessecary drain state "DRAIN_ORDERS_FIN_KEY"

# ToDo


* Loading worker shoud get trigger if a min amount of data is in cache (as long as there a still sourcing workers pumping data)
* Docu
* Status api (resulting in possible WebUI)
* replace redis-py with aioredis


# Docu shards

## Set retry count for failed neo4j merge/create transactions

```python
from neobulkmp import Manager, WorkerSourcing

[...]

manager = Manager(worker_sourcing_class=WorkerSourcing,
                  worker_parameters=movies)
manager.worker_loading_class.amount_of_retries_on_loading_fail = 3 # defaults to 4
```

## Cache Memory

### Cache Memory total available

```python
from neobulkmp import Manager, WorkerSourcing

[...]

manager = Manager(worker_sourcing_class=WorkerSourcing,
                  worker_parameters=movies)
manager.strategy.cache_storage_total = "16 GB" # defaults to total memory * 0.80 of manager host
```
### Cache Memory Limit

With neobulkmp.manager_strategy.StrategyBase.cache_storage_warning_limit and  neobulkmp.manager_strategy.StrategyBase.cache_storage_clogged_limit
 
```python
from neobulkmp import Manager, WorkerSourcing

[...]

manager = Manager(worker_sourcing_class=WorkerSourcing,
                  worker_parameters=movies)
manager.strategy.cache_storage_warning_limit = 70 # defaults to 85
manager.strategy.cache_storage_clogged_limit = 80 # defaults to 95
```


### Error too many open files

https://neo4j.com/docs/operations-manual/current/installation/linux/tarball/#linux-open-files