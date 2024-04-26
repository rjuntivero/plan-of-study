from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey, Table, insert
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

association_table = Table('prerequisite_association', Base.metadata,
    Column('course_id', String, ForeignKey('Course.class_id'), primary_key=True),
    Column('prerequisite_id', String, ForeignKey('Course.class_id'), primary_key=True)
)


class Course(Base):
    __tablename__ = 'Course'
    class_id = Column(String, primary_key = True) 
    cname = Column(String, nullable = False)
    fall = Column(Boolean)
    spring = Column(Boolean)
    summer = Column(Boolean)
    comp_sci = Column(Boolean)
    data_sci = Column(Boolean)
    info_sci = Column(Boolean)
    info_tech = Column(Boolean)
    info_sys = Column(Boolean)
    communication = Column(Boolean)
    humanities = Column(Boolean)
    social_sci = Column(Boolean)
    math_stats = Column(Boolean)
    science = Column(Boolean)
    completed = Column(Boolean, nullable = False)
    credit_hrs = Column(Integer, nullable = False)
    description = Column(Text)
    prerequisites = relationship('Course', secondary=association_table,
                                 primaryjoin=class_id == association_table.c.course_id,
                                 secondaryjoin=class_id == association_table.c.prerequisite_id,
                                 backref='prerequisite_of')

    def __repr__(self):
        return f"Course: {self.class_id} Course Name: {self.cname}"
    


Base.metadata.create_all(engine)
session = Session()

