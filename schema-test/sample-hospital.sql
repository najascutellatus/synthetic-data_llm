-- Creating Departments Table
CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL
);

-- Creating Doctors Table
CREATE TABLE Doctors (
    DoctorID VARCHAR(9) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100)
);

-- Because a doctor can belong to multiple departments and vice versa, 
-- we need a junction table for the many-to-many relationship.
CREATE TABLE DoctorDepartments (
    DoctorID VARCHAR(9),
    DepartmentID INT,
    PRIMARY KEY (DoctorID, DepartmentID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Creating Patients Table
CREATE TABLE Patients (
    PatientID VARCHAR(9) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    AssignedDoctorID VARCHAR(9),
    FOREIGN KEY (AssignedDoctorID) REFERENCES Doctors(DoctorID)
);
