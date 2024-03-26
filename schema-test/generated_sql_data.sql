INSERT INTO Departments (DepartmentID, DepartmentName) VALUES
(1, 'Cardiology'),
(2, 'Neurology'),
(3, 'Oncology');

INSERT INTO Doctors (DoctorID, Name, Specialization) VALUES
('DOC001', 'Dr. Smith', 'Cardiologist'),
('DOC002', 'Dr. Johnson', 'Neurologist'),
('DOC003', 'Dr. Lee', 'Oncologist');

INSERT INTO DoctorDepartments (DoctorID, DepartmentID) VALUES
('DOC001', 1),
('DOC002', 2),
('DOC003', 3);

INSERT INTO Patients (PatientID, Name, Age, Gender, AssignedDoctorID) VALUES
('PT001', 'Alice Smith', 35, 'Female', 'DOC001'),
('PT002', 'Bob Johnson', 45, 'Male', 'DOC002'),
('PT003', 'Eve Lee', 55, 'Female', 'DOC003');