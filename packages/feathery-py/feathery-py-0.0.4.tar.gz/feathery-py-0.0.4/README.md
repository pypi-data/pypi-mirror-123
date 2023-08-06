# feathery
### A asynchronous, scaling first Discord API package wrapper. With built-in cli for code generation and deploying/running your package. Simple database integration and State caching for Discord API objects. And more to come.

##Feature TODO List:
- [ ] Hot reload during development
- [ ] Zero downtime re-deployment
- [ ] Automatic exception handling and recovery
- [ ] Discord Dispatch Event Models (MEMBER_JOIN, MEMBER_UPDATE, etc.)
- [ ] Resource Models (User, Member, Channel, etc.)
- [ ] Database models (MongoDB, MySql, TinyDB, SQLite)
- [ ] Asynchronous standalone sharding (Single core).
- [ ] Standalone vertical scaling using multiprocessing and standalone asynchronous shards (limited by cores and asynchronous shard efficiency).
- [ ] Automatic Horizontal scaling using AWS services (CloudFormation, ElasticBeanstalk, Lambda, etc.)
- [ ] Automatic project generation using a click cli and jinja2
- [ ] Automatic service generation using a click cli and jinja2
- [ ] Automatic model generation using a click cli and jinja2
- [ ] Built-In In-Memory Caching (Cache lost on restart)
- [ ] Built-In [TinyDB](https://tinydb.readthedocs.io/en/latest/getting-started.html) Caching Implementation
- [ ] Built-In [Motor (Asynchronous MongoDB)](https://docs.mongodb.com/drivers/motor/) Caching Implementation
- [ ] Maybe? Built-In [AWS Keyspaces](https://docs.aws.amazon.com/keyspaces/index.html) Caching Implementation (Idk about this though I can't find any asynchronous package on first search...)
- [ ] Automatically generate rest api

## Why?
- Well discord.py went and archived itself so thats incentive.
- I liked the idea of discord.py but when it came to the features that large bot's 
  needed you mostly had to extend the package yourself to handle those complexities.
  (Like sharding, Discord api state caching, Database interaction, rest api)

## Sharding, How?
When sharding you start with your asynchronous services. Each service (which can handle event's, expose a rest api, etc)
will be run as seperate tasks on a single shard. Eventually (when your bot gets large enough, or your code gets
inefficient enough) your tasks don't get handled fast enough. If your code is very efficient this will become evident
when the core the python process is running on will be around 100% constantly (if you have i.o. bound tasks in your code
or complex/long-running code, service runtimes are monitored and logged...)

## Dependencies
Package | Description | Link To Package
--------|-------------|----------------
click | Command line interface | [Click Here](https://click.palletsprojects.com/)