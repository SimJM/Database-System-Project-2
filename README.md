# Database-System-Project-2

## Background
The relational query execution engine implements a set of physical operators. An operator takes as input one or more data streams and produces an output data stream. Some examples of physical operators are sequential scan, index scan, and hash join. These physical operators are the building blocks for the execution of SQL queries. An abstract representation of such an execution is a physical operator tree (operator tree for brevity), denoted as 𝑇𝑇 = (𝑁𝑁, 𝐸𝐸), where 𝑁𝑁 is a set of nodes representing the operators and 𝐸𝐸 is a set of edges representing data flow among the physical operators. The physical operator tree is the abstract representation of a query execution plan (QEP). The query execution engine is responsible for the execution of the QEP to generate results of a SQL query. You can view a QEP of a given query using the EXPLAIN feature of PostgreSQL.

It is often unclear to a user on what is happening “inside the box” of a database system when one poses an SQL query. For instance, which blocks/pages are being accessed by the query? Which tuples are there in these blocks? How much buffer is used?

## Purpose
The goal of your project is to shed light to various questions associated with a QEP by designing and implementing a software that facilitates visual exploration of disk blocks accessed by a given input SQL query as well as various features of the corresponding QEP.
Specifically, the input/output of your program is as follows:
  - Input: An SQL query
  - Output:
     - Visualization of disk blocks accessed by the query. It should also facilitate exploration of the content of these blocks interactively. 
     - Visualizing different aspects of the QEP including buffer size, cost, etc.

## Tasks
- Design and implement an algorithm that takes as input an SQL query and creates the above visual exploration framework. Your goal is to ensure generality of the solution (i.e., it can handle a wide variety of query plans on different database instances) as well as easy-to-use visual exploration. The better is the algorithm design for the task, the more credit you will receive.
- A user-friendly, graphical user interface (GUI) to enable the visual exploration goals. Note that a working GUI to show your results easily should suffice. It is not necessary to generate a fancy one as the course is not on GUI development.
