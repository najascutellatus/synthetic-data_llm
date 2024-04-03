-- Patients Table
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender CHAR(1),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    Address VARCHAR(255)
);

-- Healthcare Professionals Table
CREATE TABLE HealthcareProfessionals (
    ProfessionalID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Specialty VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20)
);

-- Appointments Table
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    ProfessionalID INT,
    AppointmentDate DATETIME,
    ReasonForVisit TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (ProfessionalID) REFERENCES HealthcareProfessionals(ProfessionalID)
);

-- Treatments Table
CREATE TABLE Treatments (
    TreatmentID INT PRIMARY KEY,
    AppointmentID INT,
    Description TEXT,
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
);

-- Billing Table
CREATE TABLE Billing (
    BillID INT PRIMARY KEY,
    AppointmentID INT,
    Amount DECIMAL(10, 2),
    BillingDate DATE,
    PaymentStatus VARCHAR(50),
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
);
