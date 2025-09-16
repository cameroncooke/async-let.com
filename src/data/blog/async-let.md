---
title: Using Async Let
pubDatetime: 2025-03-30T00:00:00.000Z
tags:
  - Swift
  - Swift Concurrency
  - Concurrency
description: A quick dive into the async let pattern in Swift
---
Async let is a lesser-known (if you're me) feature of Swift Concurrency that allows you to perform concurrent operations and combine their results.

## Example

```swift
func fetchData() async throws -> (Data, Data) {
    async let firstData = fetchFirstData()
    async let secondData = fetchSecondData()
    return try await (firstData, secondData)
}

func fetchFirstData() async -> Data {
    Task.sleep(nanoseconds: 1000000000)
    return Data("First Data".utf8)
}

func fetchSecondData() async -> Data {
    Task.sleep(nanoseconds: 1000000000)
    return Data("Second Data".utf8)
}
```
In this example, `async let` is used to initiate two asynchronous tasks concurrently: `fetchFirstData()` and `fetchSecondData()`. Both tasks start at the same time, and their results are awaited together, allowing both tasks to run concurrently. The return statement is only called when both tasks have completed, neat!

Compare this to the following sequential approach:

```swift
func fetchData() async throws -> (Data, Data) {
    let firstData = try await fetchFirstData()
    let secondData = try await fetchSecondData()
    return (firstData, secondData)
}
```
In this example, the tasks are executed sequentially, with the second task waiting for the first task to complete before starting. This is the traditional way of handling asynchronous operations in Swift.

As you can see the sequential approach is less efficient, as the second task has to wait for the first task to complete before starting.

## Benefits of Using Async Let

- **Synchronous Style Syntax**: `async let` allows you to write asynchronous code that resembles synchronous code. This makes it easier to read and maintain, as it reduces the need for deeply nested closures or callback hell.
- **Concurrent Execution**: With `async let`, you can initiate multiple asynchronous tasks at once without waiting for each task to complete sequentially. This is particularly useful when tasks are independent.

## Caveats

While `async let` provides a straightforward way to manage concurrency in Swift, this simplicity comes with a trade-off in flexibility. Unlike task groups, `async let` does not allow for dynamic task management. This means that once tasks are defined, you cannot add or remove tasks dynamically during execution.
