create database DB_Student_Management_System;

USE DB_Student_Management_System;

CREATE TABLE User (
    userID CHAR(10) PRIMARY KEY,
    userName VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE Student (
    studentID CHAR(10) PRIMARY KEY,
    fullName VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(50),
    address VARCHAR(50),
    idNumber VARCHAR(50),
    status VARCHAR(50),
    userID CHAR(10),
    CONSTRAINT fk_student_user FOREIGN KEY (userID) REFERENCES User (userID)
) ENGINE = InnoDB;

CREATE TABLE Teacher (
    teacherID CHAR(10) PRIMARY KEY,
    fullName VARCHAR(50),
    email VARCHAR(50),
    userID CHAR(10),
    CONSTRAINT fk_teacher_user FOREIGN KEY (userID) REFERENCES User (userID)
) ENGINE = InnoDB;

CREATE TABLE Admin (
    adminID CHAR(10) PRIMARY KEY,
    userID CHAR(10),
    CONSTRAINT fk_admin_user FOREIGN KEY (userID) REFERENCES User (userID)
) ENGINE = InnoDB;

CREATE TABLE ClassRoom (
    roomID CHAR(10) PRIMARY KEY,
    roomName VARCHAR(50),
    capacity INT
) ENGINE = InnoDB;

CREATE TABLE Department (
    departmentID CHAR(10) PRIMARY KEY,
    departmentName VARCHAR(50)
) ENGINE = InnoDB;

CREATE TABLE Course (
    courseID CHAR(10) PRIMARY KEY,
    courseCode VARCHAR(50),
    courseName VARCHAR(50),
    credit INT,
    departmentID CHAR(10),
    CONSTRAINT fk_course_department FOREIGN KEY (departmentID) REFERENCES Department (departmentID)
) ENGINE = InnoDB;

CREATE TABLE Instructor (
    instructorID CHAR(10) PRIMARY KEY,
    fullName VARCHAR(50),
    email VARCHAR(50)
) ENGINE = InnoDB;

CREATE TABLE Class (
    classID CHAR(10) PRIMARY KEY,
    schedule VARCHAR(50),
    maxStudent INT,
    courseID CHAR(10),
    instructorID CHAR(10),
    roomID CHAR(10),
    CONSTRAINT fk_class_course FOREIGN KEY (courseID) REFERENCES Course (courseID),
    CONSTRAINT fk_class_instructor FOREIGN KEY (instructorID) REFERENCES Instructor (instructorID),
    CONSTRAINT fk_class_room FOREIGN KEY (roomID) REFERENCES ClassRoom (roomID)
) ENGINE = InnoDB;

CREATE TABLE Enrollment (
    enrollmentID CHAR(10) PRIMARY KEY,
    status VARCHAR(50),
    openDate DATE,
    endDate DATE,
    registeredCount INT,
    studentID CHAR(10),
    classID CHAR(10),
    CONSTRAINT fk_enrollment_student FOREIGN KEY (studentID) REFERENCES Student (studentID),
    CONSTRAINT fk_enrollment_class FOREIGN KEY (classID) REFERENCES Class (classID)
) ENGINE = InnoDB;

CREATE TABLE AcademicResult (
    resultID CHAR(10) PRIMARY KEY,
    score DOUBLE,
    grade VARCHAR(50),
    classID CHAR(10),
    studentID CHAR(10),
    CONSTRAINT fk_result_class FOREIGN KEY (classID) REFERENCES Class (classID),
    CONSTRAINT fk_result_student FOREIGN KEY (studentID) REFERENCES Student (studentID)
) ENGINE = InnoDB;

ALTER TABLE Teacher
ADD instructorID CHAR(10),
ADD CONSTRAINT fk_teacher_instructor FOREIGN KEY (instructorID) REFERENCES Instructor (instructorID);