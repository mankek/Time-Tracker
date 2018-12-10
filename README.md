This project is focused on the creation of an application (Python-Django) to record time-tracking information of
employees via a user-friendly platform with multiple features that allow for easy control and display of the information.

**Starting the Application**

This application comes with a virtual environment, tt_env, that can be found within the projects Time Tracker directory
and provides all of the needed dependencies. Once cloned and with the virtual environment running, the application can
be run like any typical Django application.

Navigate into the project directory and run the following command:

    python manage.py runserver

The application will start up on port 8000.

**Admin Mode**

New employee accounts and new Categories can only be made from the Admin site of the application.

An employee's password is set when they are first created, but the field is not available when an existing employee
is edited.

**Using the Application**

Once a user has logged in, there are 4 tabs they are able to interact with. The details of these tabs are explained
below.

*Time Form*

This page displays the form for adding a new time-tracking entry. The first four fields are required.

Work Categories: Each task will have a Category, describing the general group that the task performed belongs to and a
Subcategory that allows for more specific classification of tasks, such as the type of task or project it belongs to.

Description: A brief description of what exactly was accomplished.

Date: The date on which the task was performed. **Past dates and the current dates can be used, but future dates will
no be accepted.**

Hours & Minutes: These fields are the *first of two* optional ways to enter time information. The maximum number of hours that
can be entered is 10 and the minutes are entered in increments of 15, with the max being 45 (even if numbers that are
not multiples of 15 are entered, the closest multiple of 15 will be calculated and recorded).

Time Start & Time End: These fields are the *second of two* optional ways to enter time information. The maximum
number of hours that can be entered is 10 and the minute difference is automatically rounded to a multiple of 15.

Optional Parameters:

Entries for multiple employees can be made by using the Username fields to add employees (other than oneself) to a
'team'. When an employee is added, their username will appear in the large white box below the 'Add to Team' button.
Double-clicking a username in the box will remove that employee from the team. When there are team members present, all
of the information the user entered in the time form will also be used to make an entry in each team member's time
records.

A task entry can be marked as rework by clicking the Rework checkbox.

Clear Form: Clicking this will clear all fields (with the exception of Work Categories, which will go back to its
default values).


*Entry History*

This page displays a search form which allows the user to search through their own records for specific entries.
Currently, records can only be searched by Category, Subcategory and Date. Using the value 'all' will bring up tasks of every
Category and/or Subcategory; leaving Date without a value ("mm/dd/yyy") will bring up tasks for every date.


*Categories*

This page displays every existing Category-Subcategory pair and a form for creating a new Subcategory under a selected
Category.


*Analyze*

This page displays an interactive chart that shows the percentage of the users tasks that fit a certain criteria.
Currently, tasks can be graphed according to Category, whether or not they are rework tasks and how many hours were spent
on the task. They can also be filtered based on when they occurred. Leaving all of the time Span options unchecked will
graph tasks from any date.

