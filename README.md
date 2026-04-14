Design Choices & Assumptions
For this project, I focused on building a modular system that balances the specific constraints of the evaluation with real-world maintainability.

Parsing Logic: Since the requirement was to avoid standard CSV libraries, I built a custom parser from scratch. It doesn't just split strings; it uses a state-tracking approach to handle "quoted fields" and extra whitespace. This ensures that a name like "George Of The Jungle" doesn't break the logic if it's formatted differently in the source.

Database & Reliability:
I chose SQLite because it’s a standard, reliable relational engine that doesn't require complex setup for the person reviewing my code. I made a deliberate choice to "overwrite" the table on each CLI run. This ensures the output is always a clean reflection of the provided file, preventing data duplication.

Security & Cloud:
For the API, I implemented X-API-Key authentication. In a production environment like AWS or Azure, I would move this to an API Gateway with JWT tokens and transition the data to a managed service like RDS or Azure SQL. This separation of concerns makes the app easy to scale and secure.