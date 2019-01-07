# Jenkins-Job-automation-using-Gmail-API

A python model that can be configured with your Gmail so that if it recieves a mail from any specific sender it automatically reads it and search
for any specific keyword that say to trigger and a job name.

Then this model interacts with jenkins and run that specific job automaticaly - with or without parameters , as provided in the mail.

Workflow --->
  
    * Check for mail from a specific sender in regular interval.
    * Reads the mail and its content in case of required sender mail.
    * Extract job name and parameters if in case mail says to <b>trigger</b> job.
    * Interact with Jenkins api and run that specific job along with the parameters given.
    
 This model can also be scheduled at set time interval, so that it automatically checks for new email at certain period of interval throughout the day. 