course_details = [
    #School of Computing Courses
    {'class_id': 'COP 2220', 'cname': 'Programming I', 'fall': True, 'spring': True, 'summer': True,'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course provides an introduction to problem solving techniques and the computer programming process. Topics in the course include data types, operations, expressions, flow control, I/O, functions, program structure, software design techniques, and memory allocation. Course concepts are reinforced with many programming projects throughout the course.'},
    
    {'class_id': 'COT 3100', 'cname': 'Computational Structures', 'fall': 1, 'spring': 1, 'summer': 1, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course will cover the mathematical and logical fundamentals required in computer science, information systems, information science, and information technology. The course develops concepts in discrete mathematical structures as applied to computing in general through the topics of sets; logic; proof techniques; Boolean algebra; algorithms and problem solving; number systems; number theory; counting and discrete probability; and relations and graphs.'},
    
    {'class_id': 'CIS 3253', 'cname': 'Legal and Ethical Issues in Computing', 'fall': 1, 'spring': 1, 'summer': 1, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course provides an opportunity to discuss and analyze the legal and ethical issues facing today’s computing professionals, as well as the legal and ethical issues computing professionals may face in the future. Legal and ethical issues are considered from local, as well as global perspectives.'},
    
    {'class_id': 'COP 3503', 'cname': 'Programming II', 'fall': 1, 'spring': 1, 'summer': 1, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course serves as a continuation to the Programming I course. Students are shown additional fundamental concepts of problem solving using the object-oriented paradigm and data structures. The topics in this course include classes, interfaces, objects, class types, events, exceptions, control structures, polymorphism, inheritance, linked lists, arrays, stacks, queues, and deques. Students are expected to apply these concepts through the construction of numerous small software systems using both integrated development environments and command-line- driven tools that support editing, testing, and debugging.'},
    
    {'class_id': 'CDA 3100', 'cname': 'Computer Organization and Architecture', 'fall': 0, 'spring': 1, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'completed': False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'credit_hrs': 4, 'description': 'This course will cover the fundamental ideas in computer architecture and organization. Topics include machine-level data representation; digital logic; computer arithmetic; processor design; system components and inter-communication; memory hierarchy; multi-core processors; GPU; and modern technological advancements.'},
    
    {'class_id': 'COT 3210', 'cname': 'Theory of Computation', 'fall': 1, 'spring': 0, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'completed': False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'credit_hrs': 3, 'description': 'This course will cover the theory of computation using formal methods for describing and analyzing programming languages and algorithms. Topics include finite automata and regular expressions; formal languages and syntactic analysis; pushdown automata and Turing machines; and computational complexity.'},
    
    {'class_id': 'COP 3530', 'cname': 'Data Structures', 'fall': 1, 'spring': 1, 'summer': 1, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Students in this course will study various data structures including binary trees, balanced trees, B-trees, hashing, and heaps. Additional topics include advanced data structures such as splay trees, tree representations, graphs, dynamic memory, and algorithms for sorting and searching. Students are expected to complete projects using object-oriented programming.'},
    
    {'class_id': 'CNT 4504', 'cname': 'Computer Networks', 'fall': 1, 'spring': 1, 'summer': 1, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'In this course, students will study architectures, protocols, and layers in computer networks and develop client-server applications. Topics include the OSI and TCP/IP models, transmission fundamentals, flow and error control, switching and routing, network and transport layer protocols, local and wide-area networks, wireless networks, client-server models, and network security. Students will extend course topics via programming assignments, library assignments and other requirements.'},
    
    {'class_id': 'COP 3703', 'cname': 'Introduction to Databases', 'fall': 1, 'spring': 1, 'summer': 1, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course covers database modeling with emphasis on the relational data model. Principles of relational database design, normal forms, constraints, and SQL programming will be discussed extensively. Additionally, topics related to indexing, views, transactions, XML and No-SQL databases will also be discussed. The course will cover aspects of information security and assurance as they relate to data management. Concepts covered in the course will be reinforced through the use of open source and/or commercial database management systems.'},
    
    {'class_id': 'COP 3404', 'cname': 'Systems Programming', 'fall': 1, 'spring': 0, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Students will learn the design and role of systems software including assemblers, loaders and linkers; assembly programming; system libraries; utility programs; concurrent programming including threads, semaphores, and synchronization; event-driven programming; memory management; and machine-dependent code optimization techniques.'},
    
    {'class_id': 'COP 4620', 'cname': 'Construction of Language Translators', 'fall': 0, 'spring': 1, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course introduces students to the theoretical foundations and practical issues of designing language translators. Students will learn how to use compiler construction tools such as generators of scanners and parsers. Grammars, parsing, lexical analysis, syntax analysis, code generation, and optimization will also be discussed.'},
    
    {'class_id': 'CEN 4010', 'cname': 'Software Engineering', 'fall': 0, 'spring': 1, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : True, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course introduces students to fundamental Software Engineering concepts and current practices. Topics covered include: software process models; agile software development; requirements engineering; domain modeling; model-driven development; software architectures; design paradigms and patterns; project management, tracking, and release planning; collaborative development, testing, deployment, maintenance and evolution.'},
    
    {'class_id': 'COT 4400', 'cname': 'Design and Analysis of Algorithms', 'fall': 1, 'spring': 0, 'summer': 0, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course will introduce fundamental techniques for designing and analyzing algorithms, including asymptotic analysis; divide-and-conquer algorithms and recurrences; greedy algorithms; dynamic programming; and graph algorithms.'},
    
    {'class_id': 'CAP 4630', 'cname': 'Introduction to Artificial Intelligence', 'fall': 0, 'spring': 1, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Course topics include heuristic techniques for problem-solving and decision making, control and search strategies, knowledge representation, logic, AI languages, and tools. Applications such as machine learning, natural language understanding, planning, and robotics will be included.'},
    
    {'class_id': 'COP 4610', 'cname': 'Operating Systems', 'fall': 0, 'spring': 1, 'summer': 0, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Topics in this course include process management, memory management, file management, and I/O device management.'},
    
    {'class_id': 'COP 3855', 'cname': 'Web Systems Development', 'fall': False, 'spring': True, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 4, 'description': 'Students learn about the influence of local and global transaction processing, Internet, Web design and development, and Electronic Data Interchange on information systems. This course discusses the concepts and skills required to design and implement Web application systems using Model-view-controller (MVC) architecture. Students learn about how Web applications are developed using client-side and server-side scripting to implement internal and external business processes. After an introduction to the basic concepts of relational database systems and Object Relational Mapping (ORM) students will practice for storing and accessing data in the database.'},
    
    {'class_id': 'COP 4813', 'cname': 'Internet Programming', 'fall': True, 'spring': False, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': ' In this course students will use current technologies to develop Internet and web-based applications. The topics to be covered include client and server-side components for the WWW to facilitate client-server communication, web services, and an introduction to source control tools. Students will extend course topics via programming assignments, library assignments and other assigned activities.'},
     
    {'class_id': 'CDA 4010', 'cname': 'User Interface Design', 'fall': True, 'spring': False, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course introduces the fundamentals of effective interaction between humans and computers with an emphasis on software and physical elements. Good and bad interface designs are examined to reinforce proven interface design techniques. The phases and tools involved in the interaction design process are discussed, as well as how the interaction design process aligns with the Software Development Life Cycle (SDLC).'},
    
    {'class_id': 'CIS 4327', 'cname': 'Information Systems Senior Project I', 'fall': True, 'spring': False, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'First of a two-course senior project on systems development with a significant laboratory component. Students will learn system development life cycle methodologies and its phases including requirements specification, analysis, and design. Students will design and develop a prototype information system in the context of the project team environment.'},

    {'class_id': 'CAP 4784', 'cname': 'Introduction to Data Analytics', 'fall': False, 'spring': True, 'summer': False,'comp_sci' : False, 'data_sci' : True, 'info_sci' : True, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course gives a broad overview of the various aspects of data analytics and visualizations. Students will learn ways of accessing data from various sources such as web APIs and repositories, techniques of cleaning data and organizing data for analysis, using analytical methods to solve real-world problems, and create visualizations to aid the interpretation of analysis results. Students will have hands on training using relevant programming languages, as well as analytics and visualization tools. Over the course of the semester, students will apply lessons learned and use tools trained to work on exploratory and descriptive data science projects.'},

    {'class_id': 'CIS 4328', 'cname': 'Information Systems Senior Project II', 'fall': False, 'spring': True, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'The second of a two-course senior project on systems development with a significant laboratory component. Students will design, implement, and deploy a prototype information system in the context of a project team environment employing relevant systems development life cycle methodologies.'},
    
    {'class_id': 'CGS 1100', 'cname': 'Computer Applications for Business', 'fall': True, 'spring': True, 'summer': True,'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course provides an introduction to the fundamentals of personal computing for business majors and other non-computer science majors. Topics include the Windows operating system, word processing, spreadsheets, database, presentation aids, internet, e-mail and related areas. Students may not receive credit for CGS1100 and also for CGS1570.'},
    
    {'class_id': 'CIS 4360', 'cname': 'Introduction to Computer Security', 'fall': False, 'spring': True, 'summer': False ,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course presents basic concepts and principles of information security, and the fundamental approaches to secure computers and networks. Main topics include security basics, security management, risk assessment, software security, cryptography algorithms and protocols, and network authentication.'},
    
    {'class_id': 'CIS 3526', 'cname': 'IT Project Management', 'fall': True, 'spring': True, 'summer': True,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'completed': False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'credit_hrs': 3, 'description': 'This course introduces todays best practices in information technology project management. Students are challenged to incrementally create mock project plans and change requests to demonstrate comprehension of scope, time, cost, quality, human resources, communications, risk, procurement and stakeholder management techniques to successfully execute projects. Projects are a group assignment so students leverage their combined interests and knowledge in computer science, information science, information systems, and information technology to imagineer their projects. Formation of project change requests will require creative and analytical thinking to resolve challenges unique to the design, implementation, configuration and maintenance of IT infrastructures and/or software programs. Students who pass this course are eligible to pursue the Associate of Project Management certification (CAPM), an internationally recognized credential in the project management field.'},

    {'class_id': 'COP 4640', 'cname': 'Operating Systems Environments', 'fall': True, 'spring': False, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'An introduction to operating systems from theoretical and applied points of view. Topics include operating system configuration, characteristics, and evaluation. The course will explore operating system theory and development using case studies of common operating systems. Students will complete laboratory assignments using the Linux operating system.'},

    {'class_id': 'CIS 4325', 'cname': 'Introduction to Systems Administration', 'fall': False, 'spring': True, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Responsibilities of a Systems Administrator in the world of IT. Topics covered will include: desktop management, servers, services; processes; file systems; user management; backups; disaster recovery; logging; networking; DNS; NFS; email; security; web hosting; software installation, maintenance, and upgrades; printing; performance analysis; policies; and ethics.'},

    {'class_id': 'CNT 4406', 'cname': 'Network Security and Management', 'fall': False, 'spring': True, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'In this course, students will identify and analyze user needs and take them into account in the selection, creation, integration, evaluation, and administration of secure computer systems. The course would focus on issues related to the management and security of various network topologies. The use of cryptographic algorithms in the design and implementation of network security protocols will be covered. Various forms of security attacks will be detected, analyzed, and mitigated.'},

    {'class_id': 'CEN 4083', 'cname': 'Introduction to Cloud Computing', 'fall': False, 'spring': True, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'The adoption of cloud computing services continues to grow across a variety of organizations and in many domains. Students will be exposed to the current practices in cloud computing. Topics may include cloud service models such as Infrastructure as a Service (IaaS), Platform as a Service (PaaS), Software as a Service (SaaS), virtualization, cloud architectures, motivating factors, benefits and challenges of the cloud, cloud storage, performance and systems issues, disaster recovery, federated clouds, hypervisor CPU and memory management, data centers, and cloud security. Course work may include homework assignments, presentations, and projects that will provide exposure to major cloud services such as Amazon Web Services (AWS) and/or Google Compute Engine (GCE).'},

    {'class_id': 'CIS 4364', 'cname': 'Intrusion Detection', 'fall': True, 'spring': False, 'summer': False,'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course explores the use of intrusion detection systems (IDS) as part of an organization''s overall security posture. A variety of approaches, models, and algorithms along with the practical concerns of deploying IDS in an enterprise environment will be discussed. Topics include the history of IDS, anomaly and misuse detection for both host and network environments, policy and legal issues surrounding the use of IDS, how IDS can complement host and network security, and current research topics.'},
    
    {'class_id': 'CIS 4366', 'cname': 'Computer Forensics', 'fall': True, 'spring': False, 'summer': False, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : True, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Topics in this course will include computer system data recovery with a particular emphasis on computer evidence handling and computer crime detection. The students will use and develop computer software tools to reboot suspect computers, detect evidence of computer crime, and preserve that evidence for later use. Students will be trained to recover data from simulated crime environments.'},

    {'class_id': 'CAP 4770', 'cname': 'Data Mining', 'fall': True, 'spring': False, 'summer': False, 'comp_sci' : False, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course covers methods and systems for mining varied data and discovering knowledge from data. The course will expose students to concepts and techniques of data mining, including characterization and comparison, association rules mining, classification and prediction, and mining complex types of data. Students will also examine applications and trends in data mining.'},

    {'class_id': 'ISM 4011', 'cname': 'Introduction to Management Information Systems', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course will cover the fundamentals of management information systems with an emphasis on the relationships of MIS and data processing to decision-making in modern organizations.'},

    {'class_id': 'MAN 3025', 'cname': 'Principles of Management', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course covers fundamentals of management which permeate organizations; including introductory studies of administrative structure, the organizational environment, and managerial functions and processes.'},

    {'class_id': 'FIN 3403', 'cname': 'Financial Management', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course focuses on management techniques for and considerations in determining short-term, intermediate-term, and long-term financial needs. Sources of funds available to management and the relevant financial instruments will be examined.'},

    {'class_id': 'ECO 2013', 'cname': 'Principles of Macroeconomics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': True, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Introduction to the theory of income determination and national income accounting. Analysis of the use of monetary and fiscal policy to accomplish the goals of full employment, economic growth and price stability. Cannot be used to satisfy upper-level requirements for a degree in business administration and economics. Normally offered each term.'},

    {'class_id': 'ECO 2032', 'cname': 'Intermediate Macroeconomics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course analyzes aggregate economic activity and growth, focusing on national economic goals and policies for their attainment.'},

    {'class_id': 'ACG 2021', 'cname': 'Principles of Financial Accounting', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course is a conceptual introduction to financial accounting. In this course, primary emphasis is placed on income measurement and the interpretation of conventional financial statements.'},
    
    {'class_id': 'ACG 2071', 'cname': 'Principles of Managerial Accounting', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course is the conceptual introduction to managerial accounting. The material covers accounting for cost reporting and control, reports, statements, and analytical tools used by management.'},

    {'class_id': 'MAC 2233', 'cname': 'Calculus for Business', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'Topics in differential and integral calculus with applications.'},

    {'class_id': 'STA 2023', 'cname': 'Elementary Statistics for Business', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : True, 'info_tech' : True, 'info_sys' : True, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'his course is an introduction to descriptive data analysis, probability, statistical distributions, confidence intervals, testing of hypotheses, regression, and correlation. Topics selected to emphasize applications in a business environment.'},

    {'class_id': 'MAC 2311', 'cname': 'Calculus I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed': False, 'credit_hrs': 4, 'description': 'This course examines the notions of limit, continuity and derivatives of functions of one variable. The course explores differentiation rules for algebraic, trigonometric, exponential and logarithmic functions. The course discusses applications of differential calculus, such as related rates problems, curve sketching, and optimization. The course also introduces students to definite and indefinite integrals and the Fundamental Theorem of Calculus.'},

    {'class_id': 'MAC 2312', 'cname': 'Calculus II', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed': False, 'credit_hrs': 4, 'description': 'This course continues the study of definite and indefinite integrals, and the Fundamental Theorem of Calculus begun in MAC 2311. The course presents various integration techniques and their applications, convergence of sequences and series, as well as power series and Taylor series of a function of one variable.'},

    {'class_id': 'PHY 2048C', 'cname': 'Calculus-based Physics I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed': False, 'credit_hrs': 4, 'description': ''},

    {'class_id': 'PHY 2049', 'cname': 'Calculus-based Physics II', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed': False, 'credit_hrs': 3, 'description': 'his course is a continuation of PHY 2048 or PHY 2048C with emphasis on electricity, magnetism and light. This course will be three hours of lecture.'},

    {'class_id': 'PHY 2049L', 'cname': 'Calculus-based Physics II Lab', 'fall': True, 'spring': True, 'summer': False, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed': False, 'credit_hrs': 1, 'description': 'This course is the laboratory course that accompanies the PHY 2049 or PHY 2042 courses. This course will be three hours of laboratory.'},
    
    {'class_id': 'STA 3032', 'cname': 'Probability and Statistics for Engineers', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : True, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This course is a survey of the basic concepts in probability and statistics with applications in electrical, mechanical, and civil engineering. Topics include probability, common discrete and continuous probability distributions, estimation and hypothesis testing, and simple regression.'},

    {'class_id': 'MAS 3105', 'cname': 'Linear Algebra', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : True, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 4, 'description': 'This course covers matrix algebra, Gaussian elimination, determinants, Euclidean spaces, linear transformations, eigenvalues, eigenvectors, and vector spaces.'},

    {'class_id': 'STA 4321', 'cname': 'Probability and Statistics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 4, 'description': 'This course will cover basic probability principles, random variables and univariate probability distributions, moments and an introduction to moment generating functions, introduction to sampling distributions and the Central Limit Theorem, and introduction to interval estimation and hypothesis testing.'},

    {'class_id': 'STA 3163', 'cname': 'Statistical Methods I', 'fall': True, 'spring': False, 'summer': False, 'comp_sci' : False, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 4, 'description': 'This is the first in a two-term sequence in applied statistical methods. This course focuses on descriptive and inferential statistics for means and proportions in one and two groups, simple linear regression with its diagnostics, and the one-way analysis of variance. The course incorporates technology and uses SAS for analysis of statistical data.'},

    {'class_id': 'STA 3164', 'cname': 'Statistical Methods II', 'fall': False, 'spring': True, 'summer': False, 'comp_sci' : False, 'data_sci' : True, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed': False, 'credit_hrs': 3, 'description': 'This is the second in a two-term sequence in applied statistical methods. In this course, the focus is on more complex data models such as multiple regression, the higher-order analysis of variance, and logistic regression. Data analysis is carried out using the SAS program.'}, 

    #--------------------------------------------------------------------------------------------General education classes
    #Part A of General Education Requirements
    #Communications Group 1
    {'class_id' : 'ENC 1101', 'cname' : '(GW) Writing for Audeience and Purpose', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Humanties Group 2   
    {'class_id' : 'ARH 2000', 'cname' : 'Art Appreciation', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'LIT 2000', 'cname' : '(GW) Introduction to Literature', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MUL 2010', 'cname' : '(GW) Introduction to Music Literature', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHI 2010', 'cname' : '(GW) Introduction to Philosophy', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'THE 2000', 'cname' : 'Theater Appreciation', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Social Sciences Group 3
    {'class_id' : 'AMH 2020', 'cname' : 'United States History Since 1877', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': True, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ANT 2000', 'cname' : 'Introduciton to Anthropology', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': True, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'POS 2041', 'cname' : 'Introduction to American Government', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': True, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PSY 2012', 'cname' : 'Introduction to Psychology', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': True, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'SYG 2000', 'cname' : 'Introduction to Sociology', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': True, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Mathematics and Stastics Group 4
    {'class_id' : 'MAC 1105', 'cname' : 'College Algebra', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MGF 1106', 'cname' : 'Finite Mathematics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MGF 1107', 'cname' : 'Explorations of Mathematics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'STA 2014', 'cname' : 'Elementary Statistics for Health and Social Sciences', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Natural and Physical Sciences Group 5
    {'class_id' : 'AST 2002', 'cname' : 'Discovering Astronomy', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'BSC 1005', 'cname' : 'Principles of Biology', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'BSC 1010C', 'cname' : 'General Biology I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'BSC 2085C', 'cname' : 'Human Anatomy and Physiology', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'CHM 1020', 'cname' : 'Discovering Chemistry', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'CHM 2045', 'cname' : 'General Chemistry I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ESC 2000', 'cname' : 'Earth Science', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'EVR X001', 'cname' : 'Introduction to Environmental Science', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHY 1020', 'cname' : 'Discovering Physics: How things work', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHY 2053', 'cname' : 'Algebra-Based Physics I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Part B of General Education Requirements
    #Writing Effectively (6 Hours)
    {'class_id' : 'ENC 1143', 'cname' : '(GW) Writing with Evidence and Style', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'IDS 1932', 'cname' : '(GW) Interdisciplinary First Year Writing', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ENC 3202', 'cname' : '(GW) Professional Communications for Business', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ENC 3246', 'cname' : '(GW) Professional Communications for Engineering', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ENC 3250', 'cname' : '(GW) Professional Communications', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': True, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Thinking Critically --------------------------------------here down checked
    {'class_id' : 'AFH 3450', 'cname' : 'South Africa',  'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'AMH 3571', 'cname' : 'Introduction to African-American History', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'AMH 3580', 'cname' : 'American Indian History', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ANT 2423', 'cname' : 'Kinship and Family', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ANT 3212', 'cname' : 'Peoples & Cultures of the World', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ANT 3312', 'cname' : 'North American Indians', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ARH 2050', 'cname' : 'Art History Survey I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ARH 2051', 'cname' : 'Art History Survey II', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ASH 3223', 'cname' : 'Middle East', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ASH 3440', 'cname' : 'Japanese Civilization', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ASN 2003', 'cname' : 'Introduction to Asia', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'CCJ 2002', 'cname' : 'Crime in America', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ECO 3701', 'cname' : 'Contemporary International Economic', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'EDF 2085', 'cname' : 'Introduction to Diversity for Educators', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'EEX 3005', 'cname' : 'Introduction to Disabilities', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'ENG 3613', 'cname' : 'Topics in Disability Studies', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'EUH 3580', 'cname' : 'Russian Thought & Culture', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'FIL 2000', 'cname' : 'Film Appreciation', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'FIL 4848', 'cname' : 'World Cinema Across Cultures', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'GEO 2420', 'cname' : 'Cultural Geograph', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'HSC 2100', 'cname' : 'Personal and Community Health', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'LAH 3300', 'cname' : 'Latin America', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'LDR 3003', 'cname' : 'Introduction to Leadership', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MMC 2701', 'cname' : 'Communicating Across Cultures', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MUH 2012', 'cname' : 'Enjoyment of Music', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MUH 2017', 'cname' : 'The History and Appreciation of Rock', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MUH 2018', 'cname' : 'Evolution of Jazz', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MUT 1011', 'cname' : 'Music Fundamentals', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MUT 1111', 'cname' : 'Theory I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHI 2100', 'cname' : '(GW) Art of Reasoning', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHI 2630', 'cname' : '(GW) Ethical Issues', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PUP 2312', 'cname' : 'Race, Gender & Politics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'REL 2300', 'cname' : 'Comparative Religion', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'REL 3102 ', 'cname' : 'Religion as Culture', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'SOP 3742', 'cname' : 'Psychology of Women', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'SYD 3700', 'cname' : 'Racial and Ethnic Minorities', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'SYD 3800', 'cname' : 'Gender and Society', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'SYG 2013', 'cname' : 'Sex, Race and Class', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'WOH 1012', 'cname' : '(GW) World History I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'WOH 1022', 'cname' : '(GW) World History II', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : True, 'social_sci': False, 'math_stats' : False, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    #Reasoning and Analyzing Quantitatively and/or Understanding the Scientific Method (4-6 Hours) 
    {'class_id' : 'MGF 1113', 'cname' : 'Math for Teachers I', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MAC 1101', 'cname' : 'Intensive College Algebra', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MAC 1101C', 'cname' : 'Intensive College Algebra with Recitation', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'MAC 1105C', 'cname' : 'College Algebra with Recitation', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : True, 'science' : False, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'AST 2002L', 'cname' : 'Discovering Astronomy Lab', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

    {'class_id' : 'BSC 1930', 'cname' : 'Current Applications in Biology', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 2, 'description' : ''},

    {'class_id' : 'CHM 1025', 'cname' : 'Introduction to Chemistry', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 2, 'description' : ''},

    {'class_id' : 'CHM 1025L', 'cname' : 'Introduction to Chemistry Lab', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

    {'class_id' : 'CHM 2045L', 'cname' : 'General Chemistry I Laboratory', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

    {'class_id' : 'HUN 1001', 'cname' : 'Introduction to Nutrition Science', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 2, 'description' : ''},

    {'class_id' : 'HUN 2201', 'cname' : 'Basic Principles of Human Nutrition', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'IDC 2000', 'cname' : 'The Beauty and Joy of Computing', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHI 2101', 'cname' : 'Introduction to Logic', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHY 1020L', 'cname' : 'Discovering Physics Laboratory: How things work', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

    {'class_id' : 'PHY 1028', 'cname' : 'Introduction to Physics', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 2, 'description' : ''},

    {'class_id' : 'PHY 1028L', 'cname' : 'Introduction to Physics Lab', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

    {'class_id' : 'PHY 2464C', 'cname' : 'The Physics of Music', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHY 2053L', 'cname' : 'Algebra-Based Physics I Lab', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

    {'class_id' : 'PHY 2054', 'cname' : 'Algebra-Based Physics II', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 3, 'description' : ''},

    {'class_id' : 'PHY 2054L', 'cname' : 'Algebra-Based Physics II Lab', 'fall': True, 'spring': True, 'summer': True, 'comp_sci' : False, 'data_sci' : False, 'info_sci' : False, 'info_tech' : False, 'info_sys' : False, 'communication': False, 'humanities' : False, 'social_sci': False, 'math_stats' : False, 'science' : True, 'completed' : False, 'credit_hrs' : 1, 'description' : ''},

]

prereq_details = [
    #Compuer Science specific prerequisites, read as "Course (course_id) has the prequisite (prerequisite_id) 
    {'course_id': 'CIS 3253', 'prerequisite_id': 'COP 2220'},
    {'course_id': 'COP 3503', 'prerequisite_id': 'COP 2220'},
    {'course_id': 'CDA 3100', 'prerequisite_id': 'COP 2220'},
    {'course_id': 'COT 3210', 'prerequisite_id': 'COT 3100'},
    {'course_id': 'COP 3530', 'prerequisite_id': 'COT 3100'},
    {'course_id': 'COP 3530', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'CNT 4504', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'COP 3703', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'COP 3404', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'COP 3404', 'prerequisite_id': 'CDA 3100'},
    {'course_id': 'COP 4620', 'prerequisite_id': 'COT 3210'},
    {'course_id': 'COP 4620', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'CEN 4010', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'COT 4400', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'CAP 4630', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'COP 4610', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'COP 4610', 'prerequisite_id': 'COP 3404'},
    {'course_id': 'CEN 4010', 'prerequisite_id': 'COP 3703'}
    ]

try:
    # Execute bulk insert
    session.execute(insert(Course).values(course_details))
    session.commit()
    print("Bulk insertion successful.")
except IntegrityError as e:
    session.rollback()  # Roll back changes to avoid partial insertions
    print(f"IntegrityError: {e}")
    print("Skipped duplicate entries.")

for p in prereq_details:
    try:
        p = association_table.insert().values(**p)
        session.execute(p)
        session.commit()
    except IntegrityError:
        session.rollback()



session.commit()


courses = session.query(Course).all()

for course in courses:
    print(course.cname, course.completed)
    prerequisites = course.prerequisites
    if prerequisites:
        print("Prerequisites:")
        for prereq in prerequisites:
            print(f"- {prereq.class_id}")
    else:
        print("No Prerequisites")
    print()
