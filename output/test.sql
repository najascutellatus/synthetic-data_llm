CREATE TABLE Patients (
    PatientID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DOB DATE,
    Gender VARCHAR(10),
    Address VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(50)
);

INSERT INTO Patients (PatientID, FirstName, LastName, DOB, Gender, Address, Phone, Email) VALUES
(1, 'John', 'Doe', '1990-05-15', 'Male', '123 Main St, City', '555-1234', 'john.doe@example.com'),
(2, 'Jane', 'Smith', '1985-08-22', 'Female', '456 Elm St, Town', '555-5678', 'jane.smith@example.com'),
(3, 'Mike', 'Johnson', '1979-11-10', 'Male', '789 Oak St, Village', '555-9012', 'mike.johnson@example.com'),
(4, 'Emily', 'Brown', '1995-02-28', 'Female', '321 Pine St, County', '555-3456', 'emily.brown@example.com'),
(5, 'David', 'Williams', '1988-04-12', 'Male', '654 Birch St, Country', '555-7890', 'david.williams@example.com'),
(6, 'Sarah', 'Wilson', '1980-09-18', 'Female', '987 Cedar St, Island', '555-2345', 'sarah.wilson@example.com'),
(7, 'Chris', 'Martinez', '1992-07-03', 'Male', '234 Maple St, State', '555-6789', 'chris.martinez@example.com'),
(8, 'Amanda', 'Garcia', '1983-12-31', 'Female', '876 Poplar St, Nation', '555-1235', 'amanda.garcia@example.com'),
(9, 'Kevin', 'Lopez', '1977-03-20', 'Male', '543 Sycamore St, World', '555-5679', 'kevin.lopez@example.com'),
(10, 'Laura', 'Torres', '1991-06-25', 'Female', '210 Cedar St, Universe', '555-9013', 'laura.torres@example.com');

CREATE TABLE MedicalRecords (
    RecordID INT PRIMARY KEY,
    PatientID INT,
    VisitDate DATE,
    DoctorID INT,
    Diagnosis VARCHAR(100),
    Treatment VARCHAR(100)
);

INSERT INTO MedicalRecords (RecordID, PatientID, VisitDate, DoctorID, Diagnosis, Treatment) VALUES
(1, 1, '2022-01-10', 1, 'Common Cold', 'Rest and fluids'),
(2, 2, '2022-02-15', 2, 'Allergic reaction', 'Antihistamines prescribed'),
(3, 3, '2022-03-20', 3, 'Fractured arm', 'Cast applied'),
(4, 4, '2022-04-25', 4, 'Influenza', 'Antiviral medication prescribed'),
(5, 5, '2022-05-30', 5, 'Sprained ankle', 'Physical therapy recommended'),
(6, 6, '2022-06-05', 6, 'Bronchitis', 'Cough syrup prescribed'),
(7, 7, '2022-07-10', 7, 'Conjunctivitis', 'Eye drops prescribed'),
(8, 8, '2022-08-15', 8, 'Pneumonia', 'Antibiotics prescribed'),
(9, 9, '2022-09-20', 9, 'Hypertension', 'Blood pressure medication prescribed'),
(10, 10, '2022-10-25', 10, 'Migraine', 'Pain relief medication prescribed');

CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE,
    Purpose VARCHAR(100),
    Status VARCHAR(20)
);

INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, AppointmentDate, Purpose, Status) VALUES
(1, 1, 1, '2022-01-05', 'Routine check-up', 'Confirmed'),
(2, 2, 2, '2022-02-10', 'Follow-up exam', 'Confirmed'),
(3, 3, 3, '2022-03-15', 'Physical therapy session', 'Confirmed'),
(4, 4, 4, '2022-04-20', 'Allergy testing', 'Confirmed'),
(5, 5, 5, '2022-05-25', 'Consultation', 'Confirmed'),
(6, 6, 6, '2022-06-30', 'Eye exam', 'Confirmed'),
(7, 7, 7, '2022-07-05', 'Prescription refill', 'Confirmed'),
(8, 8, 8, '2022-08-10', 'Pulmonary function tests', 'Confirmed'),
(9, 9, 9, '2022-09-15', 'Counseling session', 'Confirmed'),
(10, 10, 10, '2022-10-20', 'MRI scan', 'Confirmed');

CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Specialization VARCHAR(50),
    Email VARCHAR(50),
    Phone VARCHAR(20)
);

INSERT INTO Doctors (DoctorID, FirstName, LastName, Specialization, Email, Phone) VALUES
(1, 'Michael', 'Smith', 'General Practitioner', 'michael.smith@example.com', '555-1111'),
(2, 'Jennifer', 'Johnson', 'Allergist', 'jennifer.johnson@example.com', '555-2222'),
(3, 'Robert', 'Williams', 'Orthopedic Surgeon', 'robert.williams@example.com', '555-3333'),
(4, 'Sarah', 'Brown', 'Infectious Disease Specialist', 'sarah.brown@example.com', '555-4444'),
(5, 'David', 'Jones', 'Physical Therapist', 'david.jones@example.com', '555-5555'),
(6, 'Jessica', 'Garcia', 'Pulmonologist', 'jessica.garcia@example.com', '555-6666'),
(7, 'John', 'Martinez', 'Ophthalmologist', 'john.martinez@example.com', '555-7777'),
(8, 'Laura', 'Lopez', 'Internist', 'laura.lopez@example.com', '555-8888'),
(9, 'Kevin', 'Rodriguez', 'Psychiatrist', 'kevin.rodriguez@example.com', '555-9999'),
(10, 'Emily', 'Lee', 'Neurologist', 'emily.lee@example.com', '555-0000');

CREATE TABLE Staff (
    StaffID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Role VARCHAR(50),
    Email VARCHAR(50),
    Phone VARCHAR(20)
);

INSERT INTO Staff (StaffID, FirstName, LastName, Role, Email, Phone) VALUES
(1, 'Amanda', 'Brown', 'Nurse', 'amanda.brown@example.com', '555-1122'),
(2, 'Chris', 'Davis', 'Receptionist', 'chris.davis@example.com', '555-2233'),
(3, 'Megan', 'Gonzalez', 'Technician', 'megan.gonzalez@example.com', '555-3344'),
(4, 'Alex', 'Perez', 'Administrative Assistant', 'alex.perez@example.com', '555-4455'),
(5, 'Julia', 'Hernandez', 'Pharmacist', 'julia.hernandez@example.com', '555-5566'),
(6, 'Mark', 'Flores', 'Lab Technician', 'mark.flores@example.com', '555-6677'),
(7, 'Lisa', 'Morris', 'Accountant', 'lisa.morris@example.com', '555-7788'),
(8, 'Eric', 'Reyes', 'Security Officer', 'eric.reyes@example.com', '555-8899'),
(9, 'Rachel', 'Nguyen', 'Billing Specialist', 'rachel.nguyen@example.com', '555-9900'),
(10, 'Scott', 'Kim', 'IT Specialist', 'scott.kim@example.com', '555-0011');

CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    Name VARCHAR(50),
    Location VARCHAR(50),
    Phone VARCHAR(20)
);

INSERT INTO Departments (DepartmentID, Name, Location, Phone) VALUES
(1, 'Internal Medicine', 'Main Building, 1st Floor', '555-2468'),
(2, 'Orthopedics', 'East Wing, 2nd Floor', '555-1357'),
(3, 'Infectious Diseases', 'West Wing, 3rd Floor', '555-5793'),
(4, 'Physical Therapy', 'South Wing, 4th Floor', '555-8024'),
(5, 'Ophthalmology', 'North Wing, 5th Floor', '555-9135'),
(6, 'Pulmonology', 'Annex Building, Ground Floor', '555-6248'),
(7, 'Psychiatry', 'Rehabilitation Center, Upper Level', '555-3355'),
(8, 'Neurology', 'Research Institute, Lower Level', '555-4179');

CREATE TABLE RoomAllocations (
    AllocationID INT PRIMARY KEY,
    PatientID INT,
    RoomID INT,
    FromDate DATE,
    ToDate DATE
);

