-- Crear la base de datos
CREATE DATABASE Geriatrico;
USE Geriatrico;

-- Tabla de Pacientes
CREATE TABLE Paciente (
    Id_Paciente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Paciente VARCHAR(50) NOT NULL,
    Apellido_Paciente VARCHAR(50) NOT NULL,
    Fecha_Ingreso DATE,
    Diagnostico VARCHAR(500),
    Genero ENUM('M','F','Otro'),
    Edad_Paciente TINYINT CHECK(Edad_Paciente >= 0 AND Edad_Paciente <= 99)
);

-- Tabla de Niveles
CREATE TABLE Nivel (
    Id_Nivel INT AUTO_INCREMENT PRIMARY KEY,
    Tipo_Nivel VARCHAR(30) NOT NULL,
    Descripcion TEXT
);

-- Tabla de Puntajes
CREATE TABLE Puntaje (
    Id_Puntaje INT AUTO_INCREMENT PRIMARY KEY,
    Puntaje INT CHECK(Puntaje >= 0),
    Id_Paciente INT,
    Id_Nivel INT,
    FOREIGN KEY (Id_Paciente) REFERENCES Paciente(Id_Paciente),
    FOREIGN KEY (Id_Nivel) REFERENCES Nivel(Id_Nivel)
);

-- Tabla de Evaluaciones
CREATE TABLE Evaluacion (
    Id_Evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    Id_Paciente INT,
    Puntaje INT CHECK(Puntaje >= 0),
    FOREIGN KEY (Id_Paciente) REFERENCES Paciente(Id_Paciente)
);


INSERT INTO Paciente (Nombre_Paciente, Apellido_Paciente, Fecha_Ingreso, Diagnostico, Genero, Edad_Paciente)
VALUES ('Juan', 'Pérez', '2025-09-29', 'Deterioro cognitivo leve', 'M', 72);


select * from Evaluacion;

