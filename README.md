# pmux
A library aiming to ease development of distributed programs by composing a message queue and typed serialization format, both having implementations in many languages, with a POSIX inspired message structure; transcending the language barrier.
When using the PmuxServer and PmuxClient, functions are executed remotely using ComputationRequest and ComputationResponse messages, as in the example below:
```python
computation_request = {
    "function_name": "hello_world",
    "stdin": [],
    "meta": {}
}
computation_response = {
    "function_name": "hello_world",
    "stdout": [],
    "stderr": [],
    "meta": {}
}
```

An additional paradigm is "functions are processes", or infinitely iterating function executions.
This is the idea behind PmuxNode.
All you need to do is implement the iterate function and use PmuxMessage:
```python
msg = {
    "source": "source node",
    "destination": "destination node",
    "stdin": []
    "meta": {}
}
```


Using a serialization protocol containing types allows us to reason the values of our messages.
Using a message queue encapsulating multiple architecture patterns and transport backends facilitates efficiency of implementation while remaining simple.
These facts combined with interface implementations in multiple languages, for both the serialization protocol and the message queue, leaves us with a powerful way to develop distributed applications independent of language.

## TODO
0. Strip out anything extra
1. Clean up and revise PmuxNode
2. Create tests and implement CI

## STATUS
This is still pretty alpha.
Can't say I didn't warn you.
