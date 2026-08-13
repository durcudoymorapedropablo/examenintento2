CREATE DATABASE IF NOT EXISTS organitask;
USE organitask;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    fecha_entrega DATE NOT NULL,
    descripcion TEXT NOT NULL,
    completada BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_completada DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tareas_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_tareas_usuario_fecha ON tareas(usuario_id, fecha_entrega);
