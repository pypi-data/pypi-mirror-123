# Python Contactually Wrapper
 Feature complete wrapper module for the Contactually API v2. 
 
 Clone repository or install with 
 
 <code> pip install py-contactually </code>
 
Use the Contactually API documentation (https://developers.contactually.com/reference) as a reference for available endpoints and the data associated with each. With a few exceptions, module methods are aligned with the requests as listed on the reference page.

To begin using import the Contactually class: 

<code> from contactually import Contactually </code>

Each method returns a <code>Request</code> that you can inspect and alter before using the <code>Request().submit()</code> method to submit your request to the Contactually server. Most method arguments mirror the available query parameters or requirements listed with their accompanying resource in the Contactually documentaiton. 

Still a work in progress, but will eventually feature an object oriented way to add clients, buckets, and more. Open to contributions and suggestions. More comprehensive README.md to come. 
