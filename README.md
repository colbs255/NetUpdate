# NetUpdate

## Intro
Allows you to create a lightweight server on another thread while doing something else. Useful for when your computer is completing a long task and you want to keep up with it by connecting to the server via your phone or another computer.

## Example
You are a training a model that will take hours to complete. You want to let it run and be able to check the status without going back to the computer to check. Create a NetUpdate object and pass in a function that returns the learning progress to display. You can now connect to the server from any browser and check the progress.