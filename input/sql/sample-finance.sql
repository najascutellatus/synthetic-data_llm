CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    DOB DATE,
    SSN VARCHAR(11),
    Address TEXT,
    Email VARCHAR(255),
    Phone VARCHAR(20)
);

CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT,
    CardNumber VARCHAR(16),
    CardType VARCHAR(50),
    IssueDate DATE,
    ExpiryDate DATE,
    CreditLimit DECIMAL(10, 2),
    Balance DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    Amount DECIMAL(10, 2),
    TransactionDate DATE,
    MerchantName VARCHAR(255),
    MerchantCategory VARCHAR(255),
    Status VARCHAR(50),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY,
    AccountID INT,
    PaymentDate DATE,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Disputes (
    DisputeID INT PRIMARY KEY,
    TransactionID INT,
    Reason TEXT,
    Status VARCHAR(50),
    DateFiled DATE,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

CREATE TABLE Rewards (
    RewardID INT PRIMARY KEY,
    AccountID INT,
    PointsEarned INT,
    PointsRedeemed INT,
    CurrentPoints INT,
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);
