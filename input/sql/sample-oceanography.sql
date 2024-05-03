CREATE TABLE Research_Stations (
    StationID INT PRIMARY KEY,
    Name VARCHAR(255),
    Location VARCHAR(255),
    EstablishedYear INT,
    OperatingOrganization VARCHAR(255)
);

CREATE TABLE Researchers (
    ResearcherID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Affiliation VARCHAR(255),
    Specialization VARCHAR(255)
);

CREATE TABLE Expeditions (
    ExpeditionID INT PRIMARY KEY,
    StationID INT,
    StartDate DATE,
    EndDate DATE,
    Objective TEXT,
    FOREIGN KEY (StationID) REFERENCES Research_Stations(StationID)
);

CREATE TABLE Ocean_Regions (
    RegionID INT PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT
);

CREATE TABLE Samples (
    SampleID INT PRIMARY KEY,
    ExpeditionID INT,
    RegionID INT,
    SampleType VARCHAR(255),
    CollectedDate DATE,
    Depth DECIMAL,
    FOREIGN KEY (ExpeditionID) REFERENCES Expeditions(ExpeditionID),
    FOREIGN KEY (RegionID) REFERENCES Ocean_Regions(RegionID)
);

CREATE TABLE Water_Parameters (
    MeasurementID INT PRIMARY KEY,
    SampleID INT,
    Temperature DECIMAL,
    Salinity DECIMAL,
    pH DECIMAL,
    DissolvedOxygen DECIMAL,
    Nutrients TEXT,
    FOREIGN KEY (SampleID) REFERENCES Samples(SampleID)
);

CREATE TABLE Marine_Life (
    SpeciesID INT PRIMARY KEY,
    CommonName VARCHAR(255),
    ScientificName VARCHAR(255),
    Category VARCHAR(255)
);

CREATE TABLE Sightings (
    SightingID INT PRIMARY KEY,
    SpeciesID INT,
    SampleID INT,
    Quantity INT,
    DateObserved DATE,
    FOREIGN KEY (SpeciesID) REFERENCES Marine_Life(SpeciesID),
    FOREIGN KEY (SampleID) REFERENCES Samples(SampleID)
);
