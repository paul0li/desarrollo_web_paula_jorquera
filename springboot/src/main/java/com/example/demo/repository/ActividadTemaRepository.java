package com.example.demo.repository;

import com.example.demo.model.ActividadTema;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ActividadTemaRepository extends JpaRepository<ActividadTema, Long> {
    
    // Obtener el primer tema de una actividad
    List<ActividadTema> findByActividadId(Long actividadId);
} 