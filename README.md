# custom_forms
# The Challenge
Your goal is to define the data model persisted in the database and any non-obvious business logic to create and send custom forms like in Google Forms. You should approach this problem as if you're building Google Forms, not a feature in Ashby.

# Requirements
The data model should express how custom forms are designed, sent, and submitted. For simplicity, don't define a user model or how authentication works. Assume, like in Google Forms, a user can submit a survey anonymously.

### Field types
We want to support the following form fields:
* Plain text box 
* Email text box 
* Single select dropdown 
* Boolean field 
* File field

### Persistence
The data model should reflect what is persisted in the database and, for simplicity, should be represented as objects with properties and relationships to other objects. Define it as you would in an ORM like ActiveRecord (rather than as tables in SQL). Assume that you're designing an API for a stateless server.

### Conditional fields
We want a user to define a field that only becomes visible if a previous field has a specific value. Users can combine conditions with ANDs and ORs. For example:
1. Do you like lunch? (Y/N)
2. Do you like toast (Y/N)
3. Do you like pancakes? (Y/N)
4. Do you like brunch? (Y/N) Conditional on (1 == Y AND (2 == Y OR 3 == Y))
You must represent conditions as structured data (e.g., don't model it as a string).

### And Anything Else
Document other requirements, details, or future considerations that you think are important for this product!
