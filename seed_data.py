from app import create_app
from models import db, User, Exam, Question, ExamResult, StudentAnswer
from datetime import datetime, timezone

def seed_database():
    app = create_app()
    with app.app_context():
        # Recreate tables cleanly
        db.create_all()
        print("Database tables created.")

        # Check if already seeded
        if User.query.first():
            print("Database already contains data. Skipping initial seeding.")
            return

        print("Seeding initial users, exams, and questions...")

        # 1. Admin Account
        admin = User(
            name="Dr. Faculty Head (Admin)",
            email="admin@presidency.edu",
            role="admin",
            department="Computer Science and Engineering"
        )
        admin.set_password("Admin@123")
        db.session.add(admin)

        # 2. Student Accounts
        student1 = User(
            name="Student Candidate",
            roll_no="20241CSE0750",
            email="student@presidency.edu",
            role="student",
            department="Computer Science and Engineering",
            semester="4th Semester"
        )
        student1.set_password("Student@123")
        db.session.add(student1)

        student2 = User(
            name="Eknath",
            roll_no="20241CSE0752",
            email="eknath@presidency.edu",
            role="student",
            department="Computer Science and Engineering",
            semester="4th Semester"
        )
        student2.set_password("Student@123")
        db.session.add(student2)

        db.session.commit()
        print("Created Admin and Student accounts.")

        # 3. Create Exam 1: CSE2271
        exam1 = Exam(
            title="System Architecture, UML Modeling & Software Design",
            course_code="CSE2271",
            description="Comprehensive mid-term evaluation covering UML Use Case & Activity diagrams, software engineering patterns, algorithmic complexity, and ACID database integrity.",
            duration_minutes=45,
            total_marks=50.0,
            passing_marks=20.0,
            negative_marks_per_q=0.25,
            is_active=True,
            created_by_id=admin.id
        )
        db.session.add(exam1)

        # 4. Create Exam 2: CSE2500
        exam2 = Exam(
            title="Data Analytics Fundamentals & Statistical Methods",
            course_code="CSE2500",
            description="End-term evaluation on exploratory data analysis, regression, clustering models, and statistical significance testing.",
            duration_minutes=60,
            total_marks=30.0,
            passing_marks=12.0,
            negative_marks_per_q=0.25,
            is_active=True,
            created_by_id=admin.id
        )
        db.session.add(exam2)

        # 5. Create Exam 3: CSE2102
        exam3 = Exam(
            title="Object Oriented Programming in Java",
            course_code="CSE2102",
            description="Fundamentals of Java, object-oriented design, inheritance, polymorphism, abstract classes, and exception handling.",
            duration_minutes=30,
            total_marks=20.0,
            passing_marks=8.0,
            negative_marks_per_q=0.0,
            is_active=True,
            created_by_id=admin.id
        )
        db.session.add(exam3)
        db.session.commit()
        print("Created 3 Course Examinations.")

        # 6. Populate Questions for Exam 1 (CSE2271 - 25 Questions)
        cse2271_questions = [
            (
                "Which UML diagram is primarily utilized to illustrate the dynamic sequence of activities and decision branches across parallel swimlanes?",
                "Class Diagram", "Activity Diagram", "Deployment Diagram", "Entity-Relationship Diagram",
                "B", 2.0, "Activity diagrams model behavioral workflows, control flows, concurrent forks, and decision logic.", "Easy"
            ),
            (
                "In a UML Use Case diagram, which relationship denotes that a base use case unconditionally executes the behavior of another subordinate use case?",
                "<<extend>>", "<<include>>", "<<generalization>>", "<<association>>",
                "B", 2.0, "<<include>> signifies mandatory execution where the base case requires the included case to complete.", "Medium"
            ),
            (
                "Which data structure is primarily utilized to implement Breadth First Search (BFS) in an unweighted graph to guarantee shortest-distance discovery?",
                "Stack", "Queue", "Priority Queue", "Binary Search Tree",
                "B", 2.0, "BFS visits vertices level by level, requiring the First-In First-Out (FIFO) property of a Queue.", "Medium"
            ),
            (
                "What is the worst-case time complexity of QuickSort when using a naive pivot selection on an already sorted or reverse-sorted array?",
                "O(n log n)", "O(n²)", "O(n)", "O(log n)",
                "B", 2.0, "When partitions are maximally unbalanced (0 and n-1), recurrence T(n) = T(n-1) + O(n) yields O(n²).", "Medium"
            ),
            (
                "Which ACID transaction property guarantees that committed transactions survive power outages, crashes, and hardware failures?",
                "Atomicity", "Consistency", "Isolation", "Durability",
                "D", 2.0, "Durability ensures that once a transaction commits, its effects are permanently recorded in non-volatile storage.", "Easy"
            ),
            (
                "Which design pattern restricts the instantiation of a class to one single object and provides a global point of access to it?",
                "Factory Pattern", "Observer Pattern", "Singleton Pattern", "Decorator Pattern",
                "C", 2.0, "The Singleton pattern ensures only one instance exists throughout the application lifecycle.", "Easy"
            ),
            (
                "In RESTful API design, which HTTP method is canonically utilized to submit data to create a new resource on the server?",
                "GET", "POST", "PUT", "DELETE",
                "B", 2.0, "POST is standard for submitting subordinate entities to trigger creation of a new resource.", "Easy"
            ),
            (
                "Which HTTP response status code signifies that the client request requires authentication credentials that were omitted or invalid?",
                "200 OK", "301 Moved Permanently", "401 Unauthorized", "500 Internal Server Error",
                "C", 2.0, "401 indicates lack of valid authentication credentials for the requested target resource.", "Easy"
            ),
            (
                "In an online proctored examination, which HTML5 JavaScript event is utilized to detect when a candidate navigates away from the exam tab?",
                "onbeforeunload", "visibilitychange", "onresize", "oncontextmenu",
                "B", 2.0, "document.addEventListener('visibilitychange') detects when the document becomes hidden or inactive.", "Medium"
            ),
            (
                "What is the minimum number of queues required to implement a First-In-First-Out (FIFO) queue using only Last-In-First-Out (LIFO) Stacks?",
                "1 Stack", "2 Stacks", "3 Stacks", "4 Stacks",
                "B", 2.0, "Two stacks (an input stack and an output stack) are required to simulate a FIFO Queue.", "Medium"
            ),
            (
                "In relational database modeling, what integrity rule enforces that a foreign key value must always match a primary key value in the referenced table?",
                "Entity Integrity", "Referential Integrity", "Domain Integrity", "User-Defined Integrity",
                "B", 2.0, "Referential integrity ensures relationships between tables remain consistent and foreign keys remain valid.", "Easy"
            ),
            (
                "Which asymptotic notation represents the tightest formal upper bound on the growth rate of an algorithm's execution time?",
                "Big-Omega (Ω)", "Big-O (O)", "Big-Theta (Θ)", "Little-omega (ω)",
                "B", 2.0, "Big-O notation describes the asymptotic mathematical upper bound for function growth.", "Easy"
            ),
            (
                "Which sorting algorithm has a guaranteed worst-case time complexity of O(n log n) and sorts strictly in-place with O(1) auxiliary space?",
                "MergeSort", "HeapSort", "BubbleSort", "CountingSort",
                "B", 2.0, "HeapSort guarantees O(n log n) in all cases while operating in-place with O(1) extra auxiliary memory.", "Hard"
            ),
            (
                "In an operating system, which condition is NOT one of Coffman's four necessary conditions for a deadlock to occur?",
                "Mutual Exclusion", "Hold and Wait", "Preemption Allowed", "Circular Wait",
                "C", 2.0, "No preemption is the necessary condition. If preemption is allowed, deadlocks cannot occur.", "Medium"
            ),
            (
                "Which cryptographic mechanism provides non-repudiation and guarantees the origin and integrity of a digital payload?",
                "Symmetric Encryption", "Digital Signature", "Base64 Encoding", "CRC32 Checksum",
                "B", 2.0, "Digital signatures utilize asymmetric private keys to ensure non-repudiation and integrity.", "Medium"
            ),
            (
                "What is the primary purpose of salt in password hashing mechanisms such as bcrypt or Argon2?",
                "To compress the password length", "To defend against precomputed rainbow table attacks", "To make encryption reversible", "To validate email domain",
                "B", 2.0, "Salt introduces unique pseudo-random bits to every password hash, invalidating precomputed rainbow tables.", "Medium"
            ),
            (
                "Which transport layer protocol provides connection-oriented, reliable, ordered, and error-checked delivery of byte streams?",
                "UDP", "TCP", "ICMP", "ARP",
                "B", 2.0, "Transmission Control Protocol (TCP) provides guaranteed, reliable, sequence-controlled byte delivery.", "Easy"
            ),
            (
                "In software engineering, what metric measures the degree of interdependence and coupling between distinct software modules?",
                "Cohesion", "Coupling", "Polymorphism", "Encapsulation",
                "B", 2.0, "Coupling measures module interdependence; software systems should strive for loose coupling and high cohesion.", "Easy"
            ),
            (
                "In binary search trees (BST), which tree traversal order visits vertices in strictly ascending non-decreasing key sequence?",
                "Pre-order (Root-Left-Right)", "In-order (Left-Root-Right)", "Post-order (Left-Right-Root)", "Level-order (BFS)",
                "B", 2.0, "In-order traversal of a valid BST always yields elements in sorted ascending sequence.", "Easy"
            ),
            (
                "What is the average and worst-case time complexity for looking up an element in an open-addressed hash table with a uniform hash function?",
                "Average O(1), Worst O(n)", "Average O(log n), Worst O(n)", "Average O(1), Worst O(log n)", "Average O(n), Worst O(n²)",
                "A", 2.0, "Hashing achieves O(1) expected constant lookup, degrading to O(n) in worst-case full collision clustering.", "Medium"
            ),
            (
                "In software testing, what type of testing evaluates whether changes or bug fixes have introduced new unintended regressions into existing features?",
                "Unit Testing", "Regression Testing", "Stress Testing", "Usability Testing",
                "B", 2.0, "Regression testing re-executes tests to confirm code modifications did not break existing functionality.", "Easy"
            ),
            (
                "Which normalization form eliminates transitive dependencies between non-prime attributes and the candidate key?",
                "1NF", "2NF", "3NF", "BCNF",
                "C", 2.0, "Third Normal Form (3NF) requires 2NF plus the absence of transitive dependencies on primary keys.", "Medium"
            ),
            (
                "Which graph algorithm solves the single-source shortest path problem on weighted graphs with non-negative edge weights in O((V + E) log V) time?",
                "Bellman-Ford Algorithm", "Dijkstra's Algorithm", "Floyd-Warshall Algorithm", "Kruskal's Algorithm",
                "B", 2.0, "Dijkstra's algorithm efficiently computes shortest paths on non-negative weighted graphs using a min-heap priority queue.", "Medium"
            ),
            (
                "In web security, what vulnerability occurs when an application includes untrusted user input in a dynamic web page without proper escaping?",
                "SQL Injection (SQLi)", "Cross-Site Scripting (XSS)", "Cross-Site Request Forgery (CSRF)", "Buffer Overflow",
                "B", 2.0, "XSS enables malicious attackers to inject client-side executable scripts into web pages viewed by other users.", "Medium"
            ),
            (
                "Which architectural principle states that software components should be open for extension but closed for modification?",
                "Single Responsibility Principle", "Open/Closed Principle", "Liskov Substitution Principle", "Interface Segregation Principle",
                "B", 2.0, "The Open/Closed Principle (O in SOLID) encourages polymorphic abstraction so new behavior can be added without altering tested code.", "Medium"
            )
        ]

        for q_tuple in cse2271_questions:
            q = Question(
                exam_id=exam1.id,
                question_text=q_tuple[0],
                option_a=q_tuple[1],
                option_b=q_tuple[2],
                option_c=q_tuple[3],
                option_d=q_tuple[4],
                correct_option=q_tuple[5],
                marks=q_tuple[6],
                explanation=q_tuple[7],
                difficulty=q_tuple[8]
            )
            db.session.add(q)

        # 7. Add sample questions for Exam 3 (CSE2102 Java)
        cse2102_questions = [
            ("Which keyword in Java is used to inherit a class?", "implement", "extends", "inherits", "instanceof", "B", 2.0, "The extends keyword is used to establish subclass inheritance.", "Easy"),
            ("Which access modifier makes a class member visible only within its own class?", "public", "protected", "private", "default", "C", 2.0, "Private members are encapsulated and accessible only within the declaring class.", "Easy"),
            ("Can an abstract class in Java have constructors?", "No, constructors are strictly forbidden", "Yes, abstract classes can define constructors", "Only if all methods are static", "Only if it implements Serializable", "B", 2.0, "Abstract classes have constructors invoked during concrete subclass instantiation via super().", "Medium"),
            ("Which interface must be implemented to allow instances of a class to be executed by a thread?", "Callable", "Runnable", "Processable", "Threadable", "B", 2.0, "java.lang.Runnable defines the single run() method for thread execution.", "Easy"),
            ("What exception is thrown when an application attempts to use null in an object reference case?", "ArithmeticException", "NullPointerException", "ArrayIndexOutOfBoundsException", "ClassCastException", "B", 2.0, "NullPointerException is raised when dereferencing a null reference.", "Easy"),
            ("Which collection class in Java provides constant-time performance for basic operations (add, remove, contains)?", "TreeSet", "HashSet", "LinkedList", "Vector", "B", 2.0, "HashSet provides O(1) expected time for core set operations using hashing.", "Medium"),
            ("What does the 'final' keyword on a variable in Java indicate?", "The variable cannot be accessed outside the class", "The variable's value cannot be modified once initialized", "The variable is stored on the heap", "The variable is synchronized", "B", 2.0, "A final variable is a constant that cannot be reassigned once bound.", "Easy"),
            ("Which of the following is NOT a primitive data type in Java?", "boolean", "int", "String", "double", "C", 2.0, "String is an immutable reference class, not a primitive type.", "Easy"),
            ("What happens during garbage collection in Java?", "Unreferenced objects on the heap are reclaimed to free memory", "Classes are recompiled into native assembly", "Threads are paused indefinitely", "Disk cache is flushed", "A", 2.0, "The JVM Garbage Collector detects unreachable objects and reclaims their heap memory.", "Easy"),
            ("Which method in Object class is invoked immediately before an object is garbage-collected?", "dispose()", "finalize()", "destroy()", "clean()", "B", 2.0, "finalize() is historically invoked by garbage collection prior to memory reclamation.", "Medium")
        ]

        for q_tuple in cse2102_questions:
            q = Question(
                exam_id=exam3.id,
                question_text=q_tuple[0],
                option_a=q_tuple[1],
                option_b=q_tuple[2],
                option_c=q_tuple[3],
                option_d=q_tuple[4],
                correct_option=q_tuple[5],
                marks=q_tuple[6],
                explanation=q_tuple[7],
                difficulty=q_tuple[8]
            )
            db.session.add(q)

        db.session.commit()
        print("Populated all exam questions.")

        # 8. Create completed result for student1 on CSE2102 for immediate live demo
        completed_res = ExamResult(
            user_id=student1.id,
            exam_id=exam3.id,
            score=18.0,
            max_score=20.0,
            percentage=90.0,
            passed=True,
            total_questions=10,
            correct_count=9,
            incorrect_count=1,
            unanswered_count=0,
            time_taken_seconds=18 * 60 + 24,
            strike_count=0,
            submitted_at=datetime.now(timezone.utc)
        )
        db.session.add(completed_res)
        db.session.commit()

        # Add answer records for this completed result
        e3_qs = Question.query.filter_by(exam_id=exam3.id).all()
        for idx, q in enumerate(e3_qs):
            # Q3 will be wrong for realistic demo
            is_correct = (idx != 2)
            sel = q.correct_option if is_correct else ('A' if q.correct_option != 'A' else 'B')
            ans = StudentAnswer(
                result_id=completed_res.id,
                question_id=q.id,
                selected_option=sel,
                is_correct=is_correct,
                marks_awarded=2.0 if is_correct else 0.0
            )
            db.session.add(ans)

        db.session.commit()
        print(f"Created sample completed result for Student {student1.roll_no} (Score: 18/20).")
        print("\n=== SEEDING COMPLETED SUCCESSFULLY! ===")
        print("Default Credentials:")
        print("Admin:   admin@presidency.edu / Admin@123")
        print("Student: student@presidency.edu (or 20241CSE0750) / Student@123")
        print("Student: eknath@presidency.edu (or 20241CSE0752) / Student@123")

if __name__ == '__main__':
    seed_database()