INSERT INTO RoomAllocations (AllocationID, PatientID, RoomID, FromDate, ToDate) VALUES
(1, 1, 101, '2022-01-01', '2022-01-10'),
(2, 2, 102, '2022-02-05', '2022-02-15'),
(3, 3, 103, '2022-03-10', '2022-03-20'),
(4, 4, 104, '2022-04-15', '2022-04-25'),
(5, 5, 105, '2022-05-20', '2022-05-30'),
(6, 6, 106, '2022-06-25', '2022-07-05'),
(7, 7, 107, '2022-07-30', '2022-08-10'),
(8, 8, 108, '2022-08-15', '2022-08-25'),
(9, 9, 109, '2022-09-20', '2022-09-30'),
(10, 10, 110, '2022-10-25', '2022-11-05');

CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY,
    RoomNumber VARCHAR(20),
    DepartmentID INT,
    Type VARCHAR(50),
    Status VARCHAR(20)
);

INSERT INTO Rooms (RoomID, RoomNumber, DepartmentID, Type, Status) VALUES
(101, '101A', 1, 'Exam Room', 'Available'),
(102, '102B', 2, 'Operating Room', 'Occupied'),
(103, '103C', 3, 'Isolation Room', 'Available'),
(104, '104D', 4, 'Therapy Room', 'Occupied'),
(105, '105E', 5, 'Consultation Room', 'Available'),
(106, '106F', 6, 'Treatment Room', 'Available'),
(107, '107G', 7, 'Counseling Room', 'Available'),
(108, '108H', 8, 'Testing Room', 'Available'),
(109, '109I', 1, 'Observation Room', 'Occupied'),
(110, '110J', 2, 'Procedure Room', 'Available');

CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    DateIssued DATE,
    Medication VARCHAR(50),
    Dosage VARCHAR(20),
    Duration VARCHAR(20)
);

INSERT INTO Prescriptions (PrescriptionID, PatientID, DoctorID, DateIssued, Medication, Dosage, Duration) VALUES
(1, 1, 1, '2022-01-10', 'Antibiotics', '500mg', '10 days'),
(2, 2, 2, '2022-02-15', 'Antihistamines', '1 tablet', '1 week'),
(3, 3, 3, '2022-03-20', 'Painkillers', '2 tablets', 'As needed'),
(4, 4, 4, '2022-04-25', 'Antiviral medication', '1 capsule', '2 weeks'),
(5, 5, 5, '2022-05-30', 'Pain relief cream', 'Apply locally', '3 times a day'),
(6, 6, 6, '2022-06-05', 'Cough syrup', '1 teaspoon', 'Every 6 hours'),
(7, 7, 7, '2022-07-10', 'Eye drops', '2 drops', 'Twice daily'),
(8, 8, 8, '2022-08-15', 'Antibiotics', '500mg', '7 days'),
(9, 9, 9, '2022-09-20', 'Blood pressure medication', '1 tablet', 'Daily'),
(10, 10, 10, '2022-10-25', 'Pain relief medication', '1 tablet', 'As needed');

CREATE TABLE Insurance (
    InsuranceID INT PRIMARY KEY,
    PatientID INT,
    Provider VARCHAR(50),
    PolicyNumber VARCHAR(50),
    CoverageDetails VARCHAR(100)
);

INSERT INTO Insurance (InsuranceID, PatientID, Provider, PolicyNumber, CoverageDetails) VALUES
(1, 1, 'XYZ Insurance', 'POL001', 'Inpatient and outpatient coverage'),
(2, 2, 'ABC Insurance', 'POL002', 'Prescription drugs and emergency care'),
(3, 3, 'DEF Insurance', 'POL003', 'Lab tests and preventive services'),
(4, 4, 'GHI Insurance', 'POL004', 'Surgical procedures and specialist visits'),
(5, 5, 'JKL Insurance', 'POL005', 'Mental health and substance abuse services'),
(6, 6, 'MNO Insurance', 'POL006', 'Maternity and newborn care'),
(7, 7, 'PQR Insurance', 'POL007', 'Rehabilitative and habilitative services'),
(8, 8, 'STU Insurance', 'POL008', 'Medical equipment and home health care'),
(9, 9, 'VWX Insurance', 'POL009', 'Chronic disease management and skilled nursing care'),
(10, 10, 'YZA Insurance', 'POL010', 'Dental and vision coverage');