package com.example.demo.repository;

import com.example.demo.model.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Long> {
    
    // Buscar todas las notas de una actividad
    List<Nota> findByActividadId(Long actividadId);
    
    // Calcular promedio de notas para una actividad
    @Query("SELECT AVG(CAST(n.nota AS double)) FROM Nota n WHERE n.actividadId = :actividadId")
    Double findPromedioByActividadId(@Param("actividadId") Long actividadId);
    
    // Contar notas de una actividad
    long countByActividadId(Long actividadId);
} 